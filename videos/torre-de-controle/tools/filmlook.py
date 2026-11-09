"""Emulação de película para tirar o "brilho de IA" dos quadros: contraste mais baixo, pretos levantados,
saturação contida, halation (vermelho em volta das luzes), leve suavidade de lente, aberração cromática nas
bordas, vinheta e grão de filme. Uso: python3 filmlook.py entrada.png saida.png [--seed N]"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def filmlook(im, seed=0, grain=0.028):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), np.float32) / 255
    h, w, _ = a.shape
    # lente: perde um pouco de nitidez fina
    soft = np.asarray(im.convert('RGB').filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    a = a * 0.65 + soft * 0.35
    # halation: luzes fortes vazam em vermelho/laranja
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    hi = np.clip((lum - 0.72) / 0.28, 0, 1)
    hal = Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(w, h) / 120))
    hal = np.asarray(hal, np.float32)[..., None] / 255
    a = a + hal * np.array([0.28, 0.09, 0.03], np.float32)
    # curva: pretos levantados, altas suaves, contraste menor
    a = 0.022 + a * 0.955
    a = a - 0.06 * (a - 0.5) ** 3 * 4
    # saturação contida
    g = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    a = g + (a - g) * 0.9
    # aberração cromática leve nas bordas
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    shift = (r ** 2 * 1.6).astype(np.float32)
    xr = np.clip(xx + shift * (xx - w / 2) / (w / 2 + 1e-6), 0, w - 1).astype(int)
    a[..., 0] = a[yy.astype(int), xr, 0]
    # vinheta
    a = a * (1 - 0.22 * np.clip(r - 0.35, 0, 1) ** 1.5)[..., None]
    # grão (mais visível nos médios), com tamanho de grão ~1.4px
    n = rng.normal(0, 1, (h // 2 + 1, w // 2 + 1)).astype(np.float32)
    n = np.asarray(Image.fromarray(n).resize((w, h), Image.BICUBIC), np.float32)[:h, :w]
    lum = (a @ np.array([0.299, 0.587, 0.114], np.float32))
    a = a + (n * grain * (0.35 + 1.3 * lum * (1 - lum)))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


if __name__ == '__main__':
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 0
    filmlook(Image.open(sys.argv[1]), seed).save(sys.argv[2])
