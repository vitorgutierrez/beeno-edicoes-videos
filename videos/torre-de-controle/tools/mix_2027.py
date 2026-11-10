"""Mixagem do "Plano de voo 2027": voz do Vitor + trilha + efeito de impacto na cartela.

- Trilha com automação de volume: some sob um "reverse swell" antes da cartela, fica em silêncio
  durante a cartela (só a cauda do impacto) e volta em fade suave quando a torre aparece.
- Impacto: grave cinematográfico sintetizado (sub 55→36 Hz + transiente) com reverb longo.
- Reverse swell: trecho da própria trilha passado por reverb e invertido, crescendo até o impacto.
- Ducking: a trilha baixa ~9 dB sob a voz (envelope com ataque 40 ms / release 450 ms) e mais 3 dB no fim.
Uso: python3 mix_2027.py voz.wav trilha.mp3 saida.wav --card 24.98 --tower 27.51 --dur 59.95
"""
import argparse, subprocess, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

ap = argparse.ArgumentParser()
ap.add_argument('vo'); ap.add_argument('music'); ap.add_argument('out')
ap.add_argument('--card', type=float, required=True)    # início da cartela (impacto)
ap.add_argument('--tower', type=float, required=True)   # início do plano da torre (música volta)
ap.add_argument('--dur', type=float, required=True)
ap.add_argument('--music-db', type=float, default=-8.5)
ap.add_argument('--target-lufs', type=float, default=-15.0)
o = ap.parse_args()
SR = 48000; N = int(o.dur * SR)
rng = np.random.default_rng(7)


def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    out = np.zeros((N, 2), np.float32); out[:min(N, len(a))] = a[:N]
    return out


def hall(seconds=2.8, tau=0.55):
    L = int(seconds * SR); t = np.arange(L) / SR
    ir = np.stack([rng.normal(0, 1, L), rng.normal(0, 1, L)], 1) * np.exp(-t / tau)[:, None]
    ir = sosfilt(butter(2, [90, 7000], 'bp', fs=SR, output='sos'), ir, axis=0)
    return ir / np.sqrt((ir ** 2).sum(0))


def conv(x, ir):
    return np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x) + len(ir) - 1] for c in range(2)], 1)


vo = load(o.vo); mus = load(o.music)
t = np.arange(N) / SR
db2g = lambda d: 10 ** (d / 20)

# ---------- automação da trilha
auto = np.full(N, db2g(o.music_db))
smooth = lambda x: 0.5 - 0.5 * np.cos(np.pi * np.clip(x, 0, 1))
# transição da cartela: a trilha não some. Ela abafa (filtro passa-baixa fechando) e recua para
# ~-10 dB enquanto a frase é dita, como se ficasse distante, e "abre" de novo com a torre.
k_in = smooth((t - (o.card - 1.4)) / 1.4)                  # 0→1 até a cartela
k_out = smooth((t - (o.tower - 0.75)) / 2.6)                # 0→1 depois da torre
depth = k_in * (1 - k_out)                                 # 0 = normal, 1 = recuado
auto *= db2g(-7) ** depth
cutoff = np.exp(np.log(16000) + (np.log(650) - np.log(16000)) * depth)
end_dip = t >= 41.5
auto[end_dip] *= db2g(-3) ** smooth((t[end_dip] - 41.5) / 1.5)

# ---------- ducking pela voz
vm = np.abs(vo).mean(1)
hop = 240; env = np.sqrt(np.convolve(vm ** 2, np.ones(hop) / hop, 'same'))
env_db = 20 * np.log10(env + 1e-9)
target = np.where(env_db > -38, db2g(-9), 1.0)            # voz presente → -9 dB
g = np.empty(N); g[0] = 1.0
a_att = np.exp(-1 / (0.040 * SR)); a_rel = np.exp(-1 / (0.450 * SR))
for i in range(1, N):
    a = a_att if target[i] < g[i - 1] else a_rel
    g[i] = a * g[i - 1] + (1 - a) * target[i]
# passa-baixa variável (1 polo, aplicado só onde a trilha está abafada)
lo, hi = int((o.card - 1.6) * SR), int((o.tower + 2.3) * SR)
x = mus[lo:hi].astype(np.float64); y = np.empty_like(x); z = np.zeros(2)
coef = 1 - np.exp(-2 * np.pi * cutoff[lo:hi] / SR)
for i in range(len(x)):
    z += coef[i] * (x[i] - z); y[i] = z
mus_f = mus.astype(np.float64).copy(); mus_f[lo:hi] = y
# um pouco de ambiência (reverb) na parte abafada, para soar distante e não "cortado"
wet = conv(mus_f[lo:hi] * depth[lo:hi, None], hall(4.5, 1.2))
amb = np.zeros_like(mus_f); amb[lo:lo + len(wet)] = wet[:max(0, min(len(wet), N - lo))]
# a trilha tem uma pausa composta e volta de forma brusca logo antes da torre: suaviza a reentrada
reentry = np.where(t < o.tower - 0.7, 1.0, smooth((t - (o.tower - 0.7)) / 1.3))
reentry[t < o.card + 0.5] = 1.0
music = mus_f * reentry[:, None] * (auto * g)[:, None] + amb * (db2g(o.music_db) * 0.8 * np.sqrt(g))[:, None]
fx = 0
mix = vo + music + fx

# ---------- ganho fixo para o alvo de loudness (medido pelo ffmpeg) + limitador de pico
def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

tmp = o.out + '.tmp.wav'; write(tmp, mix * 0.5)
meas = subprocess.run(['ffmpeg', '-i', tmp, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'],
                      capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith('I:')][-1].split()[1])
gain = db2g(o.target_lufs - I) * 0.5
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af',
                f'volume={20*np.log10(gain/0.5):.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=false',
                '-ar', str(SR), o.out], check=True)
subprocess.run(['rm', tmp])

# relatório: separação voz x trilha durante a fala
speech = env_db > -38
def rms_db(x, m): return 20 * np.log10(np.sqrt((x[m] ** 2).mean()) + 1e-9)
print(f'integrado antes do ganho: {I:.1f} LUFS')
for a, b, name in [(0, 24, '0-24s'), (27.5, 42, '27-42s'), (42, o.dur, '42s-fim')]:
    m = speech & (t >= a) & (t < b)
    print(f'{name:8s} voz {rms_db(vo.mean(1), m):6.1f} dB | trilha sob a voz {rms_db(music.mean(1), m):6.1f} dB')
