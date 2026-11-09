# Plano: teste comparativo Remotion × HyperFrames

Status: **aprovado em 14/10/2026; montado e renderizado nas duas ferramentas** (`edicoes/001. beeno-video/comparativo/`). Ajustes feitos durante a montagem: legenda oculta na cena 3 (o próprio "CRM integrado" faz o papel dela); prints com zoom de leitura (~1,9×) e moldura de 1040 × 740; logo com transparência de `hf/logo_beeno_lockup_escuro.png`.

## Objetivo

Editar **o mesmo trecho** do Vídeo A ("Uma empresa só") nas duas ferramentas, com a mesma especificação de cenas, e comparar o resultado: qualidade visual, sincronia com a fala, esforço de montagem, tempo de render e facilidade de ajuste.

**Custo:** zero créditos da Higgsfield. Nada de B-roll gerado, voz gerada, música gerada nem render na nuvem da HeyGen. Só prints, logo e efeitos sonoros que já estão na pasta, com render local nas duas ferramentas.

## Material

| Item | Valor |
|---|---|
| Master | `video/Teleprompter-2026-06-10_15-50-07_cortado.mp4` (sem pausas, já aprovado; 1080×1920, 30 fps, 41,33 s). Só leitura, nada é recomprimido |
| Trecho | **18,10 s → 33,10 s** do master (15,0 s = 450 quadros) |
| Tempos | `transcricao/15-50-07-cortado/palavras.json` |
| Rosto | `frames/rosto.json` (série A) |
| Prints | `WhatsApp Image 2026-09-01 at 20.36.42.jpeg` (ficha da Luciana Duarte) e `tela_extensao-blip-desk.png` |
| Marca | `logos/logo_beeno_transparent-2.png` (verde); Poppins; cores do `guia-edicao/1-estilo-beeno.md` |
| Som | áudio original contínuo + `sfx/whoosh.wav`, `sfx/pop.wav`, `sfx/flash.wav` (já existentes, locais) |

Fala do trecho: *"Quando atendimento e vendas olham o mesmo cliente em lugares diferentes, a empresa perde timing, perde argumento e às vezes perde o cliente. Com o CRM integrado, os tickets do atendimento e os negócios do comercial ficam no mesmo contato. Quem vai falar com o cliente vê os dois lados antes."*

## Cenas (iguais nas duas ferramentas)

Tempos no relógio do master. Gatilho = início da palavra no `palavras.json`.

| # | Início–fim | Cena | Gatilho | Visual |
|---|---|---|---|---|
| 1 | 18,10–21,40 | `camera-motion` | "atendimento" @18,41 · "vendas" @19,03 · "diferentes" @20,67 | Câmera 100%. Duas pílulas no topo, "Atendimento" e "Vendas", entram juntas no centro e **se afastam** para as bordas em "diferentes" |
| 2 | 21,40–25,20 | `camera-motion` | "timing" @22,33 · "argumento" @23,43 · "cliente" @24,81 | Corte com punch-in para 130% (âncora no rosto). Três chips empilham no topo: "− timing", "− argumento", "− cliente" (este em vermelho), com um pop em cada |
| 3 | 25,20–26,80 | palco desfocado + logo | "CRM" @25,78 | Flash branco curto com whoosh; o próprio take desfocado vira fundo; logo Beeno grande entra com borrão; "CRM integrado" embaixo do logo |
| 4 | 26,80–30,70 | `demo` (tela dividida vertical) | "tickets" @26,94 · "negócios" @28,06 · "mesmo contato" @29,66 | Print da ficha em cima, câmera embaixo (`synchronized-split`). Zoom + marca-texto em **Ticket associado**, depois em **Negócio associado**, e recuo para a ficha inteira em "mesmo contato" |
| 5 | 30,70–33,10 | `demo` | "dois" @32,14 · "lados" @32,28 | Print da extensão no Blip Desk (só a área da tela, sem o título do banner). Moldura verde na conversa em "dois" e no painel Beeno em "lados" |

**Em todas:** legenda palavra por palavra (branca, bold, sombra suave, acumulando por frase), sobre o peito nas cenas 1–3 e na faixa entre print e câmera nas cenas 4–5. Rosto sempre livre. Áudio original uma vez só, sem música.

## Onde fica cada versão

| | Remotion | HyperFrames |
|---|---|---|
| Código | `src/videos/comparativo-remotion/` + registro em `src/Root.tsx` | `comparativo-hyperframes/` (projeto à parte, criado com `npx hyperframes init`; o master entra por link, sem cópia) |
| Render | `npx remotion render` local | `npx hyperframes render` local (sem `cloud render`) |
| Saída | `edicoes/001. beeno-video/comparativo/remotion.mp4` | `edicoes/001. beeno-video/comparativo/hyperframes.mp4` |

Extras: `lado-a-lado.mp4` (as duas versões juntas, para assistir de uma vez) e `comparativo.md` com a tabela de critérios.

Observação: o HyperFrames tem plugin e skills para o Claude Code, mas instalar o plugin muda a sua configuração global. Para o teste, vou ler a documentação que vem no próprio pacote e não instalo nada global, a menos que você peça.

## Critérios da comparação

1. Qualidade visual (stills lado a lado, nos mesmos quadros).
2. Sincronia: cada gatilho dentro de ±1 quadro da palavra.
3. Esforço: arquivos e linhas de código, problemas encontrados no caminho.
4. Render: tempo, tamanho do arquivo, duração exata (450 quadros) e uma única trilha de áudio.
5. Ajuste: mudar a cor de um chip e o tempo de uma entrada. Quão fácil é em cada uma.

## Próximos passos

1. Você aprova este plano (ou ajusta o trecho e as cenas).
2. Monto as duas versões e gero stills dos mesmos quadros nas duas para você comparar.
3. Com os stills aprovados, renderizo e entrego os MP4 e o `comparativo.md`.
