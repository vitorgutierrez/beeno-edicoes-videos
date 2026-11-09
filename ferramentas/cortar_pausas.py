"""Gera uma CÓPIA do vídeo sem as pausas longas (o original não é tocado), pedido explícito da pessoa.

Uso:
    python3 cortar_pausas.py <original.mp4> <palavras.json do original> <saida.mp4> <pasta palavras novas> [inicio_fixo_s]

- Pausas >= 0,4 s (silêncio abaixo de -30 dB) ficam com 0,1 s de respiro de cada lado.
- Início: corta até 0,1 s antes da primeira fala (ou em `inicio_fixo_s`, se informado).
- Final: mantém 0,35 s depois da última fala (sem a espera olhando para a câmera).
- Grava palavras.json com os tempos remapeados e cortes.json (cortes no tempo original e no novo).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

LIMIAR_DB = -30
PAUSA_MIN = 0.4
RESPIRO = 0.1
CAUDA = 0.35


def duracao(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                capture_output=True, text=True, check=True).stdout)


def silencios(f):
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-vn', '-af', f'silencedetect=n={LIMIAR_DB}dB:d=0.05', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', log)]
    fim = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', log)]
    pares = list(zip(ini, fim + [duracao(f)] * (len(ini) - len(fim))))
    juntos = []
    for a, b in pares:  # junta silêncios separados por menos de 80 ms (respiros, estalos)
        if juntos and a - juntos[-1][1] < 0.08:
            juntos[-1] = (juntos[-1][0], b)
        else:
            juntos.append((a, b))
    return juntos


def main():
    original, palavras_json, saida, pasta, *resto = sys.argv[1:]
    inicio_fixo = float(resto[0]) if resto else None
    total = duracao(original)
    sil = silencios(original)
    cortes = []
    # início
    if inicio_fixo is not None:
        cortes.append((0.0, inicio_fixo))
    elif sil and sil[0][0] <= 0.01:
        cortes.append((0.0, max(0.0, sil[0][1] - RESPIRO)))
    # pausas do meio
    for a, b in sil:
        if a <= 0.01 or b >= total - 0.01:
            continue
        if cortes and a < cortes[0][1]:
            continue
        if b - a >= PAUSA_MIN:
            cortes.append((a + RESPIRO, b - RESPIRO))
    # final
    ultimo = sil[-1] if sil and sil[-1][1] >= total - 0.05 else None
    if ultimo and total - ultimo[0] > CAUDA:
        cortes.append((ultimo[0] + CAUDA, total))
    cortes.sort()

    manter, t = [], 0.0
    for a, b in cortes:
        if a > t:
            manter.append((t, a))
        t = max(t, b)
    if t < total:
        manter.append((t, total))

    filtros, rotulos = [], []
    for i, (a, b) in enumerate(manter):
        filtros.append(f'[0:v]trim={a:.4f}:{b:.4f},setpts=PTS-STARTPTS[v{i}]')
        filtros.append(f'[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, b - a - 0.012):.4f}:d=0.012[a{i}]')
        rotulos.append(f'[v{i}][a{i}]')
    filtros.append(''.join(rotulos) + f'concat=n={len(manter)}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', original, '-filter_complex', ';'.join(filtros), '-map', '[v]', '-map', '[a]',
                    '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', saida], check=True)

    def novo(t):
        removido = 0.0
        for a, b in cortes:
            if t >= b:
                removido += b - a
            elif t > a:
                return round(a - removido, 3)
        return round(t - removido, 3)

    palavras = json.load(open(palavras_json, encoding='utf-8'))
    novas = [dict(p, s=novo(p['s']), e=novo(p['e'])) for p in palavras]
    Path(pasta).mkdir(parents=True, exist_ok=True)
    json.dump(novas, open(Path(pasta) / 'palavras.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    pontos = []
    acc = 0.0
    for a, b in manter[:-1]:
        acc += b - a
        pontos.append(round(acc, 3))
    json.dump({'cortes_no_original': [[round(a, 3), round(b, 3)] for a, b in cortes], 'pontos_de_corte_no_novo': pontos},
              open(Path(pasta) / 'cortes.json', 'w', encoding='utf-8'), indent=1)
    print(saida, f'{duracao(saida):.3f}s (original {total:.3f}s), {len(cortes)} cortes, {sum(b - a for a, b in cortes):.2f}s removidos')


if __name__ == '__main__':
    main()
