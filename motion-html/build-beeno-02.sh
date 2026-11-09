#!/bin/bash
set -e
BASE="beeno-blip-do-canal-ao-pipeline-1080x1920"
OUT="${OUT:-$(pwd)/saida}"; mkdir -p "$OUT"
echo "== render dark =="
node render-beeno-02.js dark frames_b02_dark
echo "== render alpha =="
node render-beeno-02.js alpha frames_b02_alpha
echo "== encode mp4 (fundo escuro) =="
ffmpeg -y -loglevel error -framerate 60 -i frames_b02_dark/f%05d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 17 -preset slow -movflags +faststart \
  "$OUT/$BASE-fundo-escuro.mp4"
echo "== encode mov prores 4444 (alpha) =="
ffmpeg -y -loglevel error -framerate 60 -i frames_b02_alpha/f%05d.png \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -alpha_bits 16 -vendor apl0 \
  "$OUT/$BASE-alpha-prores4444.mov"
echo "== encode webm (alpha) =="
ffmpeg -y -loglevel error -framerate 60 -i frames_b02_alpha/f%05d.png \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -row-mt 1 \
  "$OUT/$BASE-alpha.webm"
echo "== pronto =="
ls -la "$OUT/$BASE"*
