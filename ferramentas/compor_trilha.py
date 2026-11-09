"""Trilha original no estilo Beeno (guia-edicao/1-estilo-beeno.md, seção 10), sintetizada do zero: sem samples, sem direitos de terceiros.

Uso:
    python3 compor_trilha.py <master.mp4> <tempo_da_virada_s> <saida.wav>

- Batida discreta de 110 BPM, sem melodia que dispute com a fala: bumbo, palmas, chimbal, baixo e um pad abafado.
- Silêncio antes da virada; a trilha ENTRA na virada (como nos criativos 02 e 08-09).
- Ducking de -6 dB sob a voz. O nível final (12–18 dB abaixo da voz) é ajustado na montagem.
"""

import subprocess
import sys

import numpy as np

SR = 48000
BPM = 110
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(5)

# lá menor, sem melodia: Am, F, C, G (só o pad e o baixo seguem os acordes)
PROG = [(45, [57, 60, 64]), (41, [53, 57, 60]), (48, [55, 60, 64]), (43, [55, 59, 62])]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(d):
    return np.arange(int(d * SR)) / SR


def filtro(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    if hi:
        X *= 1 / np.sqrt(1 + (f / hi) ** 4)
    if lo:
        X *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def bumbo():
    t = t_(0.35)
    f = 50 + 95 * np.exp(-t * 35)
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9))


def palma():
    t = t_(0.3)
    r = filtro(rng.standard_normal(len(t)), 900, 6000)
    env = sum((t >= k) * np.exp(-np.clip(t - k, 0, None) * 75) for k in (0.0, 0.01, 0.021))
    return r * env + r * np.exp(-t * 16) * 0.2


def chimbal(aberto=False):
    t = t_(0.22 if aberto else 0.05)
    return filtro(rng.standard_normal(len(t)), 7500) * np.exp(-t * (16 if aberto else 95))


def baixo(m, d):
    t = t_(d)
    s = np.sin(2 * np.pi * hz(m) * t) + 0.2 * np.sin(4 * np.pi * hz(m) * t)
    return np.tanh(1.4 * s) * np.exp(-t * 2.2) * np.minimum(1, t / 0.005)


def pad(acorde, d):
    t = t_(d)
    s = np.zeros_like(t)
    for m in acorde:
        for det in (-0.06, 0.06):
            s += sum(np.sin(2 * np.pi * hz(m + det) * h * t + rng.uniform(0, 6.28)) / h ** 1.8 for h in range(1, 5))
    env = np.minimum(1, t / 0.3) * np.clip((d - t) / 0.3, 0, 1)
    return filtro(s * env, hi=1400) / (len(acorde) * 2 * 2)


def soma(dst, src, ini):
    i = int(round(ini * SR))
    if i < 0:
        src, i = src[-i:], 0
    k = min(len(src), len(dst) - i)
    if k > 0:
        dst[i : i + k] += src[:k]


def compor(dur, virada):
    n = int(dur * SR) + 2 * SR
    D, B, P, H = (np.zeros(n) for _ in range(4))
    k = 0
    while virada + k * BAR < dur:
        ini = virada + k * BAR
        baixo_m, acorde = PROG[k % 4]
        soma(P, pad(acorde, BAR + 0.3), ini)
        soma(B, baixo(baixo_m - 12, BEAT * 1.5), ini)
        soma(B, baixo(baixo_m - 12, BEAT * 1.5), ini + 2.5 * BEAT)
        for b in (0, 1.5, 2, 3.5) if k % 2 else (0, 2, 2.75):
            soma(D, bumbo(), ini + b * BEAT)
        for b in (1, 3):
            soma(D, palma() * 0.7, ini + b * BEAT)
        for j in range(8):
            soma(H, chimbal() * (0.5 if j % 2 else 0.3), ini + j * BEAT / 2)
        soma(H, chimbal(True) * 0.25, ini + 3.5 * BEAT)
        k += 1
    mix = 0.75 * D + 0.6 * B + 0.45 * P + 0.3 * H
    mix = mix[: int(dur * SR)]
    t = np.arange(len(mix)) / SR
    mix *= np.clip((t - virada) / 0.03, 0, 1) * np.clip((dur - t) / 0.4, 0, 1)
    return np.tanh(1.2 * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(1.2)


def envelope_voz(master, dur):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', master, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(pcm, dtype=np.float32).astype(np.float64)[: int(dur * SR)]
    v = np.pad(v, (0, max(0, int(dur * SR) - len(v))))
    j = int(0.03 * SR)
    rms = np.sqrt(np.convolve(v ** 2, np.ones(j) / j, mode='same'))
    alvo = (rms > 10 ** (-38 / 20)).astype(float)
    g = np.empty_like(alvo)
    acc = 0.0
    a_at, a_rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.4 * SR))
    for i, x in enumerate(alvo):
        a = a_at if x > acc else a_rel
        acc = a * acc + (1 - a) * x
        g[i] = acc
    return g


def main():
    master, virada, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', master],
                               capture_output=True, text=True, check=True).stdout)
    m = compor(dur, virada) * (1 - (1 - 10 ** (-6 / 20)) * envelope_voz(master, dur)) * 10 ** (-1 / 20)
    est = np.stack([m, np.roll(m, int(0.008 * SR))], axis=1)
    pcm = (np.clip(est, -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', saida], input=pcm, check=True)
    print(saida, f'{dur:.3f}s, entra na virada {virada}')


if __name__ == '__main__':
    main()
