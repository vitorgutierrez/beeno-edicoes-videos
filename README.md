# Beeno — edições de reels

Reels do Beeno editados com a mesma linguagem dos ADs da RVOPS (ADS 05), com a identidade visual do [beeno.ai](https://beeno.ai).

## Entregas (`output/`)

| Arquivo | Bruto (Drive "Vídeos gravados") | Duração |
|---|---|---|
| `BEENO-REEL01-atendimento-vendas-1.2x.mp4` | Teleprompter-2026-06-10_15-50-07.mp4 | 34s |
| `BEENO-REEL02-registro-automatico-1.2x.mp4` | Teleprompter-2026-06-10_15-56-43.mp4 | 33s |

1080x1920, 30fps, H.264 + AAC, -14 LUFS (padrão Reels).

## O que foi aplicado da referência RVOPS

- Pílula fixa no topo com chamada de público (verde no lugar do laranja)
- Linha de progresso com 3 pontos (capítulos do roteiro)
- Split-screen: motion graphic em cima, apresentador embaixo, divisória verde
- Legenda palavra a palavra com palavras-chave destacadas (pílula branca na divisória / pílula tinta em tela cheia)
- Gancho com caixas empilhadas, carimbos ("SEGUNDA", "TERÇA", "DESORGANIZADA", "VAI FALHAR"), chips de impacto, títulos grandes revelados no ritmo da fala
- Card de marca e CTA final com botão
- Cortes secos nas pausas, zoom alternado nos cortes e velocidade 1.2x
- Trilha + whoosh/pop/impacto com ducking sob a voz

## Identidade Beeno

Verde `#00CD8A` / `#00A973`, tinta `#0A1C15`, fonte Poppins, fundos em gradiente tinta com grid e brilho verde (como o hero do site), logo oficial `beeno by skeps`.

## Como regerar

```bash
pip install faster-whisper fonttools brotli pillow numpy
python3 editor/build.py reel01 --src /caminho/Teleprompter-2026-06-10_15-50-07.mp4
python3 editor/build.py reel02 --src /caminho/Teleprompter-2026-06-10_15-56-43.mp4
```

`--preview 1.5,8.0,20` gera só alguns quadros para conferência.

- Roteiro/storyboard de cada reel: `editor/reels/reel0X.py` (textos, tempos, correções da transcrição, palavras-chave, banner)
- Cenas de motion graphics: `editor/scenes.py`; primitivas visuais: `editor/mg.py`
- Trilha original sintetizada (sem direitos de terceiros): `editor/music.py`
- Transcrições com tempo por palavra: `transcripts/`
