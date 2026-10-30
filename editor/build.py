"""Pipeline de edição dos reels do Beeno.

1. Transcrição (faster-whisper, timestamps por palavra) + correções manuais
2. Cortes secos nas pausas (jump cuts) e aceleração 1.2x (como nos ADs da RVOPS)
3. Composição quadro a quadro: banner, linha de progresso, split-screen com
   motion graphics, carimbos, títulos e legendas palavra a palavra
4. Trilha original + SFX com ducking sob a voz

Uso:  python3 editor/build.py reel01 --src /caminho/bruto.mp4 [--preview]
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mg  # noqa: E402
import music  # noqa: E402
import scenes as SC  # noqa: E402

ROOT = mg.ROOT
FPS = 30
W, H = mg.W, mg.H


# ------------------------------------------------------------------ transcrição
def load_words(cfg):
    words = json.load(open(os.path.join(ROOT, cfg.TRANSCRIPT)))["words"]
    for old, near, new in cfg.FIXES:
        hits = [w for w in words if w["w"] == old and abs(w["s"] - near) < 0.35]
        if len(hits) != 1:
            raise SystemExit(f"correção ambígua/ausente: {old!r} @ {near} -> {len(hits)} ocorrências")
        hits[0]["w"] = new
    return [w for w in words if w["w"]]


def keep_segments(words, gap=0.3, pre=0.1, post=0.12, tail=0.55):
    segs = []
    s = max(0, words[0]["s"] - pre)
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] > gap:
            segs.append((s, a["e"] + post))
            s = b["s"] - pre
    segs.append((s, words[-1]["e"] + tail))
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

    def cut_points(self):
        return [c / self.speed for c in self.cum[1:-1]]


def caption_groups(words, m, keywords, max_words=4, max_chars=20):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        if w["w"][-1] in ".,?!" or len(cur) >= max_words or len(txt) >= max_chars:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        t0 = m(g[0]["s"]) - 0.05
        end = m(g[-1]["e"]) + 0.3
        nxt = m(groups[i + 1][0]["s"]) - 0.05 if i + 1 < len(groups) else end + 0.4
        out.append({
            "t0": t0, "t1": min(nxt, end + 0.6) if nxt - end > 0.6 else nxt,
            "words": [{"text": w["w"], "t": m(w["s"]),
                       "key": norm(w["w"]) in keywords} for w in g],
        })
    return out


def norm(s):
    return s.lower().strip(".,?!;:").replace("-", "")


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
        f"[vc]setpts=PTS/{speed},fps={FPS}[v];[ac]atempo={speed}[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)


# ------------------------------------------------------------------ layout
class Timeline:
    def __init__(self, scenes, duration):
        self.sc = scenes
        for i, s in enumerate(scenes):
            s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else duration + 1
            s["prev_split"] = i > 0 and scenes[i - 1]["layout"] == "split"
            s["next_split"] = i + 1 < len(scenes) and scenes[i + 1]["layout"] == "split"
            s["prev"] = scenes[i - 1] if i > 0 else None

    def at(self, t):
        for s in self.sc:
            if s["start"] <= t < s["end"]:
                return s
        return None

    def split_p(self, t):
        s = self.at(t)
        if not s or s["layout"] != "split":
            return 0.0
        p_in = 1.0 if s["prev_split"] else mg.ease_in_out((t - s["start"]) / 0.3)
        p_out = 1.0 if s["next_split"] else mg.ease_in_out((s["end"] - t) / 0.25)
        return min(p_in, p_out)

    def whooshes(self):
        ev = []
        for s in self.sc:
            if s["layout"] == "split" and not s["prev_split"]:
                ev.append((s["start"], "whoosh"))
            if s["layout"] == "split" and not s["next_split"]:
                ev.append((s["end"] - 0.15, "whoosh"))
        return ev


class Events:
    def __init__(self):
        self.list = []

    def pop(self, t):
        self.list.append((t, "pop"))
        return t

    def hit(self, t):
        self.list.append((t, "hit"))
        return t


@__import__("functools").lru_cache(maxsize=None)
def divider_line():
    img = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    g = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    ImageDraw.Draw(g).rectangle([0, 24, W, 36], fill=mg.rgba(mg.GREEN, 200))
    img = Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(img).rectangle([0, 27, W, 33], fill=mg.rgba(mg.GREEN))
    return img


def speaker(frame, area_h, zoom, face, frac):
    fx, fy = face
    ww, wh = W / zoom, area_h / zoom
    y0 = min(max(0, fy - frac * wh), H - wh)
    x0 = min(max(0, fx - ww / 2), W - ww)
    return frame.resize((W, int(area_h)), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + wh))


def zoom_for(t, cuts, sc):
    if sc and "zoom" in sc:
        return sc["zoom"]
    idx = sum(1 for c in cuts if c <= t)
    return 1.0 if idx % 2 == 0 else 1.08


# ------------------------------------------------------------------ render
def render(cfg, base, out_path, scenes, groups, chapters, events, duration, preview=None):
    tl = Timeline(scenes, duration)
    cuts = cfg._cuts
    banner = mg.banner(tuple(cfg.BANNER))
    face = cfg.FACE
    frac_full = face[1] / H

    def frame_at(t, src):
        p = tl.split_p(t)
        sc = tl.at(t)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        area_h = H - int(round(mg.PANEL_H * p))
        if area_h > 0:
            z = lerp(zoom_for(t, cuts, sc if sc and sc["layout"] != "split" else None), cfg.SPLIT_ZOOM, p)
            canvas.paste(speaker(src, area_h, z, face, mg.lerp(frac_full, cfg.SPLIT_FRAC, p)), (0, H - area_h))
        if p > 0:
            panel = mg.panel_bg().copy()
            if sc["prev_split"] and t - sc["start"] < 0.2:
                old = mg.panel_bg().copy()
                SC.DRAW[sc["prev"]["type"]](old, t, sc["prev"])
                panel = Image.blend(old, panel, mg.ease_out((t - sc["start"]) / 0.2))
            SC.DRAW[sc["type"]](panel, t, sc)
            ph = H - area_h
            canvas.paste(panel.crop((0, mg.PANEL_H - ph, W, mg.PANEL_H)), (0, 0))
        else:
            canvas.alpha_composite(mg.top_shade(620 if sc and sc["type"] == "head" else 420,
                                                215 if sc and sc["type"] == "head" else 170))
            if sc:
                SC.DRAW[sc["type"]](canvas, t, sc)
        if p > 0:
            mg.place(canvas, divider_line(), W / 2, H - area_h)
        # banner + progresso
        ba = mg.ease_out(t / 0.4)
        mg.place(canvas, banner, W / 2, 72 + (1 - ba) * -30, 1, ba)
        mg.progress(canvas, t, chapters)
        # legenda
        if not (sc and sc.get("nocap")):
            style = "light" if p >= 0.5 else "dark"
            cy = H - area_h if p >= 0.5 else cfg.CAP_Y
            cap = mg.caption(groups, t, style, None, cy)
            if cap:
                pill, shadow, scale = cap
                mg.place(canvas, shadow, W / 2, cy + 6, scale)
                mg.place(canvas, pill, W / 2, cy, scale)
        return canvas.convert("RGB")

    lerp = mg.lerp
    if preview is not None:
        os.makedirs(out_path, exist_ok=True)
        for t in preview:
            n = int(t * FPS)
            r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{n / FPS:.3f}", "-i", base, "-frames:v", "1",
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
            src = Image.frombytes("RGB", (W, H), r.stdout[: W * H * 3])
            frame_at(t, src).save(os.path.join(out_path, f"p_{t:06.2f}.jpg"), quality=88)
        return

    reader = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                              stdout=subprocess.PIPE)
    mix = out_path + ".mix.wav"
    writer = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                               "-r", str(FPS), "-i", "-", "-i", mix, "-map", "0:v", "-map", "1:a",
                               "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-profile:v", "high",
                               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                               "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    n, t0 = 0, time.time()
    fsz = W * H * 3
    while True:
        buf = reader.stdout.read(fsz)
        if len(buf) < fsz:
            break
        src = Image.frombytes("RGB", (W, H), buf)
        writer.stdin.write(frame_at(n / FPS, src).tobytes())
        n += 1
        if n % 150 == 0:
            print(f"  {n} quadros ({n / FPS:.1f}s) - {time.time() - t0:.0f}s", flush=True)
    writer.stdin.close()
    writer.wait()
    reader.wait()
    print(f"  ok: {n} quadros em {time.time() - t0:.0f}s")


def mix_audio(base, duration, events, out_wav, work):
    mus = os.path.join(work, "music.wav")
    sfx = os.path.join(work, "sfx.wav")
    music.write_wav(mus, music.music(duration))
    music.write_wav(sfx, music.sfx_track(duration, events))
    fc = ("[0:a]highpass=f=80,afftdn=nf=-38,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
          "loudnorm=I=-15:TP=-2:LRA=8,aresample=48000,asplit=2[v][key];"
          "[1:a]volume=0.20[m];[m][key]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=350[md];"
          "[2:a]volume=0.9[s];"
          "[v][md][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.93[out]")
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
    segs = keep_segments(words)
    m = TimeMap(segs, cfg.SPEED)
    cfg._cuts = m.cut_points()
    print(f"{args.reel}: {len(segs)} trechos, {m.duration:.2f}s finais")

    base = os.path.join(work, "base.mp4")
    sig = json.dumps([segs, cfg.SPEED, args.src])
    sigf = base + ".sig"
    if not (os.path.exists(base) and os.path.exists(sigf) and open(sigf).read() == sig):
        print("  gerando base cortada...")
        render_base(args.src, segs, cfg.SPEED, base)
        open(sigf, "w").write(sig)

    ev = Events()
    scenes = cfg.build(m, ev)
    duration = m.duration
    groups = caption_groups(words, m, {norm(k) for k in cfg.KEYWORDS})
    chapters = [m(c) for c in cfg.CHAPTERS]
    tl_events = sorted(ev.list + Timeline(scenes, duration).whooshes())

    if args.preview:
        render(cfg, base, os.path.join(work, "preview"), scenes, groups, chapters, tl_events, duration,
               preview=[float(x) for x in args.preview.split(",")])
        print("  prévias em", os.path.join(work, "preview"))
        return

    out = os.path.join(ROOT, "output", cfg.OUT_NAME)
    mix_audio(base, duration, tl_events, out + ".mix.wav", work)
    render(cfg, base, out, scenes, groups, chapters, tl_events, duration)
    os.remove(out + ".mix.wav")
    print("  ->", out)


if __name__ == "__main__":
    main()
