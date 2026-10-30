"""Primitivas visuais na identidade do Beeno (beeno.ai), com a linguagem
sóbria/documental dos ADs da RVOPS: cortes secos, entradas por fade,
linhas finas, verde só como acento.

Paleta: verde #00CD8A, tinta #0A1C15. Fonte: Poppins."""
import os
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
BRAND = os.path.join(ROOT, "assets", "brand")

W, H = 1080, 1920
PANEL_H = 960

GREEN = (0, 205, 138)
GREEN_600 = (0, 169, 115)
INK = (10, 28, 21)
INK_700 = (16, 42, 32)
WHITE = (255, 255, 255)
MUTED = (150, 165, 158)
LINE = (255, 255, 255, 34)
RED = (255, 101, 104)


def rgba(c, a=255):
    return (c[0], c[1], c[2], int(a))


@lru_cache(maxsize=None)
def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{weight}.ttf"), int(size))


# ---------------------------------------------------------------- tempo / easing
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp01(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def lerp(a, b, x):
    return a + (b - a) * x


PACE = 1.6  # multiplica a duração de todas as entradas (animações mais calmas)


def appear(t, t0, dur=0.35):
    return clamp01((t - t0) / (dur * PACE))


# ---------------------------------------------------------------- composição
def place(canvas, img, cx, cy, alpha=1.0, scale=1.0):
    """Cola img (RGBA) centrado em (cx, cy). Sem semitransparência: `alpha` só liga/desliga
    (texto nunca aparece 'vazado')."""
    if alpha < 0.5:
        return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    canvas.alpha_composite(img, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))


def fade_up(canvas, img, cx, cy, p, rise=14):
    """Entrada padrão: o elemento aparece já sólido e só sobe levemente até a posição."""
    if p <= 0:
        return
    place(canvas, img, cx, cy + (1 - ease_out(p)) * rise)


def text_img(txt, f, color=WHITE, shadow=False, tracking=0):
    asc, desc = f.getmetrics()
    widths = [f.getlength(ch) for ch in txt] if tracking else None
    w = int(sum(widths) + tracking * (len(txt) - 1)) if tracking else int(f.getlength(txt))
    pad = 24 if shadow else 2
    img = Image.new("RGBA", (w + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))

    def draw(dd, col, off=(0, 0)):
        if tracking:
            x = pad + off[0]
            for ch, cw in zip(txt, widths):
                dd.text((x, pad + off[1]), ch, font=f, fill=col)
                x += cw + tracking
        else:
            dd.text((pad + off[0], pad + off[1]), txt, font=f, fill=col)

    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(sh), (0, 0, 0, 160), (0, 3))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(10)))
    draw(ImageDraw.Draw(img), rgba(color) if len(color) == 3 else color)
    return img


def rounded(w, h, r, fill, outline=None, width=0):
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=fill, outline=outline, width=width)
    return img


def label(txt, f, fill, color, padx=28, pady=12, r=10):
    ti = text_img(txt, f, color)
    asc, desc = f.getmetrics()
    box = rounded(ti.width + padx * 2 - 4, asc + desc + pady * 2, r, rgba(fill))
    box.alpha_composite(ti, (padx - 2, pady - 2))
    return box


def eyebrow(txt, color=GREEN):
    """Rótulo pequeno em caixa-alta com bolinha (selo do site)."""
    f = font("SemiBold", 26)
    ti = text_img(txt, f, MUTED, tracking=3)
    img = Image.new("RGBA", (ti.width + 30, ti.height), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse([0, ti.height / 2 - 6, 12, ti.height / 2 + 6], fill=rgba(color))
    img.alpha_composite(ti, (26, 0))
    return img


def check_icon(size, color=GREEN, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    w = width or max(3, size // 10)
    ImageDraw.Draw(img).line([(size * 0.18, size * 0.52), (size * 0.40, size * 0.72), (size * 0.82, size * 0.28)],
                             fill=rgba(color), width=w, joint="curve")
    return img


def x_icon(size, color=RED, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = width or max(3, size // 10)
    a, b = size * 0.25, size * 0.75
    d.line([(a, a), (b, b)], fill=rgba(color), width=w)
    d.line([(a, b), (b, a)], fill=rgba(color), width=w)
    return img


def arrow_down(size, color=INK, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = width or max(3, size // 8)
    m = size / 2
    d.line([(m, size * 0.12), (m, size * 0.85)], fill=rgba(color), width=w)
    d.line([(size * 0.22, size * 0.55), (m, size * 0.86), (size * 0.78, size * 0.55)], fill=rgba(color), width=w,
           joint="curve")
    return img


@lru_cache(maxsize=None)
def logo(width):
    im = Image.open(os.path.join(BRAND, "beeno-logo-dark-bg.png")).convert("RGBA")
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


# ---------------------------------------------------------------- fundos
def panel_bg(frame):
    """Fundo do painel: o próprio quadro desfocado e escurecido com tinta verde
    (mesma ideia do fundo desfocado/escuro da RVOPS)."""
    small = frame.resize((135, 240), Image.BILINEAR).crop((0, 30, 135, 150))
    small = small.filter(ImageFilter.GaussianBlur(6)).resize((W, PANEL_H), Image.BILINEAR).convert("RGBA")
    return Image.alpha_composite(small, _tint())


@lru_cache(maxsize=None)
def _tint():
    img = Image.new("RGBA", (W, PANEL_H), rgba(INK, 222))
    v = Image.radial_gradient("L").resize((W, PANEL_H)).point(lambda x: int(x * 0.55))
    dark = Image.new("RGBA", (W, PANEL_H), (0, 0, 0, 255))
    dark.putalpha(v)
    return Image.alpha_composite(img, dark)


@lru_cache(maxsize=None)
def top_shade(height=560, strength=190):
    g = Image.linear_gradient("L").resize((W, height)).point(lambda v: int((255 - v) * strength / 255))
    img = Image.new("RGBA", (W, height), (5, 12, 9, 255))
    img.putalpha(g)
    return img


@lru_cache(maxsize=None)
def divider():
    img = Image.new("RGBA", (W, 4), rgba(GREEN))
    return img


# ---------------------------------------------------------------- legendas
def caption(groups, t, style):
    """Legenda por grupo de palavras, sempre sólida (sem revelar palavra a palavra).
    'light' = pílula branca na divisória; 'dark' = pílula tinta com borda verde."""
    g = next((grp for grp in groups if grp["t0"] <= t < grp["t1"]), None)
    if g is None:
        return None
    size = 50
    f = font("Bold", size)
    words = g["words"]

    def total(ff):
        return sum(ff.getlength(w["text"]) for w in words) + ff.getlength(" ") * (len(words) - 1)

    while total(f) > 900 and size > 38:
        size -= 2
        f = font("Bold", size)
    asc, desc = f.getmetrics()
    pw, ph = int(total(f) + 48), int(asc + desc + 20)
    if style == "light":
        pill = rounded(pw, ph, 12, rgba(WHITE))
        base_col, key_col = INK, GREEN_600
    else:
        pill = rounded(pw, ph, 12, rgba(INK), rgba(GREEN, 200), 2)
        base_col, key_col = WHITE, GREEN
    d = ImageDraw.Draw(pill)
    x, space = 24, f.getlength(" ")
    for w in words:
        col = key_col if w["key"] else base_col
        d.text((x, 8), w["text"], font=f, fill=rgba(col))
        x += f.getlength(w["text"]) + space
    return pill


# ---------------------------------------------------------------- títulos
def wrap(items, f, maxw):
    lines, cur = [], []
    for it in items:
        test = cur + [it]
        if f.getlength(" ".join(x[0] for x in test)) > maxw and cur:
            lines.append(cur)
            cur = [it]
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def headline(canvas, t, items, y_top, size=80, maxw=940):
    """Título em caixa-alta revelado palavra a palavra (cada palavra entra sólida)."""
    f = font("ExtraBold", size)
    asc, _ = f.getmetrics()
    lh = int(size * 1.12)
    space = f.getlength(" ")
    for li, line in enumerate(wrap(items, f, maxw)):
        lw = sum(f.getlength(w[0]) for w in line) + space * (len(line) - 1)
        x = W / 2 - lw / 2
        for word, tw, hi in line:
            wl = f.getlength(word)
            if t >= tw:
                img = text_img(word, f, GREEN if hi else WHITE, shadow=True)
                fade_up(canvas, img, x + wl / 2, y_top + li * lh + asc / 2 + 26, appear(t, tw, 0.25), rise=10)
            x += wl + space
