"""Capa do reel 01 — "Departamentos separados = Cliente frustrado".

Linguagem editorial/premium (fundo escuro, tipografia grande alinhada à esquerda,
fios finos, foto em contêiner arredondado) com a identidade do Beeno.
A foto do apresentador é dividida em dois blocos desencontrados (Atendimento /
Comercial): a própria imagem mostra a separação.

Todo o conteúdo importante fica dentro do recorte 3:4 (1080x1440) que o Instagram
mostra no grid do perfil.

Uso: python3 editor/cover.py --src /caminho/Teleprompter-2026-06-10_15-50-07.mp4
"""
import argparse
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from mg import GREEN, INK, MUTED, ROOT, WHITE, font, logo, rgba, text_img

W, H = 1080, 1920
GRID_TOP = (H - 1440) // 2  # 240: topo do recorte 3:4 do grid
MARGIN = 96


def frame(src, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1080, 1920), raw[: 1080 * 1920 * 3])


def grade(img):
    """Tratamento sóbrio: menos saturação, contraste maior e sombra puxada para o verde-tinta."""
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Brightness(img).enhance(0.86)
    tint = Image.new("RGB", img.size, INK)
    return Image.blend(img, tint, 0.18)


def background():
    bg = Image.new("RGBA", (W, H), rgba(INK))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-200, 250, 900, 1250], fill=rgba(GREEN, 38))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(220)))
    # granulação fina para dar textura de impresso
    rnd = random.Random(4)
    noise = Image.new("L", (W // 2, H // 2))
    noise.putdata([rnd.randint(0, 255) for _ in range(noise.width * noise.height)])
    noise = noise.resize((W, H), Image.NEAREST).point(lambda v: int(v * 0.035))
    grain = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    grain.putalpha(noise)
    return Image.alpha_composite(bg, grain)


def rounded_photo(img, w, h, r):
    img = ImageOps.fit(img, (w, h), Image.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def tag(txt, dot=GREEN):
    f = font("SemiBold", 26)
    ti = text_img(txt, f, WHITE, tracking=3)
    w, h = ti.width + 70, 54
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=rgba(INK))
    d.ellipse([22, h / 2 - 6, 34, h / 2 + 6], fill=rgba(dot))
    img.alpha_composite(ti, (44, (h - ti.height) // 2 - 1))
    return img


def build(src, t, out_png):
    c = background()
    d = ImageDraw.Draw(c)

    # cabeçalho editorial: marca à esquerda, rubrica à direita, fio fino
    y0 = GRID_TOP + 58
    lg = logo(150)
    c.alpha_composite(lg, (MARGIN, y0))
    eb = text_img("CRM DE VENDAS E MARKETING", font("SemiBold", 22), MUTED, tracking=3)
    c.alpha_composite(eb, (W - MARGIN - eb.width, y0 + 10))
    d.line([(MARGIN, y0 + 78), (W - MARGIN, y0 + 78)], fill=(255, 255, 255, 46), width=2)

    # foto dividida em dois blocos desencontrados
    gap, pw, ph, r = 26, 431, 690, 44
    full = grade(frame(src, t))
    ch = int(540 * ph / pw)  # mesma proporção dos blocos: nada é recortado a mais
    photo = full.crop((0, 490, 1080, 490 + ch))  # cabeça até as mãos afastadas
    half = photo.width // 2
    py = y0 + 118
    left = rounded_photo(photo.crop((0, 0, half, photo.height)), pw, ph, r)
    right = rounded_photo(photo.crop((half, 0, photo.width, photo.height)), pw, ph, r)
    lx, rx = MARGIN, MARGIN + pw + gap
    c.alpha_composite(left, (lx, py))
    c.alpha_composite(right, (rx, py + 46))
    tl, tr = tag("ATENDIMENTO"), tag("COMERCIAL")
    c.alpha_composite(tl, (lx + 22, py + ph - tl.height - 22))
    c.alpha_composite(tr, (rx + 22, py + 46 + ph - tr.height - 22))

    # título-equação
    f = font("Bold", 92)
    y = py + ph + 46 + 40
    for line in ("Departamentos", "separados"):
        im = text_img(line, f, WHITE, tracking=-3)
        c.alpha_composite(im, (MARGIN - 4, y))
        y += 100
    # sinal de igual como dois fios grossos verdes
    eq_y = y + 28
    for k in (0, 28):
        d.rounded_rectangle([MARGIN, eq_y + k, MARGIN + 110, eq_y + k + 13], 6, fill=rgba(GREEN))
    y = eq_y + 66
    x = MARGIN - 4
    for word, col in (("Cliente", WHITE), ("frustrado.", GREEN)):
        im = text_img(word, f, col, tracking=-3)
        c.alpha_composite(im, (x, y))
        x += im.width + 22


    c.convert("RGB").save(out_png, quality=95)
    return out_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--t", type=float, default=14.5, help="segundo do bruto usado na foto")
    args = ap.parse_args()
    out = os.path.join(ROOT, "output", "BEENO-REEL01-capa.png")
    build(args.src, args.t, out)
    print("->", out)


if __name__ == "__main__":
    main()
