"""Som do reel "Roleta comercial": trilha (estendida em 1 compasso, no tempo) + efeitos de interface
sintetizados e sincronizados com a animação do reel.html.
Uso: python3 mix.py trilha.mp3 saida.wav"""
import subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000; DUR = 28.0; N = int(DUR * SR)
src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
m = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

# ---- estende 1 compasso (2 s a 120 BPM, fase medida 0.02 s): repete 18.02–20.02 em 20.02
def splice(x, a, b, at, xf=0.03):
    a, b, at, f = int(a * SR), int(b * SR), int(at * SR), int(xf * SR)
    seg = x[a:b].copy(); w = np.linspace(0, 1, f)[:, None]
    head, tail = x[:at].copy(), x[at:].copy()
    seg[:f] = head[-f:] * (1 - w) + seg[:f] * w
    tail[:f] = seg[-f:] * (1 - w) + tail[:f] * w
    return np.concatenate([head[:-f], seg[:-f], tail])
m = splice(m, 18.02, 20.02, 20.02)
music = np.zeros((N, 2)); L = min(N, len(m)); music[:L] = m[:L]
fo = int(26.6 * SR); music[fo:] *= np.linspace(1, 0, N - fo)[:, None] ** 2

# ---- síntese de efeitos
rng = np.random.default_rng(3)
fx = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); fx[i:j] += sig[:j - i] * g
def env(n, a=0.002, d=0.05):
    tt = np.arange(n) / SR; return (1 - np.exp(-tt / a)) * np.exp(-tt / d)
def click(f=3200, d=0.012):
    n = int(0.06 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) * env(n, 0.0005, d) + rng.normal(0, 1, n) * env(n, 0.0003, d * 0.4) * 0.3
    return sosfilt(butter(2, 900, 'hp', fs=SR, output='sos'), s)
def blip(f1=880, f2=1320, d=0.12):
    n = int(0.35 * SR); tt = np.arange(n) / SR
    f = f1 + (f2 - f1) * np.minimum(1, tt / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, d)
def ding():
    n = int(1.4 * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for k, (f, t0) in enumerate([(1318.5, 0), (1975.5, 0.11)]):
        i = int(t0 * SR); e = env(n - i, 0.002, 0.45)
        s[i:] += (np.sin(2 * np.pi * f * tt[:n - i]) + 0.25 * np.sin(2 * np.pi * 2 * f * tt[:n - i])) * e * (0.8 if k else 1)
    return s
def whoosh(dur=0.5, up=True):
    n = int(dur * SR); x = rng.normal(0, 1, n); out = np.zeros(n); z = 0.0
    fc = np.linspace(300, 4000, n) if up else np.linspace(4000, 300, n)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(n): z += a[i] * (x[i] - z); out[i] = z
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return out * e * 0.6

# 0–9 s: relógio
add(blip(660, 990, 0.10), 0.05, 0.35)                     # 09:02 aparece
add(click(2400, 0.02), 0.85, 0.5)                          # card do lead
prev = None
for i in range(int(3.0 * SR), int(5.45 * SR), int(0.004 * SR)):
    t = i / SR; x = np.clip((t - 3.0) / 2.4, 0, 1)
    run = 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
    mm = int((9 * 60 + 2 + (14 * 60 + 37 - 9 * 60 - 2) * run) // 9)
    if prev is not None and mm != prev: add(click(2800, 0.008), t, 0.28)
    prev = mm
add(blip(520, 300, 0.18), 5.42, 0.45)                       # vira vermelho (tom descendo)
# 9 s: problema / 11.6 s: automação
add(whoosh(0.55), 11.1, 0.5)
for t in (12.0, 13.6):  add(blip(880, 1320), t, 0.35)       # nós acendem
# roleta: clique a cada nome que passa (desacelerando)
prev = None
for i in range(int(13.7 * SR), int(15.75 * SR), int(0.002 * SR)):
    t = i / SR; k = np.clip((t - 13.7) / 2.0, 0, 1); r = 1 - (1 - k) ** 4; row = int(20 * r)
    if prev is not None and row != prev: add(click(3600, 0.01), t, 0.45)
    prev = row
add(blip(988, 1480, 0.16), 15.72, 0.45)                     # parou em Ana Lima
# contagem 60 → 0 (16.3–18.0): tique a cada 5 s da contagem
for s in range(55, -1, -5):
    t = 16.3 + 1.7 * (1 - s / 60); add(click(2000, 0.012), t, 0.3)
add(blip(880, 1320), 18.2, 0.35)                            # tarefa criada
add(ding(), 18.6, 0.55)                                     # notificação
# 22 s: comparação
add(whoosh(0.35, False), 22.45, 0.35)                       # risco no "5h35"
add(blip(740, 1480, 0.2), 23.0, 0.45)                       # "1 min"
add(whoosh(0.6), 24.5, 0.35)                                # entra o logo
fx = np.stack([fx, fx], 1)

mix = music * 10 ** (-5 / 20) + fx * 0.5
def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
tmp = out + '.tmp.wav'; write(tmp, mix * 0.5)
meas = subprocess.run(['ffmpeg', '-i', tmp, '-af', 'ebur128=framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith('I:')][-1].split()[1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'volume={-14 - I:.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=false', '-ar', str(SR), out], check=True)
subprocess.run(['rm', tmp]); print('ok, antes do ganho', I, 'LUFS')
