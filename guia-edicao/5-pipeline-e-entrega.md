# Pipeline e entrega

## Do bruto ao vídeo pronto
1. **Transcrever** com tempo por palavra: `python ferramentas/transcrever.py <bruto.mp4> <pasta>` → `palavras.json` (faster-whisper, roda no computador). Corrija marca e nomes.
2. **Preparar o bruto** (opcional): `bash ferramentas/preparar_bruto.sh <bruto.mp4> <pasta>` → voz limpa e imagem estabilizada. O bruto nunca é alterado.
3. **Tirar pausas** (só com pedido): `python ferramentas/cortar_pausas.py …` gera uma **cópia** sem as pausas e remapeia o `palavras.json`.
4. **Planejar** (`plano.md`): uma linha por frase com cena, escala, texto, som. Aprovar antes de programar. Exemplos em [exemplos/](exemplos/).
5. **Montar** em uma das três bases:
   - `editor/` (Python, usado nos reels 01 e 02, versão v5);
   - `remotion/` (React, componentes do estilo Beeno);
   - `motion-html/` (inserções em HTML renderizadas por Chrome, para usar no CapCut).
6. **Stills de revisão** de cada cena/transição → ok → render.
7. **Som:** trilha com `ferramentas/mixar.sh` (ou `compor_trilha.py` para uma trilha sintetizada sem direitos de terceiros), efeitos de `gerar_sfx.py`, masterização com `masterizar.sh`.
8. Conferir o [checklist de revisão](3-revisao.md).

## Formatos
- Vídeo: 1080×1920, 30 fps, H.264 (CRF 17–18), AAC 256 kbps, −14 LUFS.
- Inserções HTML: 60 fps, em três arquivos: MP4 com fundo escuro, ProRes 4444 com alfa (CapCut) e WebM VP9 com alfa.
- Thumbnail YouTube: 1280×720, < 2 MB. Capa de reel: 1080×1920 com o conteúdo dentro do recorte 3:4 do grid.

## Versões e nomes
- Anúncio: `BEENO_C<criativo>_H<gancho>_<IDEIA>` (ex.: `BEENO_C2_H1_PLANILHA`).
- Reel: `BEENO-REEL03-<tema>.mp4`, capa `BEENO-REEL03-capa.png`.
- Versão nova = arquivo novo com sufixo (`_v2`, `_sem-trilha`); os anteriores ficam.
- **Versão acelerada** (1,1–1,3×) só quando pedirem, como arquivo à parte.

## Entrega
- Uma pasta por peça (ou episódio) com o vídeo, o texto da publicação (`.txt`/`legenda.md`) e a capa.
- Uma peça por vez, esperando aprovação antes da próxima.
- Vídeos brutos e arquivos de trabalho (ProRes, quadros) **não vão para o git** (ficam no Drive); o git guarda o roteiro, o código, as transcrições e só as entregas finais leves em `output/`.
