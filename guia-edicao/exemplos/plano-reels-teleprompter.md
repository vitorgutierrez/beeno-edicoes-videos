# Plano de edição — 001. beeno-video (Nível 2)

Dois vídeos, duas edições independentes. Status: **Revisão 3 (estilo Beeno) montada; aguardando aprovação dos rascunhos e pranchas** (`edicoes/001. beeno-video/rascunhos/` e `stills/`).

## Decisões gerais

| Item | Decisão |
|---|---|
| Público | Gestores comerciais e de atendimento (operações na Blip) |
| Uso | Anúncio pago (Reels / Stories / Shorts) |
| Formato | Vertical 1080×1920, 30 fps, duração igual ao master |
| Identidade | Banners do Beeno: fundo menta claro `#EAFBF4`, verde `#00CB88`, tinta `#141414`, branco. Logo em `logos/logo_beeno-2.png` (verde) e `-3.png` (preto), fundo branco removido na montagem. Fonte: Poppins (próxima da dos banners) |
| Intensidade | Equilibrada: câmera nos momentos de opinião, print/animação nos momentos de produto |
| Legendas | Palavra por palavra, branca em negrito com sombra, palavra-chave em amarelo `#FFD43B`, abaixo do queixo (faixa y ≈ 1340–1480), fora das zonas da interface (topo 250 px, base 420 px) |
| Tela dividida | Vertical = conteúdo em cima, câmera embaixo (`synchronized-split`), rosto sempre inteiro |
| Higgsfield | Só B-rolls realistas sem texto, sem pessoas identificáveis. Todo texto, chip, seta e print entra no Remotion |
| Montagem | **Remotion** (local, sem custo), usando os assets gerados na Higgsfield. Motivo: seu prompt pede overlays do Remotion combinados, e o Remotion dá controle fino de sincronia e enquadramento |
| Orçamento | Teto de 60 créditos por vídeo |

Correções de transcrição: chamar → chamado · perde time → perde timing · tiques → tickets · No Binance → No Beeno · "a gente mande-me com o nosso time" → "e agende uma demo com o nosso time".

Estilo dos B-rolls (sufixo): `Cinematic realistic shot, modern small office with warm exposed brick wall and light wood shelves, soft natural daylight, shallow depth of field, calm premium mood, subtle green accents (#00CB88). No people faces, no readable text, no letters, no logos, no watermark. Vertical 9:16.` Combina com a parede de tijolo das suas gravações.

---

## Vídeo A — "Uma empresa só" (`Teleprompter-2026-06-10_15-50-07.mp4`, 48,74 s)

⚠️ **O vídeo começa com 3,25 s sem fala.** Em anúncio, isso derruba a retenção. Veja a decisão pendente no fim.

| Tempo | Fala | Formato | O que entra |
|---|---|---|---|
| 0,00–3,25 | (silêncio) | `broll` | **B-roll 1**: celular sobre a mesa vibrando, tela acendendo com notificações desfocadas. Sem texto |
| 3,25–6,50 | "Isso aqui eu tenho certeza que já aconteceu na sua operação." | `camera-enfase` | Push-in 1,00→1,06. "na sua **operação**" em tipografia grande no topo, palavra por palavra |
| 6,59–10,40 | "É segunda-feira, um cliente abre um chamado no WhatsApp reclamando de um problema." | `broll` + overlay | **B-roll 2** (celular/atendimento). Chip "SEGUNDA · Atendimento" em "segunda", balão de chat "reclamação" em "WhatsApp" |
| 10,47–13,60 | "No outro dia, o comercial manda proposta de renovação." | `broll` + overlay | **B-roll 3** (notebook/e-mail saindo). Chip "TERÇA · Comercial", card "Proposta de renovação ✉" em "proposta" |
| 13,75–15,40 | "Nenhum dos dois sabia do outro." | `cena` | B-rolls 2 e 3 empilhados (cima/baixo), linha vermelha rompida entre eles em "nenhum" |
| 15,57–19,50 | "Para a empresa, são dois departamentos diferentes. Para o cliente, uma empresa só." | `aula` | Dois blocos "Atendimento" e "Comercial" separados; em "uma empresa só" eles se fundem num só |
| 19,93–21,50 | "E ela parece desorganizada." | `camera-enfase` | Punch-in até 1,12; chip "desorganizada" com leve tremida |
| 21,97–25,30 | "Quando atendimento e vendas olham o mesmo cliente em lugares diferentes," | `aula` | Um card de contato no centro, puxado por duas setas para duas telas diferentes |
| 25,45–29,00 | "a empresa perde timing, perde argumento e às vezes perde o cliente." | `camera-motion` | Três chips empilhando no topo: "− timing", "− argumento", "− cliente" (o último em vermelho), cada um na sua palavra |
| 29,23–35,20 | "Com o CRM integrado, os tickets do atendimento e os negócios do comercial ficam no mesmo contato." | `transformacao` → `demo` | Logo Beeno em "CRM integrado"; o print da ficha da Luciana Duarte (`WhatsApp…20.36.42`) toma a tela. Zoom + marca-texto no **Ticket associado** em "tickets", no **Negócio associado** em "negócios", e recuo para a ficha inteira em "mesmo contato". Câmera em card embaixo |
| 35,29–38,10 | "Quem vai falar com o cliente vê os dois lados antes." | `demo` | `tela_extensao-blip-desk`: zoom na conversa e depois no painel do Beeno ao lado ("os dois lados") |
| 38,27–42,50 | "O seu cliente enxerga uma empresa só e a sua operação também deveria." | `camera-enfase` | Volta à câmera cheia (pull-out 1,06→1,00); "uma empresa só" no topo |
| 42,63–43,90 | "Quer ver isso na prática?" | `camera-espaco` | Pergunta em tipografia grande |
| 44,07–48,74 | "Chama a gente aqui e conheça a nossa plataforma." | `transformacao` → cartela | A câmera encolhe para um card; fundo menta, logo Beeno, "O CRM feito para a sua operação na Blip" e botão "Conheça a plataforma →" pulsando até o fim |

**Higgsfield, Vídeo A**

| Asset | Modelo | Custo estimado |
|---|---|---|
| 3 imagens-base 9:16 (B-rolls 1, 2, 3) | `nano_banana_pro` 2k | 3 × 2 = 6 |
| 3 animações de 4–5 s | `kling3_0` pro, sem som | 3 × ~8 = 24 |
| Margem para refazer (~25%) | | ~8 |
| **Total** | | **~38 créditos** (teto 60) |

---

## Vídeo B — "O melhor registro" (`Teleprompter-2026-06-10_15-56-43.mp4`, 44,91 s)

A câmera mexe um pouco neste vídeo: a posição do rosto será mapeada a cada 2 s antes de qualquer tela dividida.

| Tempo | Fala | Formato | O que entra |
|---|---|---|---|
| 0,00–4,90 | "O melhor registro é aquele que ninguém precisa fazer manualmente." | `camera-espaco` | Tipografia grande no topo, palavra por palavra; "manualmente" entra riscado |
| 5,00–7,70 | "Pare de pedir para o seu time registrar tudo no CRM." | `camera-enfase` | Punch-in em "Pare"; chip "registrar tudo no CRM" com um ✕ |
| 7,80–9,90 | "Parece estranho vir de alguém que vende CRM." | `camera-motion` | Selo pequeno do logo Beeno entra no canto em "vende CRM" |
| 10,04–14,20 | "Mas pense comigo, todo processo que depende de alguém lembrar, vai falhar em algum momento." | `broll` | **B-roll 1**: post-its de lembrete caindo de um monitor, um por um. Em "falhar", o último cai |
| 14,36–17,10 | "O caminho é capturar o que já acontece." | `camera-motion` | Volta à câmera; "capturar o que já acontece" no topo |
| 17,20–20,80 | "Na operação com a Blip, por exemplo, o atendente já classifica a conversa com uma tag." | `demo` | `tela_extensao-blip-desk`: zoom na conversa; marca-texto em "Adicionar tags"; chip de tag pousa na conversa em "tag" |
| 20,92–23,90 | "No Beeno, a tag move o negócio no funil e muito mais." | `demo` | Print do kanban (`WhatsApp…20.32.08`): a tag voa até um card e um destaque verde leva o card de uma coluna à seguinte em "move" |
| 24,16–27,90 | "A conversa já existe, o histórico já existe, ele só precisa chegar no CRM." | `aula` | Fluxo que se monta: 💬 Conversa ✓ → 🕘 Histórico ✓ → seta → Beeno, que entra em "chegar no CRM" com o print da ficha do contato |
| 28,40–31,50 | "Quando registra a consequência do trabalho e não uma tarefa a mais," | `aula` | Dois lados: "consequência do trabalho ✓" × "tarefa a mais ✕" (print `tela_tarefas` esmaecido e riscado) |
| 31,66–35,90 | "o dado fica completo sem cobrança e o gestor deixa de ser fiscal de preenchimento." | `broll` + overlay | Barra "dados do CRM" enche até 100% em "completo"; depois o **B-roll 2**: prancheta com checklist sendo fechada e deixada de lado na mesa, em "fiscal" |
| 36,00–39,50 | "O registro bom é aquele que ninguém precisa lembrar de fazer." | `camera-enfase` | Push-in lento; retoma a frase da abertura no topo, como fechamento |
| 39,70–44,91 | "Clique em Saiba Mais e agende uma demo com o nosso time para conhecer a nossa plataforma." | `transformacao` → cartela | Câmera vira card; logo Beeno, "O CRM feito para a sua operação na Blip", botão "Saiba mais ↓" apontando para o botão do anúncio em "Saiba Mais", e "Agende uma demo" em "demo" |

**Higgsfield, Vídeo B**

| Asset | Modelo | Custo estimado |
|---|---|---|
| 2 imagens-base 9:16 (B-rolls 1 e 2) | `nano_banana_pro` 2k | 2 × 2 = 4 |
| 2 animações de 4–5 s | `kling3_0` pro, sem som | 2 × ~8 = 16 |
| Margem para refazer (~25%) | | ~5 |
| **Total** | | **~25 créditos** (teto 60) |

**Total dos dois vídeos: ~63 créditos** (de 1.050 disponíveis). Se o gasto real passar ~20% disso, eu paro e aviso.

---

## Processo

1. Gerar as imagens dos B-rolls e mostrar numa prancha para aprovação.
2. Animar só as imagens aprovadas e conferir pelo quadro do meio e do fim.
3. Programar os dois vídeos no Remotion (`src/videos/beeno-uma-empresa/` e `src/videos/beeno-melhor-registro/`).
4. Gerar quadros de revisão de cada troca de layout (rosto, legibilidade, borda, sincronia) e corrigir antes do render.
5. Render final em `edicoes/001. beeno-video/` e conferir duração, resolução e volume iguais aos do original.

## Decisão tomada

**Opção (a) aprovada.** Cópia aparada em `video/Teleprompter-2026-06-10_15-50-07_aparado.mp4` (começa em 3,00 s do original, 45,75 s, original intocado). Tempos em `transcricao/15-50-07-aparado/palavras.json` (todos os tempos da tabela do Vídeo A recuam 3,00 s). Com isso o B-roll 1 do Vídeo A saiu do plano: Vídeo A passa a ter 2 imagens + 2 animações (~25 créditos com margem).

Imagens geradas: `hf/A1_segunda_celular.png`, `hf/A2_terca_notebook.png` (refeita sem texto na tela), `hf/B1_postits.png`, `hf/B2_prancheta.png`. Gasto até aqui: ~10 créditos.

### Opções que estavam em aberto

**Os 3,25 s iniciais sem fala do Vídeo A.** Opções:
- **(a) Recomendado:** você autoriza remover só esse silêncio inicial. Eu faço uma cópia aparada (o arquivo original não é tocado) e o vídeo passa a começar em "Isso aqui…". Fica com ~45,5 s.
- **(b)** Manter o vídeo intacto e cobrir o silêncio com o B-roll 1 (já está no plano acima).

## Produção (registro)

- Animações `kling3_0` pro, 5 s, sem som: `hf/A1_segunda_celular.mp4`, `hf/A2_terca_notebook.mp4`, `hf/B1_postits.mp4`, `hf/B2_prancheta.mp4`.
- Refeitos: A2 (imagem com texto na tela) e A1 (animação gerou letras nos balões). Versões antigas guardadas com sufixo `_v1_com-texto`.
- B2: uma mão entra pela base do clipe; escondida com recorte de 1,32× a partir do topo.
- Logos com fundo transparente gerados em `hf/logo_beeno_*_alpha.png`.
- Créditos gastos: **~54** (saldo 1.050 → 996). Estimado: ~63.
- Montagem no Remotion: `src/videos/beeno-uma-empresa/`, `src/videos/beeno-melhor-registro/`, componentes em `src/videos/_beeno/`. Tela dividida vertical adicionada em `src/_shared/synchronized-split.tsx`.
- Legendas com uma faixa escura translúcida atrás (o fundo menta das telas divididas deixava o branco ilegível).

## Mudanças pedidas depois do plano

- **Música** (pedido em 06/10): trilha instrumental original composta por código (`musica/compor_trilha.py`), sem samples nem direitos de terceiros. Seção contida no problema e virada otimista na solução ("Com o CRM integrado" no A, "O caminho é capturar" no B), ducking de -8 dB sob a voz, ~16 dB abaixo da voz na mixagem.
- **Cortes nas pausas** (pedido explícito, exceção ao `locked-final-cut`): cópias `video/*_cortado.mp4` geradas a partir dos ORIGINAIS por `cortar_pausas.py`; originais intocados. Pausas >= 0,4 s (abaixo de -30 dB) ficam com 0,1 s de respiro de cada lado; final com 0,35 s depois da última palavra (pedido: sem a espera olhando para a câmera). A: 48,7 → 41,3 s; B: 44,9 → 38,4 s. Tempos em `transcricao/*-cortado/` (palavras.json e cortes.json). Em cada corte o enquadramento alterna 1,00/1,06 para o corte parecer intencional.
- Volume: o áudio mono do celular perde 3 dB ao virar estéreo no Remotion; compensado com +3 dB. Mix final com o mesmo volume médio do original.

## Revisão 2 (08/10): edição de impacto

Pedido: edição muito simples, sem sons, música sem relação com o conteúdo. Referência: anúncio da Meta Ads Library 1069518592624860 (analisado só como referência; nada dele entra no vídeo).

- Planos em corte seco (aberto 1,00 / fechado 1,22 no rosto) nas trocas de frase.
- Telas de impacto (fundo branco, palavras batendo com tremida): A "Ela parece DESORGANIZADA", "PERDE O CLIENTE", "UMA EMPRESA SÓ"; B "NINGUÉM PRECISA FAZER MANUALMENTE", "VAI FALHAR", "FISCAL DE PREENCHIMENTO".
- Preto e branco no trecho do problema; a cor volta com luz vazada + flash na virada.
- Textos que batem na tela (Slam) no lugar das tipografias suaves; etiquetas empilhando ("− timing", "− argumento").
- Prints entram inclinados em 3D; cursor clica no ticket, no negócio, em "Adicionar tags", arrasta o card do kanban e clica no botão final.
- Efeitos sonoros originais (`sfx/gerar_sfx.py`): whoosh, pop, clique, notificação, impacto, flash, riser, deslizar, tick, erro.
- Música nova (`musica/compor_trilha.py`): batida 92 BPM em lá menor (piano, 808, palmas, chimbal), abafada no problema, cheia na solução, com silêncio de 0,45 s antes de cada impacto; ~20 dB abaixo da voz.
- Legendas sem tarja, brancas com contorno; ocultas durante as telas de impacto.
- Masterização: limitador em -1 dBFS (`masterizar.sh`), sem mudar o volume médio.

## Revisão 3 (08/10): estilo Beeno (`guia-edicao/1-estilo-beeno.md`)

Pedido: refazer os dois vídeos seguindo o manual de estilo Beeno. Substitui a revisão 2 (telas brancas, tremida, luz vazada, etiquetas laranja, cartela final e P&B longo saem).

### Base comum
| Item | Decisão (seção do manual) |
|---|---|
| Masters | as cópias sem pausas já aprovadas (`video/*_cortado.mp4`); fala começa no 1º quadro e termina ~0,35–0,6 s antes do fim (4.2) |
| Família | **A = estúdio** (tripé, parede de tijolo); **B = selfie** (janela ao fundo, câmera na mão). Os dois são "de produto", então usam blocos **Beeno dark** da família C (2) |
| Punch-in | escala parada por plano, troca em cada frase, 1–2 quadros antes da 1ª palavra. A: 100 / 130 / 160 %, âncora no centro do rosto (550, 760). B: 100 / 115 / 130 %, âncora no queixo (555, 1290) para o rosto nunca ser cortado (4.3) |
| Legenda | Montserrat Bold 72 px, branca, sem contorno, sombra 3px 4px 6px, caixa baixa (maiúscula só no início e em Beeno/Blip/CRM/WhatsApp), sem ponto final, palavra por palavra acumulando, página por frase/vírgula, até 3 linhas de ~22 caracteres; peito (A: topo em y 1390; B: y 1420), na emenda no split, some no palco com tipografia e no Beeno dark (5.1) |
| Cores | vermelho `#EC1D1D` dor, amarelo `#F4C70F` alerta, verde `#00CB88` solução, azul `#0090FF` comercial; 3–6 palavras por vídeo (5.2) |
| Palco desfocado | o próprio take com `blur(32px)`, ampliado e subido para o queixo ficar acima de y ≈ 900–1000; logo/tipografia **abaixo do queixo** (regra do rosto livre, seção 13) |
| Split B-roll | câmera em cima (rosto inteiro até y ≈ 800), B-roll embaixo a partir de y ≈ 880 com emenda em degradê, legenda na emenda (7) |
| Beeno dark | fundo `#091B15` + brilho `#09402D` (azul-petróleo `#082E37` nas cenas da Blip), grade de 40 px, cards de vidro com **prints reais**, títulos Poppins em 3 níveis parafraseando a fala, ✓/✗ por palavra (8) |
| Dados | nos prints da Blip e da ficha, **telefone e e-mail reais ficam desfocados** (seção 13); nomes de demonstração ficam |
| Transições | corte seco na maioria; flash branco com rampa de desfoque + whoosh em 3 viradas por vídeo (9). Sem tremida, glitch, vinheta |
| Logo Beeno | uma vez, grande, centralizado abaixo do queixo, entrada rápida com borrão de movimento + estrondo (6.2) |
| Final | CTA na câmera nítida, **sem cartela** (1, regra 14) |
| Som | SFX só nos eventos (10.2), começando 1–2 quadros antes; ≤ 1 som forte a cada 1,5 s; trilha nova ~110 BPM sem melodia, **entra na virada**, ~15 dB abaixo da voz; master −15 LUFS, pico −1 dBTP |

### Vídeo A — "Uma empresa só" (41,3 s)
| Tempo | Fala | Cena | O que entra |
|---|---|---|---|
| 0,00–3,5 | "Isso aqui eu tenho certeza que já aconteceu na sua operação." | `camera` 100 % → 130 % em "já aconteceu" | legenda; "operação" verde não (texto comum) |
| 3,6–7,2 | "É segunda-feira, um cliente abre um chamado no WhatsApp reclamando de um problema." | `split` B-roll celular | pop + notificação em "chamado"; "atendimento" não é dito aqui |
| 7,3–10,4 | "No outro dia, o comercial manda proposta de renovação." | `split` B-roll notebook | "comercial" **azul**; clique em "proposta" |
| 10,5–11,9 | "Nenhum dos dois sabia do outro." | `camera-impacto` 160 % **P&B**, legenda amarela | — |
| 12,0–14,8 | "Para a empresa, são dois departamentos diferentes." | `split-painel`: câmera à esquerda; painel amarelo "Atendimento" em "dois", azul "Comercial" em "departamentos" | impacto grave no painel |
| 14,9–16,1 | "Para o cliente, uma empresa só." | `palco` + **linha-chave** "uma empresa SÓ" (verde) abaixo do queixo | impacto |
| 16,2–17,9 | "E ela parece desorganizada." | `camera-impacto` 160 % | "desorganizada" **vermelho** |
| 18,2–21,4 | "Quando atendimento e vendas olham o mesmo cliente em lugares diferentes," | `camera` 130 % → 100 % em "o mesmo cliente" | "atendimento" amarelo |
| 21,5–25,2 | "a empresa perde timing, perde argumento e às vezes perde o cliente." | `palco` + lista **✗** vermelha (timing, argumento, o cliente), um item por palavra | pop em cada ✗ |
| 25,3–26,6 | "Com o CRM integrado," | **virada**: flash branco + riser/whoosh → `palco` + **logo Beeno** (zoom-out com borrão) | estrondo; trilha entra aqui |
| 26,6–30,7 | "…os tickets do atendimento e os negócios do comercial ficam no mesmo contato." | `ui` Beeno dark: print da ficha num card, zoom + marca-texto no ticket e no negócio, cursor clicando; título "tickets + negócios / no **mesmo contato**" | cliques |
| 30,8–33,1 | "Quem vai falar com o cliente vê os dois lados antes." | `ui` Beeno dark: print da extensão no Blip Desk, contorno "Conversa" e "CRM"; título "vê os **dois lados** antes" | pops |
| 33,2–36,2 | "O seu cliente enxerga uma empresa só e a sua operação também deveria." | flash → `camera` 100 % → 160 % em "e a sua operação" | "também deveria" **verde** |
| 37,0–41,3 | "Quer ver isso na prática? Chama a gente aqui e conheça a nossa plataforma." | flash → `cta` câmera nítida, punch-ins curtos (100 → 130 em "conheça") | sem cartela |

### Vídeo B — "O melhor registro" (38,4 s)
| Tempo | Fala | Cena | O que entra |
|---|---|---|---|
| 0,00–2,9 | "O melhor registro é aquele que ninguém precisa fazer manualmente." | `camera` 100 % → 115 % em "ninguém" | "NINGUÉM" em caixa alta 1,3× na legenda |
| 3,1–5,1 | "Pare de pedir para o seu time registrar tudo no CRM." | `camera-impacto` 130 % **P&B**, legenda amarela | — |
| 5,6–7,3 | "Parece estranho vir de alguém que vende CRM." | `camera` 100 % | — |
| 7,7–10,4 | "Mas pense comigo, todo processo que depende de alguém lembrar," | `split` B-roll post-its | — |
| 10,4–11,3 | "vai falhar em algum momento." | `camera-impacto` 130 % | "falhar" **vermelho** |
| 11,8–14,0 | "O caminho é capturar o que já acontece." | **virada**: flash + whoosh/riser → `palco` + linha-chave "CAPTURAR o que já acontece" (verde) | trilha entra aqui |
| 14,3–17,8 | "Na operação com a Blip, por exemplo, o atendente já classifica a conversa com uma tag." | `ui` Beeno dark (brilho azul-petróleo): print do Blip Desk, cursor clica em "Adicionar tags", tag "Proposta enviada" estala; título "o atendente **classifica** com uma tag" | clique + pop |
| 17,8–18,9 | "No Beeno," | `palco` + **logo Beeno** (whip com borrão), aterrissa ~0,3 s antes de "Beeno" | estrondo + whoosh |
| 18,9–20,9 | "…a tag move o negócio no funil e muito mais." | `ui` Beeno dark (brilho verde): kanban, cursor arrasta o card para "Proposta enviada"; título "a tag **move o negócio**" | clique + deslizar + ding |
| 21,1–24,0 | "A conversa já existe, o histórico já existe, ele só precisa chegar no CRM." | `ui` Beeno dark: ✓ "a conversa já existe", ✓ "o histórico já existe", título "só precisa **chegar no CRM**" | pop por item |
| 24,5–27,2 | "Quando registra a consequência do trabalho e não uma tarefa a mais," | flash → `camera` 115 % | "consequência" **verde**, "tarefa a mais" **vermelho** |
| 27,6–29,5 | "o dado fica completo sem cobrança" | `camera` 100 % | "completo" **verde** |
| 29,6–30,5 | "e o gestor deixa de ser" | `split` B-roll prancheta | — |
| 30,5–31,7 | "fiscal de preenchimento." | `palco` + **X desenhado** sobre "FISCAL DE PREENCHIMENTO" | som de erro/rabisco |
| 31,8–34,4 | "O registro bom é aquele que ninguém precisa lembrar de fazer." | `camera` 130 % → 100 % em "ninguém" | — |
| 34,6–38,4 | "Clique em Saiba Mais e agende uma demo com o nosso time para conhecer a nossa plataforma." | flash → `cta` câmera nítida, punch-ins (100 → 115 em "agende" → 100 em "para conhecer") | "demo" **verde**; sem cartela |

### Desvios conscientes do manual
- **Rosto livre:** no palco, logo e tipografia ficam abaixo do queixo (o manual pede isso na seção 13).
- **Logo Blip:** não há arquivo do logo da Blip no projeto e o estúdio não recria logos. No "Blip" do vídeo B entra o **print real do Blip Desk**. Se quiser o logo, salve um PNG em `logos/`.
- **B-roll:** reaproveito os 4 já gerados (0 crédito novo).

### Produção da revisão 3 (registro)
- Plano e escolha do logo aprovados (logo aterrissa ~0,3 s antes de "Beeno", conforme o manual).
- Código: `src/videos/_beeno/estilo.tsx` (CameraBeeno, SplitBroll, PaineisCor, FlashBranco, LogoEntrada, LinhaChave, ListaX, XDesenhado, BlocoDark, CardVidro, TituloDark, ListaCheck, LegendaBeeno) e os dois vídeos reescritos.
- Logo para fundo escuro: `hf/logo_beeno_lockup_escuro.png` ("beeno" verde + "by skeps" branco, a partir de `logos/logo_beeno-2.png`).
- Dados reais desfocados nos prints: e-mail na ficha; telefone e e-mail no Blip Desk.
- Trilha nova (`musica/compor_trilha.py`): 110 BPM, sem melodia, entra na virada; ~15 dB abaixo da voz.
- Master (`masterizar.sh`): loudnorm em duas passadas, −15 LUFS / −1 dBTP, duração do áudio igual à do vídeo.
- 0 crédito da Higgsfield nesta revisão (B-rolls reaproveitados).
