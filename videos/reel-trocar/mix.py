"""Som do reel "Por que trocar de CRM": trilha re-editada no tempo (120 BPM, compasso 2 s, fase 0.02 s)
com o groove entrando no exato momento em que as ferramentas viram o Beeno (16.02 s) + efeitos sincronizados.
Uso: python3 mix.py trilha.mp3 saida.wav"""
import subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000; DUR = 36.0; N = int(DUR * SR)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
m = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
seg = lambda a, b: m[int(a * SR):int(b * SR)].copy()
def xjoin(parts, xf=0.03):
    f = int(xf * SR); out = parts[0]
    for p in parts[1:]:
        w = np.linspace(0, 1, f)[:, None]; out = np.concatenate([out[:-f], out[-f:] * (1 - w) + p[:f] * w, p[f:]])
    return out
intro = seg(0, 16.02)
d = int(1.0 * SR); intro[-d:] *= np.linspace(1, 0.35, d)[:, None]          # recua antes do "merge"
m2 = xjoin([intro, seg(16.02, 24.02), seg(16.02, 24.02), seg(24.02, 28.03)])
music = np.zeros((N, 2)); L = min(N, len(m2)); music[:L] = m2[:L]
fo = int(35.0 * SR); music[fo:] *= np.linspace(1, 0, N - fo)[:, None] ** 2

rng = np.random.default_rng(11); fx = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); fx[i:j] += sig[:j - i] * g
def env(n, a=0.002, d=0.05):
    tt = np.arange(n) / SR; return (1 - np.exp(-tt / a)) * np.exp(-tt / d)
def click(f=3200, d=0.012):
    n = int(0.06 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) * env(n, 0.0005, d) + rng.normal(0, 1, n) * env(n, 0.0003, d * 0.4) * 0.3
    return sosfilt(butter(2, 900, 'hp', fs=SR, output='sos'), s)
def blip(f1=880, f2=1320, d=0.12):
    n = int(0.35 * SR); tt = np.arange(n) / SR; f = f1 + (f2 - f1) * np.minimum(1, tt / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, d)
def thunk(f=180, d=0.09):
    n = int(0.3 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt * (1 - 0.3 * tt)) * env(n, 0.002, d)
def whoosh(dur=0.5, up=True):
    n = int(dur * SR); x = rng.normal(0, 1, n); out = np.zeros(n); z = 0.0
    fc = np.linspace(300, 4500, n) if up else np.linspace(4500, 300, n); a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(n): z += a[i] * (x[i] - z); out[i] = z
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 0.6
def chord():
    n = int(1.6 * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for f in (523.25, 659.25, 783.99, 1046.5): s += np.sin(2 * np.pi * f * tt)
    return s / 4 * env(n, 0.004, 0.5)

S = 3.6                                                            # início da cena da pilha
add(blip(660, 990, 0.1), 0.05, 0.3); add(blip(740, 1110, 0.12), 1.5, 0.35)
for i in range(5): add(thunk(170 + 20 * i), S + 0.8 + i * 0.9, 0.55); add(click(2600, 0.015), S + 0.8 + i * 0.9, 0.3)
for k in range(2): add(blip(330, 260, 0.08), S + 5.8 + k * 0.16, 0.4)       # erro de sincronização
for i in range(5): add(click(3400, 0.01), S + 7.0 + i * 0.25, 0.35)          # cliente em pedaços
add(whoosh(1.0), S + 11.4 - 0.4, 0.5)                                       # blocos voam para o centro
add(chord(), 16.0, 0.5); add(blip(988, 1480, 0.2), 16.0, 0.4)               # vira o Beeno
for i in range(5): add(blip(880, 1320, 0.1), 16.6 + 0.7 + i * 1.15, 0.33)   # eventos na timeline
add(click(2400, 0.02), 22.2, 0.4)
add(whoosh(0.4), 25.85, 0.35)
for i in range(4): add(blip(784, 1175, 0.12), 26.0 + 0.9 + i * 0.95, 0.38)   # objeções respondidas
add(whoosh(0.5), 31.4, 0.35); add(blip(740, 1480, 0.2), 32.4, 0.4)
fx = np.stack([fx, fx], 1)

mix = music * 10 ** (-5 / 20) + fx * 0.5
def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
out = sys.argv[2]; tmp = out + '.tmp.wav'; write(tmp, mix * 0.5)
meas = subprocess.run(['ffmpeg', '-i', tmp, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith('I:')][-1].split()[1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'volume={-14 - I:.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=false', '-ar', str(SR), out], check=True)
subprocess.run(['rm', tmp]); print('ok', I)
