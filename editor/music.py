"""Trilha e clique de transição.

Trilhas: arquivos enviados pelo cliente, em assets/music/ (fora do git). A faixa é
posicionada para que a batida cheia entre quando o gancho termina.
Clique: Mixkit 'Clear mouse clicks' (Sound Effects Free License), baixado na 1a execução.
"""
import os
import subprocess
import urllib.request
import wave

import numpy as np

SR = 48000
CLICK_URL = "https://assets.mixkit.co/active_storage/sfx/1120/1120-preview.mp3"


def music_segment(path, start, duration, out_wav):
    """Recorta a faixa a partir de `start`, com fade in/out, normalizada para -24 LUFS."""
    fade_out = 1.0
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, start):.3f}", "-t", f"{duration:.3f}",
                    "-i", path, "-af",
                    f"afade=t=in:d=0.4,afade=t=out:st={duration - fade_out:.3f}:d={fade_out},"
                    "highpass=f=35,loudnorm=I=-24:TP=-6:LRA=11,aresample=48000",
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
