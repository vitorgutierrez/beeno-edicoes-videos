#!/usr/bin/env bash
# Prepara intermediários a partir do vídeo bruto (o bruto nunca é alterado):
#   1) voz limpa: RNNoise + graves cortados + presença + compressão leve  -> <pasta>/voz-limpa.wav
#   2) imagem estabilizada (vidstab) + nitidez leve + cor opcional        -> <pasta>/tratado.mp4
# Uso: bash preparar_bruto.sh <bruto.mp4> <pasta de saída> [filtro de cor do ffmpeg] [--so-voz]
# O modelo do RNNoise (arquivo .rnnn, ex.: "rn.rnnn" do projeto GregorR/rnnoise-models) fica em ferramentas/
# ou é indicado em RNNN=/caminho/modelo.rnnn. Em evento muito barulhento, o DeepFilterNet 3 limpa mais.
set -euo pipefail
BRUTO="$1"; OUT="$2"; COR="${3:-null}"; SO_VOZ="${4:-}"
RNNN="${RNNN:-$(dirname "$0")/rn.rnnn}"
mkdir -p "$OUT"

ffmpeg -v error -y -i "$BRUTO" -vn -ac 1 -ar 48000 \
  -af "highpass=f=90,arnndn=m='$RNNN':mix=0.85,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2" \
  "$OUT/voz-limpa.wav"
echo "voz: $OUT/voz-limpa.wav"
[[ "$SO_VOZ" == "--so-voz" ]] && exit 0

TRF="$OUT/transf.trf"
ffmpeg -v error -y -i "$BRUTO" -vf "vidstabdetect=shakiness=5:accuracy=12:result='$TRF'" -f null -
ffmpeg -v error -y -i "$BRUTO" \
  -vf "vidstabtransform=input='$TRF':smoothing=25:zoom=4:optzoom=0:interpol=bicubic,unsharp=5:5:0.4,${COR},format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 15 -g 15 "$OUT/tratado.mp4"
echo "imagem: $OUT/tratado.mp4"
