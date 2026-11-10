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
fade_out = (t >= o.card - 0.75) & (t < o.card)
auto[fade_out] *= 1 - smooth((t[fade_out] - (o.card - 0.75)) / 0.75)
auto[(t >= o.card) & (t < o.tower - 0.35)] = 0
back = t >= o.tower - 0.35
auto[back] *= smooth((t[back] - (o.tower - 0.35)) / 2.2)
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
music = mus * (auto * g)[:, None]

# ---------- reverse swell (trilha invertida com reverb) terminando no impacto
s0, s1 = int((o.card - 2.4) * SR), int((o.card - 1.2) * SR)
seg = mus[s0:s1] * db2g(o.music_db)
tail = conv(seg, hall(2.2, 0.6))
rev = tail[::-1][:int(1.6 * SR)]
rev *= (np.linspace(0, 1, len(rev)) ** 2.2)[:, None]
rev *= db2g(6)
fx = np.zeros((N + 4 * SR, 2))
c0 = int(o.card * SR)
fx[c0 - len(rev):c0] += rev

# ---------- impacto grave
L = int(3.2 * SR); tt = np.arange(L) / SR
f = 36 + 19 * np.exp(-tt / 0.18)
sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.75) * (1 - np.exp(-tt / 0.004))
sub = np.tanh(sub * 1.6) / np.tanh(1.6)
click = sosfilt(butter(2, 1800, 'lp', fs=SR, output='sos'), rng.normal(0, 1, L)) * np.exp(-tt / 0.03) * 0.35
hit = np.stack([sub + click, sub + click], 1)
hit_wet = conv(hit * 0.5, hall(3.0, 0.75))[:L + 3 * SR]
hit_all = np.zeros_like(hit_wet); hit_all[:L] += hit; hit_all += hit_wet * 0.3
hit_all *= db2g(-14)
fx[c0:c0 + len(hit_all)] += hit_all
fx = fx[:N]

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
