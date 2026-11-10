"""Som do reel "Roleta comercial": trilha (estendida em 1 compasso, no tempo) + efeitos de interface
sintetizados e sincronizados com a animação do reel.html.
Uso: python3 mix.py trilha.mp3 saida.wav"""
import subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000; DUR = 36.4; N = int(DUR * SR)
src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
m = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

# ---- montagem da trilha no tempo (120 BPM, compasso = 2 s, fase 0.02 s)
from scipy.signal import resample_poly, fftconvolve
seg = lambda a, b: m[int(a * SR):int(b * SR)].copy()
def xjoin(parts, xf=0.03):
    f = int(xf * SR); out = parts[0]
    for p in parts[1:]:
        w = np.linspace(0, 1, f)[:, None]
        out = np.concatenate([out[:-f], out[-f:] * (1 - w) + p[:f] * w, p[f:]])
    return out
intro = seg(0, 11.5); intro[-int(0.08 * SR):] *= np.linspace(1, 0.2, int(0.08 * SR))[:, None]
# "fita voltando": trecho da intro invertido e acelerado 6x (11.5 → 12.9)
rw = resample_poly(seg(3.02, 11.52)[::-1], 1, 6, axis=0)
rw *= np.linspace(1, 0.6, len(rw))[:, None]
# reverse swell até o primeiro tempo do groove (12.9 → 14.02)
hit = seg(16.02, 16.7); L = int(2.0 * SR); tt = np.arange(L) / SR
ir = np.random.default_rng(5).normal(0, 1, (L, 2)) * np.exp(-tt / 0.5)[:, None]; ir /= np.sqrt((ir ** 2).sum(0))
tail = np.stack([fftconvolve(hit[:, c], ir[:, c]) for c in range(2)], 1)[::-1]
sw_len = int((14.02 - 12.9) * SR); swell = tail[-sw_len:] * (np.linspace(0, 1, sw_len) ** 2)[:, None]
swell *= 0.9 / (np.abs(swell).max() + 1e-9) * np.abs(seg(16.02, 18.02)).max()
groove = [seg(16.02, 24.02), seg(16.02, 24.02), seg(20.02, 22.02)]
m2 = np.concatenate([intro, rw, swell])
m2 = np.concatenate([m2[:int(14.02 * SR)], np.zeros((max(0, int(14.02 * SR) - len(m2)), 2))])
m2 = xjoin([m2] + groove + [seg(24.02, 28.03)])
music = np.zeros((N, 2)); L = min(N, len(m2)); music[:L] = m2[:L]
fo = int(35.2 * SR); music[fo:] *= np.linspace(1, 0, N - fo)[:, None] ** 2

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
add(whoosh(0.55), 13.5, 0.4)
for t in (14.4, 16.0):  add(blip(880, 1320), t, 0.35)       # nós acendem
# roleta: clique a cada nome que passa (desacelerando)
prev = None
for i in range(int(16.1 * SR), int(18.15 * SR), int(0.002 * SR)):
    t = i / SR; k = np.clip((t - 16.1) / 2.0, 0, 1); r = 1 - (1 - k) ** 4; row = int(20 * r)
    if prev is not None and row != prev: add(click(3600, 0.01), t, 0.45)
    prev = row
add(blip(988, 1480, 0.16), 18.12, 0.45)                     # parou em Ana Lima
# contagem 60 → 0 (16.3–18.0): tique a cada 5 s da contagem
for s in range(55, -1, -5):
    t = 18.7 + 1.7 * (1 - s / 60); add(click(2000, 0.012), t, 0.3)
add(blip(880, 1320), 20.6, 0.35)                            # tarefa criada
add(ding(), 21.0, 0.55)                                     # notificação
# desfecho: telefone chamando, atende, card muda de etapa, reunião marcada
def tone(f1, f2, d):
    n = int(d * SR); tt = np.arange(n) / SR; e = np.minimum(1, tt / 0.01) * np.minimum(1, (d - tt) / 0.02)
    return (np.sin(2 * np.pi * f1 * tt) + np.sin(2 * np.pi * f2 * tt)) * 0.5 * e
for t0 in (24.55, 25.15): add(tone(440, 480, 0.4), t0, 0.18)
add(blip(660, 990, 0.12), 25.8, 0.35)
add(whoosh(0.5), 26.8, 0.4)
add(click(2600, 0.02), 27.8, 0.5)
add(blip(988, 1480, 0.18), 27.92, 0.45)
# 22 s: comparação
add(whoosh(0.35, False), 30.35, 0.35)                       # risco no "5h35"
add(blip(740, 1480, 0.2), 30.9, 0.45)                       # "3 min"
add(whoosh(0.6), 32.4, 0.35)                                # entra o logo
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
