"""Trilha e efeito de transição.

Trilha: "Minimal Emotion" (Mixkit, Stock Music Free License — uso liberado em
posts de redes sociais e anúncios online, sem atribuição). O arquivo não fica
no repositório: é baixado do Mixkit na primeira execução.

A trilha é posicionada para que o 'drop' (90.7s da faixa) caia exatamente no
início do CTA de cada reel.
"""
import os
import subprocess
import urllib.request
import wave

import numpy as np

SR = 48000
TRACK_URL = "https://assets.mixkit.co/music/180/180.mp3"
TRACK_DROP = 90.70  # segundo da faixa onde entra a parte cheia


def track(work):
    path = os.path.join(work, "..", "mixkit-180-minimal-emotion.mp3")
    if not os.path.exists(path):
        req = urllib.request.Request(TRACK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r, open(path, "wb") as f:
            f.write(r.read())
    return path


def music_segment(work, start, duration, out_wav):
    """Recorta a faixa a partir de `start`, com fade in/out, normalizada para -26 LUFS."""
    fade_out = 1.4
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, start):.3f}", "-t", f"{duration:.3f}",
                    "-i", track(work), "-af",
                    f"afade=t=in:d=0.6,afade=t=out:st={duration - fade_out:.3f}:d={fade_out},"
                    "loudnorm=I=-26:TP=-6:LRA=11,aresample=48000",
                    "-ac", "2", out_wav], check=True)


def whoosh_track(duration, times, out_wav, seed=7):
    """'Ar' suave e curto nas transições (ruído filtrado, bem baixo)."""
    rng = np.random.default_rng(seed)
    out = np.zeros(int(duration * SR) + SR)
    n = int(0.32 * SR)
    tt = np.arange(n) / SR
    for t0 in times:
        noise = rng.standard_normal(n)
        cut = 0.01 + 0.10 * np.sin(np.pi * tt / tt[-1]) ** 2
        y = np.empty(n)
        acc = 0.0
        for i in range(n):
            acc += cut[i] * (noise[i] - acc)
            y[i] = acc
        y *= np.sin(np.pi * tt / tt[-1]) ** 2 * 0.22
        i0 = int(max(0, t0 - 0.16) * SR)
        out[i0:i0 + n] += y[: len(out) - i0]
    pcm = (np.clip(out[: int(duration * SR)], -1, 1) * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.stack([pcm, pcm], axis=1).tobytes())
