#!/bin/bash
# Mixa a trilha de fundo num render do Remotion (voz + efeitos) e normaliza em −14 LUFS.
# Uso: bash mixar.sh <render.mp4> <trilha.mp3> <início da trilha em s> <ganho da trilha em dB> <saída.mp4>
# A trilha fica ~13 dB abaixo da voz e abaixa mais 4–6 dB enquanto ele fala (sidechain), com um vale em 2,5 kHz
# para a voz ficar limpa. Fade de entrada curto e fade de saída de 1,2 s no fim do vídeo.
set -e
VIDEO="$1"; TRILHA="$2"; INICIO="$3"; GANHO="$4"; SAIDA="$5"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
FIM=$(awk -v d="$DUR" 'BEGIN{print d-1.2}')
TMP="${SAIDA%.mp4}.tmp.mp4"
ffmpeg -v error -y -i "$VIDEO" -ss "$INICIO" -t "$DUR" -i "$TRILHA" -filter_complex "\
[1:a]aresample=48000,volume=${GANHO}dB,equalizer=f=2500:t=q:w=1.2:g=-3,afade=t=in:d=0.12,afade=t=out:st=${FIM}:d=1.2[m];\
[0:a]aresample=48000,asplit=2[voz][chave];\
[m][chave]sidechaincompress=threshold=0.04:ratio=4:attack=15:release=350:makeup=1[md];\
[voz][md]amix=inputs=2:duration=first:normalize=0[mix]" \
  -map 0:v -map "[mix]" -c:v copy -c:a pcm_s16le "$TMP"
# Normalização em duas passadas (−14 LUFS, pico −1 dBTP).
M=$(ffmpeg -nostats -i "$TMP" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$M" | grep "\"$1\"" | grep -oE '[-0-9.]+'; }
ffmpeg -v error -y -i "$TMP" -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -movflags +faststart "$SAIDA"
rm -f "$TMP"
