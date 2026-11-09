"""Biblioteca de efeitos sonoros sintetizados do zero (sem samples de terceiros).

Uso: python3 gerar_sfx.py   (grava os .wav nesta pasta, 48 kHz estéreo)
"""

from pathlib import Path

import numpy as np

SR = 48000
AQUI = Path(__file__).parent
rng = np.random.default_rng(11)


def t_(d):
    return np.arange(int(d * SR)) / SR


def ruido(d):
    return rng.standard_normal(int(d * SR))


def filtro_banda(x, f_lo, f_hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < f_lo) | (f > f_hi)] = 0
    return np.fft.irfft(X, len(x))


def varredura(x, f0, f1, q=0.35):
    """Passa-banda que varre de f0 a f1 (STFT simples por blocos)."""
    n, blk = len(x), 1024
    out = np.zeros(n)
    janela = np.hanning(blk * 2)
    for i in range(0, n - blk, blk):
        seg = x[i : i + blk * 2]
        if len(seg) < blk * 2:
            seg = np.pad(seg, (0, blk * 2 - len(seg)))
        p = i / n
        fc = f0 * (f1 / f0) ** p
        X = np.fft.rfft(seg * janela)
        f = np.fft.rfftfreq(blk * 2, 1 / SR)
        X *= np.exp(-((np.log(f + 1) - np.log(fc)) ** 2) / (2 * q ** 2))
        y = np.fft.irfft(X, blk * 2)
        out[i : i + blk * 2] += y[: min(blk * 2, n - i)]
    return out


def reverb(x, tempo=0.6, mix=0.25):
    n = int(tempo * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * (6.9 / tempo))
    ir = filtro_banda(ir, 200, 7000)
    y = np.convolve(x, ir)
    base = np.pad(x, (0, len(y) - len(x)))
    return base * (1 - mix) + y * mix / (np.max(np.abs(y)) + 1e-9) * np.max(np.abs(x))


def norm(x, pico=0.9):
    return x / (np.max(np.abs(x)) + 1e-9) * pico


def fades(x, a=0.002, r=0.02):
    n = len(x)
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[n - nr :] = np.linspace(1, 0, nr)
    return x * e


def salvar(nome, x, largura=0.0):
    x = fades(norm(x))
    esq, dir_ = x, x
    if largura:
        atraso = int(largura * SR)
        dir_ = np.concatenate([np.zeros(atraso), x[:-atraso]])
    est = np.stack([esq, dir_], axis=1)
    pcm = (np.clip(est, -1, 1) * 32767).astype('<i2')
    import wave

    with wave.open(str(AQUI / f'{nome}.wav'), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(nome, f'{len(x) / SR:.2f}s')


def whoosh(d=0.55, f0=300, f1=5000, pico=0.6):
    t = t_(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    env *= np.exp(-((t / d - pico) ** 2) / 0.08)
    return varredura(ruido(d), f0, f1) * env


def pop():
    t = t_(0.12)
    f = 520 * np.exp(-t * 25) + 180
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38)
    clique = filtro_banda(ruido(0.12), 2000, 9000) * np.exp(-t * 400) * 0.4
    return s + clique


def clique():
    t = t_(0.09)
    a = filtro_banda(ruido(0.09), 1500, 8000) * np.exp(-t * 650)
    b = np.zeros_like(a)
    k = int(0.045 * SR)
    b[k:] = a[: len(a) - k] * 0.55  # o "soltar" do botão
    corpo = np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 300) * 0.3
    return a + b + corpo


def notificacao():
    t = t_(0.7)
    s = np.zeros_like(t)
    for ini, f in ((0.0, 1318.5), (0.11, 1760.0)):
        tt = np.clip(t - ini, 0, None)
        on = (t >= ini).astype(float)
        s += on * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 7)
    return reverb(s, 0.4, 0.2)


def impacto():
    d = 1.6
    t = t_(d)
    f = 30 + 90 * np.exp(-t * 14)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    estalo = filtro_banda(ruido(d), 80, 3000) * np.exp(-t * 30) * 0.8
    cauda = filtro_banda(ruido(d), 60, 600) * np.exp(-t * 4) * 0.25
    return reverb(np.tanh(1.8 * (sub + estalo + cauda)), 1.0, 0.3)


def riser(d=1.4):
    t = t_(d)
    s = varredura(ruido(d), 200, 9000, q=0.5) * (t / d) ** 2
    f = 180 * (8 ** (t / d))
    tom = np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 3 * 0.25
    return s + tom


def flash():
    """Estalo de câmera + brilho, para o flash branco."""
    t = t_(0.5)
    estalo = filtro_banda(ruido(0.5), 2500, 12000) * np.exp(-t * 90)
    brilho = varredura(ruido(0.5), 6000, 12000, q=0.3) * np.exp(-t * 9) * 0.5
    return reverb(estalo + brilho, 0.5, 0.25)


def deslizar():
    return whoosh(0.35, 900, 3500, 0.45)


def tick():
    t = t_(0.05)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 180) + filtro_banda(ruido(0.05), 4000, 10000) * np.exp(-t * 500) * 0.3


def erro():
    t = t_(0.45)
    s = np.zeros_like(t)
    for ini in (0.0, 0.16):
        tt = np.clip(t - ini, 0, None)
        on = ((t >= ini) & (t < ini + 0.13)).astype(float)
        s += on * np.sign(np.sin(2 * np.pi * 220 * tt)) * 0.4 * np.exp(-tt * 6)
    return filtro_banda(s, 100, 3000)


if __name__ == '__main__':
    salvar('whoosh', whoosh(), 0.01)
    salvar('whoosh_curto', whoosh(0.3, 600, 6000, 0.5), 0.008)
    salvar('pop', pop())
    salvar('clique', clique())
    salvar('notificacao', notificacao())
    salvar('impacto', impacto(), 0.012)
    salvar('riser', riser(), 0.01)
    salvar('flash', flash(), 0.01)
    salvar('deslizar', deslizar(), 0.006)
    salvar('tick', tick())
    salvar('erro', erro())
