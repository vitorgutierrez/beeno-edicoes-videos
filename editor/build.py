"""Pipeline de edição dos reels do Beeno.

1. Transcrição (faster-whisper, timestamps por palavra) + correções manuais
2. Cortes secos em todas as pausas (bordas ajustadas pela energia do áudio para não
   comer palavras), início no primeiro som e fim logo após a última palavra
3. Composição quadro a quadro: split-screen, motion graphics sóbrios, títulos e legendas.
   Nada de transparência em texto: tudo entra sólido
4. Trilha enviada pelo cliente, com a batida entrando no fim do gancho, ducking sob a voz,
   e clique de mouse nas trocas de cena

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


# ------------------------------------------------------------------ transcrição / cortes
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


def keep_segments(words, audio, gap=0.2, pad=0.06, end_max=None):
    """Corta toda pausa acima de `gap`. As bordas de cada trecho são ajustadas pela energia
    do áudio (o timestamp da transcrição às vezes atrasa) para nunca comer uma palavra."""
    sr = 16000
    env = np.sqrt(np.convolve(audio ** 2, np.ones(160) / 160, "same"))[::160]  # 10 ms
    voiced = env > np.percentile(env, 10) * 3.5

    def back(t):  # recua até o silêncio que antecede a palavra
        i = int(t * 100)
        while i > 0 and (voiced[i] or voiced[i - 1]) and t * 100 - i < 40:
            i -= 1
        return i / 100

    def fwd(t):  # avança até o silêncio depois da palavra
        i = int(t * 100)
        while i < len(voiced) - 1 and (voiced[i] or voiced[i + 1]) and i - t * 100 < 40:
            i += 1
        return i / 100

    segs, sentence_end = [], []
    # começa na primeira palavra (sem o 'respiro' parado antes de ele falar)
    s = max(0, back(words[0]["s"]) - 0.04, words[0]["s"] - 0.25)
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] > gap:
            e, nxt = fwd(a["e"]) + pad, back(b["s"]) - pad
            if nxt - e > 0.04:
                segs.append((s, e))
                sentence_end.append(a["w"][-1] in ".?!")
                s = nxt
    end = fwd(words[-1]["e"]) + 0.25
    segs.append((s, min(end, end_max or end, len(audio) / sr)))
    return segs, sentence_end


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

    def cuts(self):
        return [c / self.speed for c in self.cum[1:-1]]


def norm(s):
    return s.lower().strip(".,?!;:").replace("-", "")


def caption_groups(words, m, keywords, tl, max_words=4, max_chars=20):
    """Agrupa as palavras em legendas. Palavras que já aparecem num título (cenas com
    'nocap' ou antes de 'cap_from') não viram legenda, e nenhum grupo atravessa troca de cena."""
    groups, cur, cur_sc = [], [], None
    for w in words:
        t = m(w["s"])
        sc = tl.at(t)
        if sc and (sc.get("nocap") or t < sc.get("cap_from", 0)):
            if cur:
                groups.append(cur)
            cur, cur_sc = [], None
            continue
        if cur and sc is not cur_sc:
            groups.append(cur)
            cur = []
        cur.append(w)
        cur_sc = sc
        if w["w"][-1] in ".,?!" or len(cur) >= max_words or len(" ".join(x["w"] for x in cur)) >= max_chars:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        t0 = m(g[0]["s"])
        sc = tl.at(t0)
        end = min(m(g[-1]["e"]) + 0.35, sc["end"] if sc else 1e9)
        nxt = m(groups[i + 1][0]["s"]) if i + 1 < len(groups) else end
        out.append({"t0": max(t0 - 0.04, sc["start"] if sc else 0), "t1": min(nxt, end),
                    "words": [{"text": w["w"], "key": norm(w["w"]) in keywords} for w in g]})
    return out


# ------------------------------------------------------------------ base cortada
def render_base(src, segs, speed, out):
    parts, labels = [], []
    for i, (s, e) in enumerate(segs):
        d = e - s
        parts.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.01,afade=t=out:st={max(0, d - 0.015):.3f}:d=0.015[a{i}];")
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
        # trocas visuais (tela cheia <-> split, ou troca de gráfico no split): clique + 'assentar'
        self.trans = [b["start"] for a, b in zip(scenes, scenes[1:])
                      if a["layout"] != b["layout"] or b["layout"] == "split"]

    def at(self, t):
        return next((s for s in self.sc if s["start"] <= t < s["end"]), None)


class Framing:
    """Enquadramento fixo em tela cheia. Só muda (corte seco, sem animação) entre aberto e
    fechado nos cortes que caem no fim de uma frase."""
    CLOSE = 1.1

    def __init__(self, cut_times, sentence_end):
        self.switch = [t for t, se in zip(cut_times, sentence_end) if se]

    def __call__(self, t):
        return self.CLOSE if sum(1 for c in self.switch if c <= t) % 2 else 1.0


def speaker(frame, area_h, zoom, face, frac):
    fx, fy = face
    ww, wh = W / zoom, area_h / zoom
    y0 = min(max(0, fy - frac * wh), H - wh)
    x0 = min(max(0, fx - ww / 2), W - ww)
    return frame.resize((W, int(area_h)), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + wh))


def settle(img, k):
    """Corte com 'assentada': a cena nova entra 4% maior e volta ao tamanho em 0.2s."""
    s = 1 + 0.04 * k
    w, h = img.size
    big = img.resize((int(w * s), int(h * s)), Image.BILINEAR)
    x, y = (big.width - w) // 2, (big.height - h) // 2
    return big.crop((x, y, x + w, y + h))


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
        canvas.paste(speaker(src, H, cfg._framing(t), cfg.FACE, cfg.FACE[1] / H), (0, 0))
        canvas.alpha_composite(mg.top_shade(640, 170))
        if sc:
            SC.DRAW[sc["type"]](canvas, t, sc)
    T = next((T for T in tl.trans if 0 <= t - T < 0.2), None)
    if T is not None:
        canvas = settle(canvas, 1 - mg.ease_out((t - T) / 0.2))
    pill = mg.caption(groups, t, "light" if split else "dark")
    if pill:
        mg.place(canvas, pill, W / 2, mg.PANEL_H if split else cfg.CAP_Y)
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


def mix_audio(cfg, base, duration, tl, out_wav, work):
    mus = os.path.join(work, "music.wav")
    sfx = os.path.join(work, "sfx.wav")
    track, drop = cfg.MUSIC
    first_cut = tl.sc[1]["start"]  # a batida cheia entra quando o gancho termina
    music.music_segment(os.path.join(ROOT, "assets", "music", track), drop - first_cut, duration, mus)
    music.click_track(work, duration, tl.trans, sfx)
    fc = ("[0:a]highpass=f=80,afftdn=nf=-38,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
          "loudnorm=I=-15:TP=-2:LRA=8,aresample=48000,asplit=2[v][key];"
          "[1:a][key]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=400[md];"
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
    segs, sentence_end = keep_segments(words, load_audio(args.src), end_max=getattr(cfg, "END_MAX", None))
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
    cfg._framing = Framing(m.cuts(), sentence_end)
    groups = caption_groups(words, m, {norm(k) for k in cfg.KEYWORDS}, tl)

    if args.preview:
        out_dir = os.path.join(work, "preview")
        preview(cfg, base, out_dir, tl, groups, [float(x) for x in args.preview.split(",")])
        print("  prévias em", out_dir)
        return

    out = os.path.join(ROOT, "output", cfg.OUT_NAME)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    mix = os.path.join(work, "mix.wav")
    mix_audio(cfg, base, m.duration, tl, mix, work)
    render(cfg, base, out, tl, groups, mix)
    print("  ->", out)


if __name__ == "__main__":
    main()
