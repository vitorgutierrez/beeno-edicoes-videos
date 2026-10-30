# Beeno — edições de reels

Reels do Beeno editados com a mesma linguagem dos ADs da RVOPS (ADS 05), com a identidade visual do [beeno.ai](https://beeno.ai).

## Entregas (`output/`)

| Arquivo | Bruto (Drive "Vídeos gravados") | Duração |
|---|---|---|
| `BEENO-REEL01-atendimento-vendas-1.2x.mp4` | Teleprompter-2026-06-10_15-50-07.mp4 | 34s |
| `BEENO-REEL02-registro-automatico-1.2x.mp4` | Teleprompter-2026-06-10_15-56-43.mp4 | 33s |

1080x1920, 30fps, H.264 + AAC, -14 LUFS (padrão Reels).

## Conceito (v2, após feedback)

Linguagem sóbria/documental dos ADs da RVOPS, sem "gamificação":

- Sem faixa de público nem linha de progresso no topo
- Cortes secos entre tela cheia e split-screen (sem cortina/slide)
- Elementos entram só com fade + leve subida; sem pops, carimbos ou escala com rebote
- Painel superior com o próprio quadro desfocado e escurecido; linhas finas, celulares abstratos,
  partículas que convergem para a marca, chips discretos
- Legenda palavra a palavra (pílula branca na divisória / pílula escura em tela cheia)
- Títulos em caixa-alta revelados no ritmo da fala; CTA com seta para o botão do anúncio
- Tratamento de cor mais sóbrio no apresentador
- Trilha ambiente (pad sustentado, sem batida) com ducking sob a voz; sem efeitos sonoros
- Cortes secos nas pausas e velocidade 1.2x

## Identidade Beeno

Verde `#00CD8A` (só como acento), tinta `#0A1C15`, fonte Poppins, logo oficial `beeno by skeps`.

## Como regerar

```bash
pip install faster-whisper fonttools brotli pillow numpy
python3 editor/build.py reel01 --src /caminho/Teleprompter-2026-06-10_15-50-07.mp4
python3 editor/build.py reel02 --src /caminho/Teleprompter-2026-06-10_15-56-43.mp4
```

`--preview 1.5,8.0,20` gera só alguns quadros para conferência.

- Roteiro/storyboard de cada reel: `editor/reels/reel0X.py` (textos, tempos, correções da transcrição, palavras-chave)
- Cenas de motion graphics: `editor/scenes.py`; primitivas visuais: `editor/mg.py`
- Trilha ambiente original sintetizada (sem direitos de terceiros): `editor/music.py`
- Transcrições com tempo por palavra: `transcripts/`
