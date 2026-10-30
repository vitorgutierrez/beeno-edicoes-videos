"""Pipeline de edição dos reels do Beeno.

1. Transcrição (faster-whisper, timestamps por palavra) + correções manuais
2. Cortes secos nas pausas e aceleração 1.2x (como nos ADs da RVOPS) + correção de cor
3. Composição quadro a quadro: split-screen com cortes secos, motion graphics
   sóbrios, títulos e legendas palavra a palavra
4. Trilha ambiente com ducking sob a voz

Uso:  python3 editor/build.py reel01 --src /caminho/bruto.mp4 [--preview 1.5,8,20]
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import time

from PIL import Image

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

    def at(self, t):
        return next((s for s in self.sc if s["start"] <= t < s["end"]), None)


def speaker(frame, area_h, zoom, face, frac):
    fx, fy = face
    ww, wh = W / zoom, area_h / zoom
    y0 = min(max(0, fy - frac * wh), H - wh)
    x0 = min(max(0, fx - ww / 2), W - ww)
    return frame.resize((W, int(area_h)), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + wh))


def make_frame(cfg, tl, groups, t, src):
    sc = tl.at(t)
    split = bool(sc and sc["layout"] == "split")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    if split:
        panel = mg.panel_bg(src)
        SC.DRAW[sc["type"]](panel, t, sc)
        canvas.paste(panel, (0, 0))
        canvas.paste(speaker(src, H - mg.PANEL_H, cfg.SPLIT_ZOOM, cfg.FACE, cfg.SPLIT_FRAC), (0, mg.PANEL_H))
        canvas.alpha_composite(mg.divider(), (0, mg.PANEL_H - 2))
    else:
        if sc and "zoom" in sc:
            z = sc["zoom"]
        else:  # zoom alternado a cada corte seco para disfarçar o jump cut
            z = 1.0 if sum(1 for c in cfg._cuts if c <= t) % 2 == 0 else 1.05
        canvas.paste(speaker(src, H, z, cfg.FACE, cfg.FACE[1] / H), (0, 0))
        if sc and sc["type"] in ("head", "cta_full"):
            canvas.alpha_composite(mg.top_shade(640, 200))
        if sc:
            SC.DRAW[sc["type"]](canvas, t, sc)
    if not (sc and sc.get("nocap")):
        cy = mg.PANEL_H if split else cfg.CAP_Y
        pill = mg.caption(groups, t, "light" if split else "dark")
        if pill:
            mg.place(canvas, pill, W / 2, cy)
    return canvas.convert("RGB")


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


def mix_audio(base, duration, out_wav, work):
    mus = os.path.join(work, "music.wav")
    music.write_wav(mus, music.music(duration))
    fc = ("[0:a]highpass=f=80,afftdn=nf=-38,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
          "loudnorm=I=-15:TP=-2:LRA=8,aresample=48000,asplit=2[v][key];"
          "[1:a]volume=0.30[m];[m][key]sidechaincompress=threshold=0.03:ratio=4:attack=60:release=600[md];"
          "[v][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.93[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", mus, "-filter_complex", fc,
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
    sig = json.dumps([segs, cfg.SPEED, args.src, GRADE])
    sigf = base + ".sig"
    if not (os.path.exists(base) and os.path.exists(sigf) and open(sigf).read() == sig):
        print("  gerando base cortada...")
        render_base(args.src, segs, cfg.SPEED, base)
        open(sigf, "w").write(sig)

    tl = Timeline(cfg.build(m), m.duration)
    groups = caption_groups(words, m, {norm(k) for k in cfg.KEYWORDS})

    if args.preview:
        out_dir = os.path.join(work, "preview")
        preview(cfg, base, out_dir, tl, groups, [float(x) for x in args.preview.split(",")])
        print("  prévias em", out_dir)
        return

    out = os.path.join(ROOT, "output", cfg.OUT_NAME)
    mix = os.path.join(work, "mix.wav")
    mix_audio(base, m.duration, mix, work)
    render(cfg, base, out, tl, groups, mix)
    print("  ->", out)


if __name__ == "__main__":
    main()
