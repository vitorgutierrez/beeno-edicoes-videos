#!/bin/sh
# Masterização do áudio do render (guia-edicao/1-estilo-beeno.md, seção 10): -15 LUFS integrado, pico -1 dBTP.
# Duas passadas de loudnorm (mede, depois aplica linear). O vídeo é copiado sem recompressão.
# Uso: sh masterizar.sh entrada.mp4 saida.mp4
set -e
MED=$(ffmpeg -hide_banner -i "$1" -vn -af loudnorm=I=-15:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
v() { echo "$MED" | sed -n "s/.*\"$1\" : \"\(.*\)\".*/\1/p"; }
ffmpeg -v error -y -i "$1" -c:v copy \
  -af "loudnorm=I=-15:TP=-1:LRA=11:measured_I=$(v input_i):measured_TP=$(v input_tp):measured_LRA=$(v input_lra):measured_thresh=$(v input_thresh):offset=$(v target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -shortest -movflags +faststart "$2"
