"""Trilha e clique de transição.

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
CLICK_URL = "https://assets.mixkit.co/active_storage/sfx/1120/1120-preview.mp3"


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


def click_track(work, duration, times, out_wav):
    """Clique de mouse real (Mixkit 'Clear mouse clicks', Sound Effects Free License) nas transições."""
    path = os.path.join(work, "..", "mixkit-1120-mouse-click.mp3")
    if not os.path.exists(path):
        req = urllib.request.Request(CLICK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r, open(path, "wb") as f:
            f.write(r.read())
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.085", "-t", "0.15", "-i", path, "-ac", "1",
                          "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    click = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    click = click / (np.abs(click).max() + 1e-9) * 0.30
    out = np.zeros(int(duration * SR) + SR)
    for t0 in times:
        i0 = int(max(0, t0 - 0.02) * SR)
        out[i0:i0 + len(click)] += click[: len(out) - i0]
    pcm = (np.clip(out[: int(duration * SR)], -1, 1) * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.stack([pcm, pcm], axis=1).tobytes())
