"""Capa do reel 01 — "Departamentos separados = cliente frustrado".

Segue o template das capas que o Beeno já posta: fundo quase preto com brilho verde
no alto, traço verde curto acima do título, título alinhado à esquerda (primeira parte
em peso leve, o resto em negrito, palavra-chave em verde) e o "b" da marca bem sutil
no canto inferior direito, cortado pela borda. Sem imagens.

Todo o conteúdo fica dentro do recorte 3:4 (1080x1440) que o Instagram mostra no grid.

Uso: python3 editor/cover.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from mg import BRAND, GREEN, ROOT

W, H = 1080, 1920
GRID_TOP = (H - 1440) // 2  # 240: topo do recorte 3:4 do grid
MARGIN = 72
BG = (11, 17, 15)
INTER = "/usr/share/fonts/opentype/inter"

# (texto, peso, cor) — uma linha por item
LINES = [
    ("Departamentos", "Light", (236, 240, 238)),
    ("separados", "Light", (236, 240, 238)),
    ("= cliente", "Bold", (255, 255, 255)),
    ("frustrado.", "Bold", GREEN),
]
SIZE = 112


def font(weight):
    return ImageFont.truetype(os.path.join(INTER, f"InterDisplay-{weight}.otf"), SIZE)


def background():
    bg = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse([260, GRID_TOP - 120, 1180, GRID_TOP + 640], fill=(0, 92, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(190))
    return Image.fromarray(np.clip(np.asarray(bg, np.int16) + np.asarray(glow, np.int16) * 0.4, 0, 255)
                           .astype(np.uint8))


def b_mark(height):
    """O 'b' do ícone da marca, como máscara (o canal R separa o branco do verde)."""
    icon = Image.open(os.path.join(BRAND, "beeno-icon.png")).convert("RGB")
    mask = icon.getchannel("R").crop((269, 178, 832, 923))
    return mask.resize((int(mask.width * height / mask.height), height), Image.LANCZOS)


def build(out_png):
    c = background()
    d = ImageDraw.Draw(c)

    # 'b' marca-d'água no canto inferior direito, cortado pela borda do recorte
    mark = b_mark(560)
    layer = Image.new("RGB", mark.size, (24, 31, 29))
    c.paste(layer, (W - mark.width + 40, GRID_TOP + 1440 - 400), mark)

    # título: traço verde + linhas alinhadas à esquerda, centradas na vertical do recorte
    lh = int(SIZE * 1.12)
    block = 28 + 60 + lh * len(LINES)
    y = GRID_TOP + (1440 - block) // 2 - 40
    d.rectangle([MARGIN, y, MARGIN + 96, y + 7], fill=GREEN)
    y += 60
    for txt, weight, col in LINES:
        f = font(weight)
        x = MARGIN
        for ch in txt:  # leve aperto entre letras, como nas capas do perfil
            d.text((x, y), ch, font=f, fill=col)
            x += f.getlength(ch) - SIZE * 0.012
        y += lh

    c.save(out_png, quality=95)
    return out_png


def main():
    out = os.path.join(ROOT, "output", "BEENO-REEL01-capa.png")
    build(out)
    print("->", out)


if __name__ == "__main__":
    main()
