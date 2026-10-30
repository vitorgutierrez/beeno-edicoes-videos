"""Trilha ambiente original (sem direitos de terceiros), no espírito da trilha
dos ADs da RVOPS: pad sustentado, sem batida, com uma nota aguda contínua,
reverb longo e entrada/saída suaves. Fica baixa e é 'duckada' pela voz."""
import wave

import numpy as np

SR = 48000


def _hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def _lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def _reverb(x, seconds=3.2, seed=1):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 6.5 / seconds)
    ir = _lowpass(ir, 5000)
    ir /= np.sqrt(np.sum(ir ** 2))
    m = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return y


def _voice(freq, t, rng):
    """Uma voz de pad: 3 osciladores levemente desafinados, harmônicos suaves."""
    out = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.11):
        f = freq * 2 ** (det / 12)
        ph = rng.uniform(0, 2 * np.pi)
        for h, a in ((1, 1.0), (2, 0.35), (3, 0.16), (4, 0.07)):
            out += a * np.sin(2 * np.pi * f * h * t + ph * h)
    return out


def music(duration, seed=3):
    rng = np.random.default_rng(seed)
    n = int(duration * SR) + SR
    t = np.arange(n) / SR
    # progressão lenta e neutra: Dmaj9 -> Bm7 -> Gmaj7 -> A(add9), ~6s cada, com crossfade
    chords = [(50, 57, 61, 64, 69), (47, 54, 57, 62, 66), (43, 50, 54, 59, 62), (45, 52, 57, 59, 64)]
    step, xf = 6.0, 2.0
    pad = np.zeros(n)
    for i in range(int(duration / step) + 2):
        s0 = i * step - xf / 2
        env = np.clip((t - s0) / xf, 0, 1) * np.clip((s0 + step + xf - t) / xf, 0, 1)
        env = np.sin(env * np.pi / 2) ** 2
        idx = env > 0
        if not idx.any():
            continue
        for note in chords[i % 4]:
            pad[idx] += _voice(_hz(note), t[idx], rng) * env[idx] * (0.6 if note < 48 else 1.0)
    pad = _lowpass(pad, 1400)
    # respiração lenta de volume
    pad *= 0.85 + 0.15 * np.sin(2 * np.pi * t / 9.0)
    # nota aguda sustentada (o 'fio' que se ouve na trilha da RVOPS)
    shimmer = np.sin(2 * np.pi * _hz(73) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7.0 + 1)) * 0.9
    shimmer += 0.25 * np.sin(2 * np.pi * _hz(81) * t)
    sub = np.sin(2 * np.pi * _hz(38) * t) * 0.5
    dry = pad * 0.08 + shimmer * 0.12 + sub * 0.10
    out = 0.55 * dry + 0.9 * _reverb(dry)
    out = out[: int(duration * SR)]
    fi, fo = int(1.2 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi) ** 2
    out[-fo:] *= np.linspace(1, 0, fo) ** 2
    return out / (np.max(np.abs(out)) + 1e-9) * 0.8


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.stack([pcm, pcm], axis=1).tobytes())
