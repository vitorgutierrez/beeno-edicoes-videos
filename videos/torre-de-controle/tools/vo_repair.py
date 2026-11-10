"""Reparo de locução gravada como mensagem de voz do WhatsApp.

O WhatsApp aplica um "gate": tudo o que ele considera silêncio vira silêncio digital (-80 dB), o que
decepa finais de palavra e deixa vácuos entre frases. Este script:
  1. corta o trecho antes de `--start` (ruído de manuseio) com fade-in curto;
  2. suaviza cada fechamento brusco do gate com rampa de 12 ms e uma cauda de sala curta
     (convolução com resposta de impulso de ~0,3 s, só na parte "molhada");
  3. preenche o silêncio digital com ambiente de sala (ruído rosa filtrado, -60 dBFS);
  4. normaliza por ganho linear (sem compressor).
Uso: python3 vo_repair.py entrada.ogg saida.wav --offset 1.86 --start 3.17
  --offset: segundo do original que vira o 0 do filme; --start: início real da fala no original."""
import argparse, subprocess, numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--offset', type=float, default=0); ap.add_argument('--start', type=float, default=0)
ap.add_argument('--peak', type=float, default=-3.0)
o = ap.parse_args()
SR = 48000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', o.src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).copy()
x = sosfilt(butter(2, 70, 'hp', fs=SR, output='sos'), x)

# 1. ruído inicial
s = int(o.start * SR); f = int(0.03 * SR)
x[:s] = 0; x[s:s + f] *= np.linspace(0, 1, f)

# máscara de "som presente" (janela de 10 ms acima de -70 dB)
hop = int(0.01 * SR); n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
alive = db > -70
# 2a. rampas nas bordas do gate (12 ms) para não estalar
r = int(0.012 * SR); g = np.ones_like(x)
for i in range(1, n):
    if alive[i - 1] and not alive[i]:            # fechou: rampa descendo antes do corte
        a = i * hop; g[max(0, a - r):a] *= np.linspace(1, 0.15, min(r, a))
    if not alive[i - 1] and alive[i]:            # abriu: rampa subindo
        a = i * hop; g[a:a + r] *= np.linspace(0.15, 1, len(g[a:a + r]))
x = x * g
# 2b. cauda de sala: IR de ruído com decaimento exponencial (~0,3 s), mistura discreta
rng = np.random.default_rng(1)
L = int(0.32 * SR); t = np.arange(L) / SR
ir = rng.normal(0, 1, L) * np.exp(-t / 0.07); ir = sosfilt(butter(2, [200, 5000], 'bp', fs=SR, output='sos'), ir)
ir /= np.sqrt((ir ** 2).sum())
wet = fftconvolve(x, ir)[:len(x)]
x = x + wet * 0.12
# 3. ambiente de sala nos vácuos
pink = np.cumsum(rng.normal(0, 1, len(x))); pink -= np.convolve(pink, np.ones(4800) / 4800, 'same')
pink = sosfilt(butter(2, [120, 6000], 'bp', fs=SR, output='sos'), pink); pink /= np.abs(pink).max()
x = x + pink * 10 ** (-60 / 20) * (np.arange(len(x)) >= s)
# 4. ganho linear e corte do deslocamento
x = x[int(o.offset * SR):]
x *= 10 ** (o.peak / 20) / (np.abs(x).max() + 1e-9)
pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
with wave.open(o.dst, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', len(x) / SR, 's')
