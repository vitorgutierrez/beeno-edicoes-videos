"""Trilha original sintetizada (sem direitos de terceiros) + efeitos sonoros.

Trilha: pulso 'tech/corporate' leve em 104 BPM (Am - F - C - G) com pad,
arpejo em colcheias, sub-grave, kick suave e hi-hat. Fica baixa e é
'duckada' pela voz na mixagem."""
import wave

import numpy as np

SR = 48000


def _note(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def _lp(x, a):
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc)
        y[i] = acc
    return y


def _lp_fast(x, cutoff):
    # filtro passa-baixa via FFT (rápido para sinais longos)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def music(duration, bpm=104, seed=3):
    rng = np.random.default_rng(seed)
    n = int(duration * SR) + SR
    t = np.arange(n) / SR
    beat = 60 / bpm
    out = np.zeros(n)
    chords = [(57, 60, 64, 69), (53, 57, 60, 65), (48, 55, 60, 64), (55, 59, 62, 67)]  # Am F C G
    bar = beat * 4
    # pad
    pad = np.zeros(n)
    for b in range(int(duration / bar) + 2):
        ch = chords[b % 4]
        s, e = int(b * bar * SR), min(n, int((b + 1) * bar * SR) + int(0.3 * SR))
        if s >= n:
            break
        tt = t[s:e] - b * bar
        env = np.minimum(1, tt / 0.4) * np.minimum(1, np.maximum(0, (bar + 0.3 - tt) / 0.5))
        sig = np.zeros(e - s)
        for note in ch:
            for det in (-0.08, 0.08):
                fr = _note(note + det)
                ph = 2 * np.pi * fr * tt
                sig += (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph))
        pad[s:e] += sig * env
    pad = _lp_fast(pad, 1800) * 0.035
    # sidechain 'pump' no tempo
    phase = (t % beat) / beat
    pump = 0.45 + 0.55 * np.minimum(1, phase / 0.45)
    out += pad * pump
    # arpejo
    eighth = beat / 2
    arp = np.zeros(n)
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    k = 0
    while k * eighth < duration + 1:
        b = int(k * eighth / bar)
        ch = chords[b % 4]
        note = ch[pattern[k % 8]] + 12
        s = int(k * eighth * SR)
        L = int(0.35 * SR)
        e = min(n, s + L)
        tt = np.arange(e - s) / SR
        fr = _note(note)
        sig = (np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(4 * np.pi * fr * tt)) * np.exp(-tt * 9)
        arp[s:e] += sig * (0.9 if k % 2 == 0 else 0.6)
        k += 1
    out += _lp_fast(arp, 3500) * 0.05
    # sub-grave (fundamental do acorde, semínimas)
    k = 0
    while k * beat < duration + 1:
        b = int(k * beat / bar)
        fr = _note(chords[b % 4][0] - 24)
        s = int(k * beat * SR)
        e = min(n, s + int(beat * SR))
        tt = np.arange(e - s) / SR
        out[s:e] += np.sin(2 * np.pi * fr * tt) * np.minimum(1, tt / 0.02) * np.exp(-tt * 3) * 0.12
        k += 1
    # kick + hat
    k = 0
    while k * beat < duration + 1:
        s = int(k * beat * SR)
        e = min(n, s + int(0.3 * SR))
        tt = np.arange(e - s) / SR
        f = 45 + 90 * np.exp(-tt * 30)
        out[s:e] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * 0.22
        hs = int((k * beat + beat / 2) * SR)
        he = min(n, hs + int(0.06 * SR))
        if hs < n:
            noise = rng.standard_normal(he - hs)
            noise = noise - _lp(noise, 0.5)
            out[hs:he] += noise * np.exp(-np.arange(he - hs) / SR * 60) * 0.03
        k += 1
    out = out[: int(duration * SR)]
    # fade in/out
    fi, fo = int(0.8 * SR), int(1.5 * SR)
    out[:fi] *= np.linspace(0, 1, fi)
    out[-fo:] *= np.linspace(1, 0, fo)
    return out / (np.max(np.abs(out)) + 1e-9) * 0.8


def whoosh(rng, dur=0.45):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # varredura de filtro: passa-baixa com corte subindo e descendo
    cut = 0.02 + 0.25 * np.sin(np.pi * tt / dur) ** 2
    y = np.empty(n)
    acc = 0.0
    for i in range(n):
        acc += cut[i] * (noise[i] - acc)
        y[i] = acc
    env = np.sin(np.pi * tt / dur) ** 1.5
    return y * env * 1.6


def pop_sfx(dur=0.09):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 900 * np.exp(-tt * 25) + 380
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45) * 0.55


def hit_sfx(rng, dur=0.35):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 60 + 120 * np.exp(-tt * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12)
    noise = rng.standard_normal(n) * np.exp(-tt * 40) * 0.3
    return (body + noise) * 0.8


def sfx_track(duration, events, seed=7):
    rng = np.random.default_rng(seed)
    out = np.zeros(int(duration * SR) + SR)
    for t0, kind in events:
        if kind == "whoosh":
            s = whoosh(rng) * 0.35
            t0 -= 0.2
        elif kind == "hit":
            s = hit_sfx(rng) * 0.55
        else:
            s = pop_sfx() * 0.35
        i = int(max(0, t0) * SR)
        out[i:i + len(s)] += s[: len(out) - i]
    return out[: int(duration * SR)]


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    st = np.stack([pcm, pcm], axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
