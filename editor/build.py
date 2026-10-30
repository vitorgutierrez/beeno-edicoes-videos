"""Pipeline de edição dos reels do Beeno.

1. Transcrição (faster-whisper, timestamps por palavra) + correções manuais
2. Cortes secos nas pausas e aceleração 1.2x (como nos ADs da RVOPS) + correção de cor
3. Composição quadro a quadro: split-screen com cortes secos, motion graphics
   sóbrios, títulos e legendas palavra a palavra
4. Trilha (Mixkit) com o 'drop' sincronizado no CTA, ducking sob a voz

Uso:  python3 editor/build.py reel01 --src /caminho/bruto.mp4 [--preview 1.5,8,20]
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import time

import numpy as np

from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mg  # noqa: E402
import music  # noqa: E402
import scenes as SC  # noqa: E402

ROOT = mg.ROOT
FPS = 30
W, H = mg.W, mg.H
# tom mais sóbrio/escuro no apresentador, como nos ADs da RVOPS
GRADE = "eq=contrast=1.06:saturation=0.82:brightness=-0.03:gamma=0.97,vignette=angle=PI/5"


# ------------------------------------------------------------------ transcrição
def load_words(cfg):
    words = json.load(open(os.path.join(ROOT, cfg.TRANSCRIPT)))["words"]
    for old, near, new in cfg.FIXES:
        hits = [w for w in words if w["w"] == old and abs(w["s"] - near) < 0.35]
        if len(hits) != 1:
            raise SystemExit(f"correção ambígua/ausente: {old!r} @ {near} -> {len(hits)} ocorrências")
        hits[0]["w"] = new
    return [w for w in words if w["w"]]


def load_audio(src):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def keep_segments(words, audio, gap=0.4, pad=0.15, tail=1.5):
    """Corta só pausas longas, mantendo respiro natural. As bordas de cada trecho são
    ajustadas pela energia do áudio para nunca comer o começo/fim de uma palavra."""
    sr, hop = 16000, 160  # janelas de 10 ms
    env = np.sqrt(np.convolve(audio ** 2, np.ones(hop) / hop, "same"))[::hop]
    floor = np.percentile(env, 10)
    voiced = env > floor * 3.5

    def back(t):  # recua até achar silêncio contínuo
        i = int(t * 100)
        while i > 0 and (voiced[i] or voiced[i - 1]) and t * 100 - i < 40:
            i -= 1
        return i / 100

    def fwd(t):
        i = int(t * 100)
        while i < len(voiced) - 1 and (voiced[i] or voiced[i + 1]) and i - t * 100 < 40:
            i += 1
        return i / 100

    segs = []
    s = max(0, back(words[0]["s"]) - pad)
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] > gap:
            e, nxt = fwd(a["e"]) + pad, back(b["s"]) - pad
            if nxt > e:
                segs.append((s, e))
                s = nxt
    segs.append((s, min(len(audio) / sr, words[-1]["e"] + tail)))
    return segs


class TimeMap:
    """Converte tempo do bruto -> tempo do vídeo editado (após cortes e velocidade)."""

    def __init__(self, segs, speed):
        self.segs, self.speed = segs, speed
        self.cum = [0.0]
        for s, e in segs:
            self.cum.append(self.cum[-1] + e - s)
        self.duration = self.cum[-1] / speed

    def __call__(self, t):
        for i, (s, e) in enumerate(self.segs):
            if t < s:
                return self.cum[i] / self.speed
            if t <= e:
                return (self.cum[i] + t - s) / self.speed
        return self.duration



def norm(s):
    return s.lower().strip(".,?!;:").replace("-", "")


def caption_groups(words, m, keywords, max_words=4, max_chars=20):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"][-1] in ".,?!" or len(cur) >= max_words or len(" ".join(x["w"] for x in cur)) >= max_chars:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        end = m(g[-1]["e"]) + 0.3
        nxt = m(groups[i + 1][0]["s"]) - 0.05 if i + 1 < len(groups) else end + 0.4
        out.append({"t0": m(g[0]["s"]) - 0.05, "t1": min(nxt, end + 0.6),
                    "words": [{"text": w["w"], "t": m(w["s"]), "key": norm(w["w"]) in keywords} for w in g]})
    return out


# ------------------------------------------------------------------ base cortada
def render_base(src, segs, speed, out):
    parts, labels = [], []
    for i, (s, e) in enumerate(segs):
        d = e - s
        parts.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.02):.3f}:d=0.02[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[vc][ac];" \
        f"[vc]setpts=PTS/{speed},fps={FPS},{GRADE}[v];[ac]atempo={speed}[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)


# ------------------------------------------------------------------ composição
class Timeline:
    def __init__(self, scenes, duration):
        self.sc = scenes
        for i, s in enumerate(scenes):
            s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else duration + 1
            s["prev"] = scenes[i - 1] if i else None
        # 'layout': tela cheia <-> split (zoom leve + clique); 'panel': troca do gráfico no split
        # (dissolve + clique); 'overlay': troca de texto em tela cheia (dissolve, sem som)
        self.trans = []
        for a, b in zip(scenes, scenes[1:]):
            kind = "layout" if a["layout"] != b["layout"] else ("panel" if b["layout"] == "split" else "overlay")
            self.trans.append((b["start"], kind))

    def clicks(self):
        return [T for T, k in self.trans if k != "overlay"]

    def at(self, t):
        return next((s for s in self.sc if s["start"] <= t < s["end"]), None)


class Framing:
    """Enquadramento em tela cheia, discreto: push-in bem lento a partir do início de cada
    bloco de tela cheia e, no máximo, um punch-in suave por bloco, que se mantém até o fim
    do bloco (sem aproximar e voltar)."""
    PUSH = 0.004   # zoom por segundo
    PUNCH = 0.07

    def __init__(self, scenes, punches):
        self.blocks = []
        for sc in scenes:
            if sc["layout"] == "full" and not (self.blocks and self.blocks[-1][1] == sc["start"]):
                self.blocks.append([sc["start"], sc["end"]])
            elif sc["layout"] == "full":
                self.blocks[-1][1] = sc["end"]
        self.punches = punches

    def __call__(self, t):
        b0, b1 = next(((a, b) for a, b in self.blocks if a <= t < b), (t, t))
        z = 1 + self.PUSH * (t - b0)
        p = next((p for p in self.punches if b0 <= p <= t), None)
        if p is not None:
            z += self.PUNCH * mg.ease_in_out((t - p) / 0.7)
        return z


def zoom_blur(img, k):
    """Transição de zoom com desfoque (k: 0..1, pico no ponto de corte)."""
    w, h = img.size
    s = 1 + 0.03 * k
    big = img.resize((int(w * s), int(h * s)), Image.BILINEAR)
    x, y = (big.width - w) // 2, (big.height - h) // 2
    out = big.crop((x, y, x + w, y + h))
    small = out.resize((w // 4, h // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.0 * k))
    return Image.blend(out, small.resize((w, h), Image.BILINEAR), 0.85 * k)


def speaker(frame, area_h, zoom, face, frac):
    fx, fy = face
    ww, wh = W / zoom, area_h / zoom
    y0 = min(max(0, fy - frac * wh), H - wh)
    x0 = min(max(0, fx - ww / 2), W - ww)
    return frame.resize((W, int(area_h)), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + wh))


DISSOLVE = 0.35


def make_frame(cfg, tl, groups, t, src):
    sc = tl.at(t)
    split = bool(sc and sc["layout"] == "split")
    prev = sc["prev"] if sc and t - sc["start"] < DISSOLVE else None
    fade = mg.ease_in_out((t - sc["start"]) / DISSOLVE) if prev else 1.0
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    if split:
        panel = mg.panel_bg(src)
        if prev and prev["layout"] == "split":  # dissolve entre gráficos
            old = panel.copy()
            SC.DRAW[prev["type"]](old, t, prev)
            SC.DRAW[sc["type"]](panel, t, sc)
            panel = Image.blend(old, panel, fade)
        else:
            SC.DRAW[sc["type"]](panel, t, sc)
        canvas.paste(panel, (0, 0))
        z = cfg.SPLIT_ZOOM * (1 + Framing.PUSH * (t - sc["start"]))
        canvas.paste(speaker(src, H - mg.PANEL_H, z, cfg.FACE, cfg.SPLIT_FRAC), (0, mg.PANEL_H))
        canvas.alpha_composite(mg.divider(), (0, mg.PANEL_H - 2))
    else:
        z = cfg._framing(t)
        canvas.paste(speaker(src, H, z, cfg.FACE, cfg.FACE[1] / H), (0, 0))
        canvas.alpha_composite(mg.top_shade(640, 170))
        if prev and prev["layout"] == "full":  # dissolve entre textos
            old = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            SC.DRAW[prev["type"]](old, t, prev)
            mg.place(canvas, old, W / 2, H / 2, 1 - fade)
        if sc:
            new = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if prev else canvas
            SC.DRAW[sc["type"]](new, t, sc)
            if prev:
                mg.place(canvas, new, W / 2, H / 2, fade if prev["layout"] == "full" else 1)
    hide_cap = sc and (sc.get("nocap") or t < sc.get("cap_from", 0) or (prev and prev.get("nocap")
                                                                         and prev["layout"] == "full"))
    if not hide_cap:
        cy = mg.PANEL_H if split else cfg.CAP_Y
        pill = mg.caption(groups, t, "light" if split else "dark")
        if pill:
            mg.place(canvas, pill, W / 2, cy)
    out = canvas.convert("RGB")
    for T, kind in tl.trans:
        if kind == "layout" and abs(t - T) < 0.08:
            out = zoom_blur(out, 1 - abs(t - T) / 0.08)
    return out


def render(cfg, base, out_path, tl, groups, mix):
    reader = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                              stdout=subprocess.PIPE)
    writer = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                               "-r", str(FPS), "-i", "-", "-i", mix, "-map", "0:v", "-map", "1:a",
                               "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-profile:v", "high",
                               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                               "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    n, t0, fsz = 0, time.time(), W * H * 3
    while True:
        buf = reader.stdout.read(fsz)
        if len(buf) < fsz:
            break
        writer.stdin.write(make_frame(cfg, tl, groups, n / FPS, Image.frombytes("RGB", (W, H), buf)).tobytes())
        n += 1
        if n % 300 == 0:
            print(f"  {n} quadros ({n / FPS:.1f}s) - {time.time() - t0:.0f}s", flush=True)
    writer.stdin.close()
    writer.wait()
    reader.wait()
    print(f"  ok: {n} quadros em {time.time() - t0:.0f}s")


def preview(cfg, base, out_dir, tl, groups, times):
    os.makedirs(out_dir, exist_ok=True)
    for t in times:
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{int(t * FPS) / FPS:.3f}", "-i", base, "-frames:v", "1",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
        if len(r.stdout) < W * H * 3:
            continue
        src = Image.frombytes("RGB", (W, H), r.stdout[: W * H * 3])
        make_frame(cfg, tl, groups, t, src).save(os.path.join(out_dir, f"p_{t:06.2f}.jpg"), quality=88)


def mix_audio(base, duration, tl, out_wav, work):
    mus = os.path.join(work, "music.wav")
    sfx = os.path.join(work, "sfx.wav")
    cta = next(s["start"] for s in tl.sc if s["type"] == "cta_full")
    music.music_segment(work, music.TRACK_DROP - cta, duration, mus)
    music.click_track(work, duration, tl.clicks(), sfx)
    fc = ("[0:a]highpass=f=80,afftdn=nf=-38,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
          "loudnorm=I=-15:TP=-2:LRA=8,aresample=48000,asplit=2[v][key];"
          "[1:a][key]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=450[md];"
          "[v][md][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.93[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", mus, "-i", sfx, "-filter_complex", fc,
                    "-map", "[out]", "-ac", "2", "-ar", "48000", out_wav], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel")
    ap.add_argument("--src", required=True)
    ap.add_argument("--work", default="/tmp/beeno_work")
    ap.add_argument("--preview", help="tempos (s) separados por vírgula para gerar quadros de teste")
    args = ap.parse_args()
    cfg = importlib.import_module(f"reels.{args.reel}")
    work = os.path.join(args.work, args.reel)
    os.makedirs(work, exist_ok=True)

    words = load_words(cfg)
    segs = keep_segments(words, load_audio(args.src))
    m = TimeMap(segs, cfg.SPEED)
    print(f"{args.reel}: {len(segs)} trechos, {m.duration:.2f}s finais")

    base = os.path.join(work, "base.mp4")
    sig = json.dumps([segs, cfg.SPEED, args.src, GRADE])
    sigf = base + ".sig"
    if not (os.path.exists(base) and os.path.exists(sigf) and open(sigf).read() == sig):
        print("  gerando base cortada...")
        render_base(args.src, segs, cfg.SPEED, base)
        open(sigf, "w").write(sig)

    tl = Timeline(cfg.build(m), m.duration)
    cfg._framing = Framing(tl.sc, [m(p) for p in cfg.PUNCH])
    groups = caption_groups(words, m, {norm(k) for k in cfg.KEYWORDS})

    if args.preview:
        out_dir = os.path.join(work, "preview")
        preview(cfg, base, out_dir, tl, groups, [float(x) for x in args.preview.split(",")])
        print("  prévias em", out_dir)
        return

    out = os.path.join(ROOT, "output", cfg.OUT_NAME)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    mix = os.path.join(work, "mix.wav")
    mix_audio(base, m.duration, tl, mix, work)
    render(cfg, base, out, tl, groups, mix)
    print("  ->", out)


if __name__ == "__main__":
    main()
