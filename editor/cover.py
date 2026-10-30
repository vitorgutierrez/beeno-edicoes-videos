"""Capa do reel 01 — "Departamentos separados = Cliente frustrado".

Linguagem editorial/premium (fundo escuro, tipografia grande alinhada à esquerda,
fios finos, foto em contêiner arredondado) com a identidade do Beeno.
Foto de banco (Pexels, licença livre para uso comercial, sem atribuição): cliente
frustrada olhando o celular, com duas notificações que se contradizem — uma do
Atendimento e outra do Comercial — mostrando os departamentos que não se falam.

Todo o conteúdo importante fica dentro do recorte 3:4 (1080x1440) que o Instagram
mostra no grid do perfil.

Uso: python3 editor/cover.py
"""
import argparse
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from mg import GREEN, INK, MUTED, ROOT, WHITE, font, logo, rgba, text_img

W, H = 1080, 1920
GRID_TOP = (H - 1440) // 2  # 240: topo do recorte 3:4 do grid
MARGIN = 96


PHOTO = os.path.join(ROOT, "assets", "stock", "pexels-6383268-cliente-frustrada.jpg")


def grade(img):
    """Tratamento sóbrio: menos saturação, contraste maior e sombra puxada para o verde-tinta."""
    img = ImageEnhance.Color(img).enhance(0.7)
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


def rounded_photo(img, w, h, r, centering=(0.5, 0.5)):
    img = ImageOps.fit(img, (w, h), Image.LANCZOS, centering=centering)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def notification(dept, msg, when):
    """Card de notificação sólido (sem transparência), no estilo dos gráficos do vídeo."""
    fl, fm, fw = font("Bold", 26), font("Medium", 30), font("Regular", 22)
    w = int(max(fm.getlength(msg), 56 + fl.getlength(dept) + 40 + fw.getlength(when)) + 56)
    h = 132
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=rgba(INK), outline=(255, 255, 255, 40), width=2)
    d.ellipse([28, 32, 42, 46], fill=rgba(GREEN))
    d.text((56, 22), dept, font=fl, fill=rgba(GREEN))
    tw = fw.getlength(when)
    d.text((w - 28 - tw, 26), when, font=fw, fill=rgba(MUTED))
    d.text((28, 68), msg, font=fm, fill=rgba(WHITE))
    return img


def build(out_png):
    c = background()
    d = ImageDraw.Draw(c)

    # cabeçalho editorial: marca à esquerda, rubrica à direita, fio fino
    y0 = GRID_TOP + 58
    lg = logo(150)
    c.alpha_composite(lg, (MARGIN, y0))
    eb = text_img("CRM DE VENDAS E MARKETING", font("SemiBold", 22), MUTED, tracking=3)
    c.alpha_composite(eb, (W - MARGIN - eb.width, y0 + 10))
    d.line([(MARGIN, y0 + 78), (W - MARGIN, y0 + 78)], fill=(255, 255, 255, 46), width=2)

    # foto da cliente frustrada + duas notificações que se contradizem
    pw, ph = W - 2 * MARGIN, 700
    py = y0 + 118
    photo = rounded_photo(grade(Image.open(PHOTO).convert("RGB")), pw, ph, 44, centering=(0.5, 0.42))
    c.alpha_composite(photo, (MARGIN, py))
    n1 = notification("Atendimento", "Recebemos sua reclamação.", "seg 09:12")
    n2 = notification("Comercial", "Sua proposta de renovação chegou!", "ter 10:40")
    c.alpha_composite(n1, (MARGIN - 30, py + 300))
    c.alpha_composite(n2, (W - MARGIN - n2.width + 30, py + ph - n2.height - 50))

    # título-equação
    f = font("Bold", 92)
    y = py + ph + 50
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
    ap.parse_args()
    out = os.path.join(ROOT, "output", "BEENO-REEL01-capa.png")
    build(out)
    print("->", out)


if __name__ == "__main__":
    main()
