# Componentes Remotion da Beeno

Peças prontas para montar os reels da Beeno no [Remotion](https://www.remotion.dev) (vídeo em React),
como alternativa ao editor em Python de `editor/`. Foram usadas nas primeiras versões dos dois reels
gravados no teleprompter (as mesmas falas de `output/BEENO-REEL01` e `REEL02`).

| Pasta | O que tem |
|---|---|
| `_beeno/tema.ts` | Cores, fonte (Poppins), easing, `criarGatilhos` (acha o tempo de uma palavra no `palavras.json`) |
| `_beeno/estilo.tsx` | O estilo dos 11 criativos de referência: `CameraBeeno` (punch-in por plano), `LegendaBeeno` (palavra a palavra), `SplitBroll`, `PaineisCor`, `FlashBranco`, `LogoEntrada`, `LinhaChave`, `ListaX`, `XDesenhado`, `FundoDark`, `BlocoDark`, `CardVidro`, `TituloDark`, `ListaCheck` |
| `_beeno/componentes.tsx` | Peças dos reels: `CameraEPainel` (tela dividida), `Legendas`, `TopoPalavras`, `Chip`, `Broll`, `PrintZoom`, `Caixa`, `Seta`, `Logo`, `CartelaFinal`, `Sons`, `ImpactoTela`, `Flash`, `LuzVazada`, `Slam`, `PilhaEtiquetas`, `Cursor` |
| `_shared/synchronized-split.tsx` | Tela dividida sincronizada (câmera e painel andam juntos, sem buraco) |
| `_shared/faixa-publico.tsx` | Faixa fina de público no topo + chamada no gancho, nas cores da Beeno |
| `beeno-uma-empresa/`, `beeno-melhor-registro/` | Os dois reels montados com essas peças |
| `transcricao/` | `palavras.json` (tempo de cada palavra) das duas falas, já sem as pausas |

## Como usar num projeto Remotion

1. `npx create-video@latest` e copie esta pasta para `src/`.
2. Ponha o vídeo bruto em `public/<PROJETO>/video/` (o nome da pasta está em `PROJETO`, em `_beeno/tema.ts`).
3. Registre as composições no `Root.tsx` (1080×1920, 30 fps, duração = duração do vídeo).
4. `npx remotion studio` para ver; `npx remotion render` para exportar.

Antes de mexer, leia [guia-edicao/README.md](../guia-edicao/README.md): ali está o que mudou depois do
feedback da v5 (edição mais calma, sem transparência em texto, menos splits).
