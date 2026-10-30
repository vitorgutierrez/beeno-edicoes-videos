# Beeno — edições de reels

Reels do Beeno editados com a mesma linguagem dos ADs da RVOPS (ADS 05), com a identidade visual do [beeno.ai](https://beeno.ai).

## Entregas (`output/`)

| Arquivo | Bruto (Drive "Vídeos gravados") | Duração |
|---|---|---|
| `BEENO-REEL01-atendimento-vendas.mp4` | Teleprompter-2026-06-10_15-50-07.mp4 | 38s |
| `BEENO-REEL02-registro-automatico.mp4` | Teleprompter-2026-06-10_15-56-43.mp4 | 36s |

1080x1920, 30fps, H.264 + AAC, -14 LUFS (padrão Reels).

Capa do reel 01: `output/BEENO-REEL01-capa.png` (1080x1920, conteúdo dentro do recorte 3:4 do grid),
gerada por `python3 editor/cover.py --src /caminho/Teleprompter-2026-06-10_15-50-07.mp4`.

## Conceito (v5, após feedback)

Linguagem sóbria/documental dos ADs da RVOPS:

- Cortes secos em toda pausa acima de 0,2s; bordas de cada corte ajustadas pela energia do
  áudio para não comer palavras. Começa na primeira palavra, termina logo após a última
  (`END_MAX` corta antes de ele levar a mão à câmera no reel 01). Velocidade 1.1x
- Enquadramento fixo; troca entre aberto/fechado só em corte seco no fim de frase (sem zoom animado)
- Trocas de cena: corte com uma "assentada" de 4% em 0,2s + clique de mouse (Mixkit)
- Nada de transparência em texto: legendas, títulos, cards e chips sempre sólidos
- Frases que viram título não se repetem na legenda
- Poucos splits, cada um com tempo de leitura; painel com o quadro desfocado e escurecido
- Trilha enviada pelo cliente (`assets/music/`, fora do git), com a batida cheia entrando
  quando termina o gancho; ducking sob a voz

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
- Trilha e clique de transição: `editor/music.py`. Coloque as trilhas em `assets/music/` (nomes em `MUSIC` de cada reel); o clique é baixado do Mixkit na primeira execução
- Transcrições com tempo por palavra: `transcripts/`
