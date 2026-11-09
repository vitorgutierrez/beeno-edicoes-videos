"""Rastreia o rosto no vídeo tratado (2160x3840) a cada 0,1 s e grava a posição suavizada.

Uso: python -I rastrear_rosto.py <tratado.mp4> <saida.json>
Saída: [[t, cx, cy, largura], ...] em pixels do vídeo tratado.
"""
import json
import sys

import cv2
import numpy as np

fonte, saida = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(fonte)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
W = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cascata = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
ESC = 0.25  # detecta em 540x960
passo = 3
amostras = []
i = 0
while True:
    ok = cap.grab()
    if not ok:
        break
    if i % passo == 0:
        ok, quadro = cap.retrieve()
        if not ok:
            break
        p = cv2.cvtColor(cv2.resize(quadro, None, fx=ESC, fy=ESC), cv2.COLOR_BGR2GRAY)
        rostos = cascata.detectMultiScale(p, scaleFactor=1.1, minNeighbors=6, minSize=(70, 70))
        t = i / fps
        if len(rostos):
            x, y, w, h = max(rostos, key=lambda r: r[2] * r[3])
            amostras.append([t, (x + w / 2) / ESC, (y + h / 2) / ESC, w / ESC])
        else:
            amostras.append([t, None, None, None])
    i += 1

ts = np.array([a[0] for a in amostras])
saidas = []
for k in (1, 2, 3):
    v = np.array([np.nan if a[k] is None else a[k] for a in amostras], dtype=float)
    boas = ~np.isnan(v)
    v = np.interp(ts, ts[boas], v[boas])
    # mediana curta (tira saltos de detecção errada) + média móvel de ~0,9 s
    med = np.array([np.median(v[max(0, j - 2): j + 3]) for j in range(len(v))])
    ker = np.ones(9) / 9
    suave = np.convolve(np.pad(med, 4, mode="edge"), ker, mode="valid")
    saidas.append(suave)
    print(f"coluna {k}: {boas.mean() * 100:.0f}% detectado")

res = [[round(float(t), 2), round(float(a)), round(float(b)), round(float(c))] for t, a, b, c in zip(ts, *saidas)]
json.dump(res, open(saida, "w"))
print(len(res), "amostras; largura do vídeo", W)
