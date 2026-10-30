# Beeno — edições de reels

Reels do Beeno editados com a mesma linguagem dos ADs da RVOPS (ADS 05), com a identidade visual do [beeno.ai](https://beeno.ai).

## Entregas (`output/`)

| Arquivo | Bruto (Drive "Vídeos gravados") | Duração |
|---|---|---|
| `BEENO-REEL01-atendimento-vendas.mp4` | Teleprompter-2026-06-10_15-50-07.mp4 | 40s |
| `BEENO-REEL02-registro-automatico.mp4` | Teleprompter-2026-06-10_15-56-43.mp4 | 38s |

1080x1920, 30fps, H.264 + AAC, -14 LUFS (padrão Reels).

## Conceito (v4, após feedback)

Linguagem sóbria/documental dos ADs da RVOPS, pensada para ser vista sem cansar:

- Ritmo natural: velocidade 1.1x e só as pausas longas são cortadas; as bordas de cada corte
  são ajustadas pela energia do áudio para nunca comer o começo/fim de uma palavra
- Poucos splits, cada um com tempo de leitura; animações com entradas lentas (fade + leve subida)
- Enquadramento estável: push-in quase imperceptível e no máximo um punch-in suave por bloco
  de tela cheia, que se mantém (sem aproximar e voltar)
- Transições: zoom leve com desfoque entre tela cheia e split, dissolve entre gráficos e entre
  títulos; clique de mouse (Mixkit) nas trocas de cena
- Painel superior com o próprio quadro desfocado e escurecido; linhas finas, celulares abstratos,
  partículas, chips discretos
- Legenda palavra a palavra em pílula sólida (branca na divisória / escura em tela cheia)
- Títulos em caixa-alta revelados no ritmo da fala; CTA com seta para o botão do anúncio
- Trilha "Minimal Emotion" (Mixkit, licença gratuita para redes sociais e anúncios, sem atribuição),
  com a parte cheia entrando no fechamento, ducking sob a voz

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
- Trilha e clique de transição: `editor/music.py` (baixados do Mixkit na primeira execução)
- Transcrições com tempo por palavra: `transcripts/`
