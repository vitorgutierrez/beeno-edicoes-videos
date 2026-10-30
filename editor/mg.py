"""Primitivas de motion graphics na identidade visual do Beeno (beeno.ai).

Tudo é desenhado com PIL em RGBA. Paleta e tipografia seguem o site:
verde #00CD8A, tinta #0A1C15, Poppins.
"""
import math
import os
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
BRAND = os.path.join(ROOT, "assets", "brand")

W, H = 1080, 1920
PANEL_H = 960

# Paleta beeno.ai
GREEN = (0, 205, 138)
GREEN_600 = (0, 169, 115)
GREEN_300 = (95, 226, 179)
GREEN_50 = (233, 253, 245)
INK = (10, 28, 21)
INK_700 = (16, 42, 32)
INK_600 = (27, 58, 45)
WHITE = (255, 255, 255)
MUTED = (155, 181, 170)
RED = (255, 101, 104)


def rgba(c, a=255):
    return (c[0], c[1], c[2], int(a))


@lru_cache(maxsize=None)
def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{weight}.ttf"), int(size))


# ---------------------------------------------------------------- easing
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp01(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_back(x, s=1.70158):
    x = clamp01(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def lerp(a, b, x):
    return a + (b - a) * x


def appear(t, t0, dur=0.35):
    """Progresso 0..1 de uma entrada que começa em t0."""
    return clamp01((t - t0) / dur)


# ---------------------------------------------------------------- composição
def place(canvas, img, cx, cy, scale=1.0, alpha=1.0, rotate=0.0):
    """Cola img (RGBA) centrado em (cx, cy) com escala/opacidade/rotação."""
    if alpha <= 0.01 or scale <= 0.01:
        return
    if rotate:
        img = img.rotate(rotate, resample=Image.BICUBIC, expand=True)
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    if alpha < 0.999:
        a = img.getchannel("A").point(lambda v: int(v * alpha))
        img = img.copy()
        img.putalpha(a)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    canvas.alpha_composite(img, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))


def pop(canvas, img, cx, cy, p, rotate=0.0, from_scale=0.6, rise=30):
    """Entrada estilo 'pop' (escala com overshoot + fade + leve subida)."""
    if p <= 0:
        return
    place(canvas, img, cx, cy + (1 - ease_out(p)) * rise, lerp(from_scale, 1.0, ease_back(p)), ease_out(p * 1.6), rotate)


def text_size(txt, f):
    b = f.getbbox(txt)
    return b[2] - b[0], b[3] - b[1]


def text_img(txt, f, color=WHITE, tracking=0, shadow=False):
    asc, desc = f.getmetrics()
    if tracking:
        widths = [f.getlength(ch) for ch in txt]
        w = int(sum(widths) + tracking * (len(txt) - 1)) + 4
    else:
        w = int(f.getlength(txt)) + 4
    pad = 24 if shadow else 0
    img = Image.new("RGBA", (w + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

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
        draw(ImageDraw.Draw(sh), (0, 0, 0, 170), (0, 4))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(9)))
        d = ImageDraw.Draw(img)
    draw(d, rgba(color) if len(color) == 3 else color)
    return img


def rounded(w, h, r, fill, outline=None, width=0, glow=None):
    pad = 40 if glow else 0
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=glow)
        img = Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(img).rounded_rectangle([pad, pad, pad + w - 1, pad + h - 1], r, fill=fill, outline=outline, width=width)
    return img


def check_icon(size, color=GREEN, bg=None, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg:
        d.ellipse([0, 0, size - 1, size - 1], fill=rgba(bg))
    w = width or max(4, size // 9)
    s = size
    d.line([(s * 0.27, s * 0.52), (s * 0.44, s * 0.68), (s * 0.74, s * 0.34)], fill=rgba(color), width=w, joint="curve")
    return img


def x_icon(size, color=RED, bg=None, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg:
        d.ellipse([0, 0, size - 1, size - 1], fill=rgba(bg))
    w = width or max(4, size // 9)
    a, b = size * 0.32, size * 0.68
    d.line([(a, a), (b, b)], fill=rgba(color), width=w)
    d.line([(a, b), (b, a)], fill=rgba(color), width=w)
    return img


def arrow_icon(size, color=INK, width=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = width or max(4, size // 8)
    m = size / 2
    d.line([(size * 0.15, m), (size * 0.82, m)], fill=rgba(color), width=w)
    d.line([(size * 0.55, size * 0.25), (size * 0.85, m), (size * 0.55, size * 0.75)], fill=rgba(color), width=w, joint="curve")
    return img


@lru_cache(maxsize=None)
def logo(width):
    im = Image.open(os.path.join(BRAND, "beeno-logo-dark-bg.png")).convert("RGBA")
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


@lru_cache(maxsize=None)
def icon(size):
    im = Image.open(os.path.join(BRAND, "beeno-icon.png")).convert("RGBA")
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- fundos
@lru_cache(maxsize=None)
def panel_bg():
    """Fundo do painel superior: gradiente tinta + grid sutil + brilho verde (hero do site)."""
    img = Image.new("RGBA", (W, PANEL_H), rgba(INK))
    grad = Image.linear_gradient("L").resize((W, PANEL_H))
    top = Image.new("RGBA", (W, PANEL_H), rgba((14, 52, 38)))
    img = Image.composite(img, top, grad)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 72):
        d.line([(x, 0), (x, PANEL_H)], fill=(255, 255, 255, 9), width=1)
    for y in range(0, PANEL_H, 72):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 9), width=1)
    glow = Image.new("RGBA", (W, PANEL_H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W * 0.15, PANEL_H * 0.25, W * 0.85, PANEL_H * 0.95], fill=rgba(GREEN, 46))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(120)))
    return img


@lru_cache(maxsize=None)
def top_shade(height=560, strength=200):
    g = Image.linear_gradient("L").resize((W, height)).point(lambda v: int((255 - v) * strength / 255))
    img = Image.new("RGBA", (W, height), rgba(INK))
    img.putalpha(g)
    return img


@lru_cache(maxsize=None)
def bottom_shade(height=700, strength=170):
    g = Image.linear_gradient("L").resize((W, height)).point(lambda v: int(v * strength / 255))
    img = Image.new("RGBA", (W, height), rgba(INK))
    img.putalpha(g)
    return img


# ---------------------------------------------------------------- elementos fixos
@lru_cache(maxsize=None)
def banner(parts):
    """Pílula superior com chamada de público. parts = ((texto, destaque), ...)."""
    f = font("Bold", 27)
    imgs = [text_img(t, f, GREEN if hi else WHITE) for t, hi in parts]
    gap = 10
    tw = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    pw, ph = tw + 64, 66
    # bolinha verde do selo do site
    pill = rounded(pw + 26, ph, ph // 2, rgba(INK, 200), rgba(GREEN, 160), 2)
    d = ImageDraw.Draw(pill)
    d.ellipse([30, ph / 2 - 6, 42, ph / 2 + 6], fill=rgba(GREEN))
    x = 58
    for im in imgs:
        pill.alpha_composite(im, (x, (ph - im.height) // 2 - 1))
        x += im.width + gap
    return pill


def progress(canvas, t, marks, y=150, x0=250, x1=830):
    """Linha de progresso com 3 pontos (capítulos), como na referência."""
    if t < marks[0] - 0.4:
        return
    a = ease_out((t - (marks[0] - 0.4)) / 0.4)
    layer = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    xs = [lerp(x0, x1, i / (len(marks) - 1)) for i in range(len(marks))]
    d.line([(x0, 30), (x1, 30)], fill=(255, 255, 255, 70), width=4)
    # a linha avança até o último ponto ativado
    fill_x = x0
    for i in range(1, len(marks)):
        if t >= marks[i]:
            fill_x = lerp(xs[i - 1], xs[i], ease_in_out((t - marks[i]) / 0.5))
    glow = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    if fill_x > x0:
        gd.line([(x0, 30), (fill_x, 30)], fill=rgba(GREEN, 255), width=10)
        d.line([(x0, 30), (fill_x, 30)], fill=rgba(GREEN), width=5)
    for i, (x, m) in enumerate(zip(xs, marks)):
        on = t >= m
        if on:
            k = ease_back((t - m) / 0.35)
            r = 13 * k
            gd.ellipse([x - r - 6, 30 - r - 6, x + r + 6, 30 + r + 6], fill=rgba(GREEN))
            d.ellipse([x - 13, 30 - 13, x + 13, 30 + 13], fill=rgba(INK), outline=(255, 255, 255, 90), width=3)
            d.ellipse([x - r, 30 - r, x + r, 30 + r], fill=rgba(GREEN))
        else:
            d.ellipse([x - 12, 30 - 12, x + 12, 30 + 12], fill=rgba(INK, 200), outline=(255, 255, 255, 140), width=3)
    layer = Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)), layer)
    place(canvas, layer, W / 2, y, 1.0, a)


# ---------------------------------------------------------------- legendas
def caption(groups, t, style, keywords, cy):
    """Legenda palavra a palavra. Palavra falada = opaca; próximas = esmaecidas.
    style 'light' (pílula branca, na divisória) ou 'dark' (pílula tinta com borda verde)."""
    g = None
    for grp in groups:
        if grp["t0"] <= t < grp["t1"]:
            g = grp
            break
    if g is None:
        return None
    size = 52
    f = font("Bold", size)
    words = g["words"]
    space = f.getlength(" ")
    total = sum(f.getlength(w["text"]) for w in words) + space * (len(words) - 1)
    while total > 900 and size > 38:
        size -= 2
        f = font("Bold", size)
        space = f.getlength(" ")
        total = sum(f.getlength(w["text"]) for w in words) + space * (len(words) - 1)
    asc, desc = f.getmetrics()
    pw, ph = int(total + 52), int(asc + desc + 22)
    if style == "light":
        pill = rounded(pw, ph, 14, rgba(WHITE, 250))
        base_col, key_col = INK, GREEN_600
    else:
        pill = rounded(pw, ph, 14, rgba(INK, 225), rgba(GREEN, 230), 3)
        base_col, key_col = WHITE, GREEN
    d = ImageDraw.Draw(pill)
    x = 26
    for w in words:
        spoken = t >= w["t"] - 0.03
        key = w["key"]
        col = key_col if key else base_col
        a = 255 if spoken else 80
        d.text((x, 9), w["text"], font=f, fill=rgba(col, a))
        x += f.getlength(w["text"]) + space
    k = (t - g["t0"]) / 0.14
    scale = lerp(0.88, 1.0, ease_back(k)) if k < 1 else 1.0
    shadow = rounded(pw, ph, 14, (0, 0, 0, 0), glow=(0, 0, 0, 110))
    return pill, shadow, scale


# ---------------------------------------------------------------- blocos reutilizáveis
def label_box(txt, f, fill, color, padx=30, pady=14, r=12):
    ti = text_img(txt, f, color)
    asc, desc = f.getmetrics()
    box = rounded(ti.width + padx * 2, asc + desc + pady * 2, r, rgba(fill))
    box.alpha_composite(ti, (padx, pady))
    return box


def stamp(txt, color=GREEN, size=78, rotate=-7):
    f = font("ExtraBold", size)
    ti = text_img(txt, f, color, tracking=6)
    asc, desc = f.getmetrics()
    w, h = ti.width + 56, asc + desc + 30
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([3, 3, w - 4, h - 4], 10, fill=rgba(INK, 150), outline=rgba(color), width=6)
    img.alpha_composite(ti, (28, 13))
    glow = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    glow.alpha_composite(img, (30, 30))
    g = glow.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(g, glow)
    return out.rotate(rotate, resample=Image.BICUBIC, expand=True)


def stamp_anim(canvas, img, cx, cy, t, t0):
    """Carimbo que 'bate' (escala 1.6 -> 1)."""
    if t < t0:
        return
    k = clamp01((t - t0) / 0.22)
    place(canvas, img, cx, cy, lerp(1.7, 1.0, ease_out(k)), ease_out(k * 1.5))


def card(w, h, r=30, fill=INK_700, border=GREEN, border_a=90):
    return rounded(w, h, r, rgba(fill, 245), rgba(border, border_a), 2, glow=rgba(GREEN, 40))


def avatar(size, letter, bg=GREEN, fg=INK):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=rgba(bg))
    f = font("Bold", int(size * 0.48))
    tw = f.getlength(letter)
    asc, desc = f.getmetrics()
    d.text(((size - tw) / 2, (size - asc - desc) / 2), letter, font=f, fill=rgba(fg))
    return img


def bubble(txt, side="in", maxw=600, size=34):
    f = font("Medium", size)
    words = txt.split()
    lines, cur = [], ""
    for w_ in words:
        nxt = (cur + " " + w_).strip()
        if f.getlength(nxt) > maxw - 56 and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = nxt
    lines.append(cur)
    asc, desc = f.getmetrics()
    lh = asc + desc + 4
    tw = max(f.getlength(l) for l in lines)
    bw, bh = int(tw + 56), int(lh * len(lines) + 30)
    fill = rgba(GREEN_50) if side == "in" else rgba(GREEN)
    img = rounded(bw, bh, 26, fill)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text((28, 13 + i * lh), l, font=f, fill=rgba(INK))
    return img


def typing(t):
    img = rounded(130, 64, 26, rgba(GREEN_50))
    d = ImageDraw.Draw(img)
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(t * 9 - i * 0.9)
        c = int(lerp(150, 40, k))
        d.ellipse([30 + i * 26 - 8, 32 - 8 - k * 5, 30 + i * 26 + 8, 32 + 8 - k * 5], fill=(c, c + 15, c + 8, 255))
    return img


def chip(big, small, accent=GREEN, w=None, big_img=None):
    fb = font("ExtraBold", 84)
    fs = font("ExtraBold", 54)
    bi = big_img if big_img is not None else text_img(big, fb, accent)
    si = text_img(small, fs, WHITE)
    cw = w or (bi.width + si.width + 100)
    ch = 136
    img = rounded(cw, ch, ch // 2, rgba(INK, 235), rgba(accent, 200), 3, glow=rgba(accent, 70))
    pad = 40
    img.alpha_composite(bi, (pad + 34, pad + (ch - bi.height) // 2 + 2))
    img.alpha_composite(si, (pad + 34 + bi.width + 18, pad + (ch - si.height) // 2 + 3))
    return img


def wrap_words(words, f, maxw):
    lines, cur = [], []
    for w_ in words:
        test = cur + [w_]
        if f.getlength(" ".join(x[0] for x in test)) > maxw and cur:
            lines.append(cur)
            cur = [w_]
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def headline(canvas, t, items, cy, size=92, maxw=960, align_top=False):
    """Título grande revelado palavra a palavra. items = [(palavra, t_out, destaque)]."""
    f = font("Black", size)
    lines = wrap_words(items, f, maxw)
    asc, desc = f.getmetrics()
    lh = int(size * 1.08)
    total_h = lh * len(lines)
    y0 = cy if align_top else cy - total_h / 2
    space = f.getlength(" ")
    for li, line in enumerate(lines):
        lw = sum(f.getlength(w[0]) for w in line) + space * (len(line) - 1)
        x = W / 2 - lw / 2
        for word, tw, hi in line:
            wl = f.getlength(word)
            if t >= tw:
                k = (t - tw) / 0.22
                img = text_img(word, f, GREEN if hi else WHITE, shadow=True)
                place(canvas, img, x + wl / 2, y0 + li * lh + asc / 2 + 34 + (1 - ease_out(k)) * 26,
                      lerp(0.85, 1, ease_back(k)), ease_out(k * 1.4))
            x += wl + space
