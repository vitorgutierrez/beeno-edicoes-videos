# Grupo C: análise forense de edição (Reels 02 e REELS - Frase Blip ID)

Vídeos: 1080x1920, 30 fps, HEVC, AAC 44,1 kHz. Marca Beeno ("by skeps"), CRM no WhatsApp.
Método: contact sheets a cada 0,5 s, quadros em resolução cheia, tiras de 30 fps (±0,3–0,4 s) em todos os cortes, amostragem de cor em pixels (PIL), `palavras.json` (faster-whisper large-v3-turbo) para cruzar cortes e legendas com a fala, e análise espectral do áudio (numpy).
Material de trabalho: `scratchpad/work-grupo-c/` (r2/, r2s/, r2f/, blip/, bs/).

---

## VÍDEO 1: Reels 02 (65,62 s)

### 1. Resumo
- **Tema:** "o prejuízo invisível". O lead manda mensagem no WhatsApp no sábado à noite, ninguém responde, ele vai para o concorrente e nunca entra em estatística nenhuma. A Beeno transforma cada conversa em lead rastreável.
- **Gancho (0–4,9 s):** "Deixa eu te contar sobre a venda mais cara que a sua empresa perde, a que você nem sabe que existiu." Tela dividida com B-roll de mãos mexendo em notas de dólar.
- **Problema (4,9–33,2 s):** narrativa do lead perdido (sábado → segunda → concorrente → "prejuízo invisível").
- **Solução genérica (33,2–49,1 s):** "a única forma... é ter um sistema onde todo contato vira um registro/oportunidade dentro do CRM"; B-roll de HUD.
- **Produto (49,1–60,0 s):** logo beeno com flash, UI animada da Beeno (Conversas → Resumo por IA → Pipeline de vendas), frase de efeito "O que era invisível agora se torna visível".
- **CTA (60,0–65,53 s):** "Então pare de perder venda, chame a gente aqui no link da bio, que eu pessoalmente vou te mostrar como que funciona na prática." Termina em cabeça falante e 3 quadros pretos.

### 2. Shot list / linha do tempo
TH = talking head (cabeça falante, selfie sentado, janela com prédios de SP atrás). Escala relativa medida pela largura dos óculos: ~35–37% da largura do quadro no plano aberto, ~44% no médio, ~50–52% no fechado. Ou seja, há três níveis de recorte: 100% / ~118% / ~140%.

| # | início–fim (s) | dur | tipo | enquadramento / conteúdo | legenda |
|---|---|---|---|---|---|
| 1 | 0,00–3,10 | 3,10 | **Tela dividida** | Metade de cima: TH fechado (rosto entre y≈100–800), com gradiente preto da y≈700 até a junção. Metade de baixo (y≈1010–1920): B-roll de banco de imagens, mãos dobrando/rasgando notas de dólar (camiseta branca) | branca, na junção (y≈905–1041) |
| 2 | 3,10–4,93 | 1,83 | TH fechado (~140%) | rosto grande, centralizado | y≈1290 |
| 3 | 4,93–5,83 | 0,90 | TH aberto (100%) | cortina e janela visíveis, gesto com a mão | y≈1500 |
| 4 | 5,83–7,83 | 2,00 | Tela dividida | em cima, TH; embaixo, B-roll de mão rolando app de loja no celular (fundo bege) | na junção (y≈860) |
| 5 | 7,83–10,10 | 2,27 | Tela dividida | embaixo, celular com WhatsApp em ângulo (tela verde-clara, fundo preto, dedo) | na junção (y≈865) |
| 6 | 10,10–11,40 | 1,30 | **TH desfocado** (gaussiano forte) | mesmo take, plano aberto | grande e centralizada: "O time só vê na **SEGUNDA**" |
| 7 | 11,40–12,73 | 1,33 | TH médio (~118%) | | y≈1445 |
| 8 | 12,73–14,53 | 1,80 | TH fechado (~140%), jump cut | | y≈1445 |
| 9 | 14,53–15,60 | 1,07 | TH aberto | | y≈1495 |
| 10 | 15,60–18,97 | 3,37 | TH médio, com zoom lento de ~44% para ~50% de largura dos óculos (+12% em 3,4 s) | polegar para cima | y≈1460–1510 |
| 11 | 18,97–20,80 | 1,83 | **Cartela preta cheia** (#000000) | só tipografia: "ELA SIMPLESMENTE / VAI", depois "NO CONCORRENTE" | centro (y≈863–999) |
| 12 | 20,80–21,80 | 1,00 | TH | mão no peito | y≈1450 |
| 13 | 21,80–23,27 | 1,47 | **TH desfocado** | | palavra única amarela itálica: VOCÊ → NUNCA → VAI → SABER → QUE → EXISTIU |
| 14 | 23,27–25,47 | 2,20 | Tela dividida | embaixo, relatório impresso com gráficos de barras vermelhos e caneta vermelha ("estatística") | na junção (y≈920) |
| 15 | 25,47–28,03 | 2,57 | TH fechado | | y≈1250–1290 |
| — | 28,03–28,13 | 0,10 | **Transição flash** | desfoque e brilho → 2 quadros brancos | |
| 16 | 28,13–30,17 | 2,03 | TH (começa nítido em "eu chamo isso", fica desfocado em "PREJUÍZO") | | "PREJUÍZO" → "INVISÍVEL" amarelo itálico |
| 17 | 30,17–33,20 | 3,03 | TH médio | | y≈1400–1495 |
| 18 | 33,20–35,20 | 2,00 | TH aberto (cortina visível), zoom lento de +9% em 1,9 s | | y≈1450 |
| 19 | 35,20–39,00 | 3,80 | **B-roll cheio**: HUD de banco de imagens magenta/roxo no preto ("TARGET MARKET", "DATA", anéis de %, números subindo) | | **sem legenda** (fala "é ter um sistema onde todo contato, não importa o canal...") |
| 20 | 39,00–41,43 | 2,43 | TH médio | | y≈1490 |
| — | 41,40–41,47 | ~0,07 | Transição: rampa de desfoque, 1 quadro de brilho branco | | |
| 21 | 41,47–45,47 | 4,00 | **B-roll cheio**: HUD ciano e magenta, cartões de perfil com estrelas e campo "Type" em perspectiva | | sim, branca, y≈1215–1240 |
| 22 | 45,47–49,13 | 3,67 | TH aberto/médio | | y≈1445 |
| — | 49,13–49,23 | 0,10 | **Flash branco** (1 quadro de brilho + 2 brancos, logo já aparece no branco) | legenda some 5 quadros antes | |
| 23 | 49,23–50,73 | 1,50 | **Logo** "beeno by skeps" verde sobre TH desfocado | logo centralizado, y≈1000–1130, ~80% da largura | sem legenda |
| 24 | 50,73–56,07 | 5,33 | **UI animada da Beeno** em tela cheia (fundo verde-escuro com bokeh). Card "Conversas" com balões entrando um a um, depois "Resumo por IA", depois "Pipeline de vendas" (Lead ✓, Contato ✓, Proposta R$ 24.000, Negociação, Fechamento) | | sim, branca, y≈1300–1320 |
| 25 | 56,07–60,00 | 3,93 | TH desfocado | | centralizada, branco + **verde** ("agora se torna visível", "consegue melhorar") |
| 26 | 60,00–65,53 | 5,53 | TH nítido (o desfoque sai em ~3 quadros, sem corte), zoom lento de +4% | CTA | y≈1450 |
| — | 65,53–65,62 | 0,09 | 3 quadros pretos | | |

### 3. Ritmo de corte
- **25 segmentos visuais** em 65,5 s. Média de **2,6 s**, mediana de **2,07 s**, mínimo de 0,90 s, máximo de 5,5 s. Os planos ficam mais longos depois de 49 s (produto e CTA).
- **Onde os cortes caem:** em 22 dos 25 cortes, o corte fica entre −0,13 s e +0,05 s do início da primeira palavra da nova frase (mediana ≈ −0,02 s, ou seja, 0–3 quadros **antes** da palavra). **Regra: cada frase (vírgula ou ponto) = um corte novo = uma página nova de legenda.**
- **Remoção de silêncio:** pausa máxima entre palavras de 0,32 s, pausa média de 0,019 s, nenhum silêncio de 0,25 s abaixo de −40 dB. Fala densa: **3,97 palavras/s**. Os cortes por frase são jump cuts que eliminam respiração.
- **Alternância de punch-in:** três níveis (≈100 / 118 / 140%), alternados sem padrão fixo; jump cuts no mesmo take (ex.: 11,40 médio → 12,73 fechado → 14,53 aberto). Dentro de vários planos de TH há **zoom lento digital** de ~+3–6%/s (Ken Burns de entrada).
- A cada ~2–4 s entra um "evento" (B-roll, desfoque, cartela, flash). Nunca há mais de ~5,5 s de TH puro seguido.

### 4. Legendas e tipografia
Há **cinco estilos de legenda** no mesmo vídeo, cada um ligado a um tipo de plano:

| estilo | onde | fonte | tamanho | cor | comportamento |
|---|---|---|---|---|---|
| **A. Base** | TH nítido, B-roll e UI | **Montserrat Bold**, minúsculas, como na fala (sem pontuação) | ~64–66 px (caixa da linha 70 px; cap height ~44 px); entrelinha ~82 px | branco #FCFCFC, sem contorno; sombra quase invisível | **palavra por palavra acumulando** na página (palavra aparece 0–2 quadros antes de ser dita); até 3 linhas de ~3–4 palavras (~22 caracteres), largura máxima ~670 px (62%), centralizada em x≈540; página zera a cada frase/corte. Sem pop/escala |
| **B. Desfoque com palavra-chave** | TH desfocado (10,1 s) | Montserrat ExtraBold | linha branca ~100 px; palavra-chave em CAIXA ALTA ~125 px (cap height 89 px) | branco + **amarelo #EFCE1A** ("SEGUNDA"), sombra projetada escura (~4 px) | palavras acumulam; a palavra-chave entra em linha própria |
| **C. Palavra única de impacto** | TH desfocado (21,8 e 28,1 s) | **Montserrat Black Italic**, CAIXA ALTA | ~105 px (cap height 73 px) | **amarelo-limão #EEF20A** com **contorno preto ~8 px** | uma palavra por vez, trocando no tempo de cada palavra, centralizada em y≈924–997 (sobre o rosto desfocado) |
| **D. Cartela preta** | fundo #000000 (18,97 s) | geométrica pesada em caixa alta (Montserrat ExtraBold ou Gilroy) | ~85 px (cap height 60 px) | branco + **verde-limão #A6FD0A** na palavra ativa | **karaokê**: a página inteira aparece de uma vez ("ELA SIMPLESMENTE / VAI") e a palavra falada fica verde; depois "NO **CONCORRENTE**" |
| **E. Frase de efeito no desfoque** | TH desfocado (56–60 s) | Montserrat ExtraBold | ~80–90 px | branco + **verde #0ED20E** (meia frase: "agora se torna visível", "consegue melhorar"), com sombra | acumula palavra por palavra, centralizada (y≈1040–1100) |

- **Posição:** no TH, a legenda fica **abaixo do queixo, sobre a jaqueta preta** (centro y≈1450; faixa de 1250–1510 conforme o zoom). O fundo escuro garante a leitura sem contorno. Na tela dividida, fica **sobre o gradiente escuro da junção** (y≈860–1040). Nas UIs/HUDs, a ~y 1215–1320.
- **Regra de destaque:** no texto comum, nunca há destaque. Destaque só nos momentos-chave, que sempre ganham fundo desfocado ou preto: dia (SEGUNDA), consequência (SIMPLESMENTE, CONCORRENTE), negação (NUNCA... EXISTIU), conceito-tese (PREJUÍZO INVISÍVEL), virada (agora se torna visível). Amarelo = problema/dor; verde = virada/solução/marca.
- Sem emoji. Sem caixa/tarja de fundo atrás do texto.

### 5. Elementos gráficos
- **Logo:** "beeno" em verde **#12E68A** + "by ⚡skeps" pequeno em branco, centralizado (~80% da largura), entra num **flash branco** e fica sobre o TH desfocado por 1,5 s, a partir de "É exatamente isso que o Bino faz" (49,2 s). O logo aparece ~0,9 s antes de o nome ser dito. É o único uso do logo; não há marca d'água nem end card.
- **UI do produto (50,7–56,1 s):** fundo verde-escuro **#091B15 → #09271B** com manchas de bokeh verde (#0B4A30 aprox.) desfocadas nos cantos. Cards "vidro" escuros com borda sutil, fonte **Poppins**. Balões do cliente em cinza-escuro e balões da empresa em **gradiente verde-menta** (#2BB673 → #3ED598 aprox.). Card "★ Resumo por IA" ("Lead com **alta intenção**..."). "Pipeline de vendas" com timeline vertical de checks verdes e etapa ativa destacada. Os elementos entram com fade e leve subida (~6–8 quadros), sincronizados com "conecta", "transforma", "rastreável".
- **HUDs de banco de imagens:** magenta **#DB00F6** e ciano **#15FFF9** sobre preto puro (estética sci-fi de "data"). Fora da identidade verde da marca.
- **Tela dividida:** junção na altura de y≈1010–1030 (≈53% em cima / 47% embaixo). A parte de baixo do TH escurece com gradiente para preto de y≈700 até ~1000 (luminância 90 → 30). O B-roll começa logo abaixo, sem linha divisória.
- Sem gradação de cor (TH natural, céu estourado), sem P&B, sem vinheta, sem barra de progresso, sem stickers.

### 6. Transições e efeitos
- **Corte seco** em ~80% das trocas.
- **Flash branco com desfoque** (assinatura da edição), 3 vezes: 28,03 ("eu chamo isso de prejuízo invisível"), 41,43 (entrada do HUD 2) e 49,13 (logo). Quadro a quadro: q1 desfoque gaussiano entrando, q2 brilho (bloom) a ~70%, q3–q4 branco puro (no 49,13 o logo já aparece sobre o branco), depois o novo plano. Total de ~3–4 quadros (0,10–0,13 s).
- **Desfoque como "modo ênfase":** o próprio TH recebe desfoque gaussiano forte (raio ~25–40 px em 1080p) para virar fundo da tipografia grande. Entra por corte e sai por corte ou rampa de 3 quadros (60,0 s).
- **Corte para preto puro** com 4 quadros vazios antes de o texto entrar (18,97 → 19,10).
- **Zoom lento** de entrada nos TH (+4 a +12% por plano). Sem tremida artificial, sem glitch, sem whip pan, sem speed ramp.

### 7. B-roll
| tempo | conteúdo | estilo | relação com a fala |
|---|---|---|---|
| 0–3,1 | mãos dobrando/rasgando notas de dólar | banco de imagens realista, fundo escuro, camiseta branca | metáfora: "venda mais cara que sua empresa perde" (dinheiro indo embora) |
| 5,8–7,8 | mão rolando loja/app no celular | banco realista | literal: "alguém vê seu anúncio, se interessa" |
| 7,8–10,1 | celular com WhatsApp, dedo digitando | banco realista, fundo preto | literal: "manda uma mensagem no WhatsApp" |
| 23,3–25,5 | relatório com barras vermelhas e caneta | banco realista | literal: "estatística de venda perdida" |
| 35,2–39,0 | HUD magenta "TARGET MARKET/DATA" | motion graphic de banco | metáfora de "sistema" |
| 41,4–45,5 | HUD de perfis, estrelas, campo "Type" | motion graphic de banco | metáfora: "cada mensagem entra no funil, ganha um dono" |
| 50,7–56,1 | UI da Beeno (motion design próprio) | marca, verde-escuro | literal: produto |

- A voz continua por baixo de todo B-roll (narração contínua, áudio intacto).
- Na tela dividida, o rosto continua visível em cima, então o B-roll nunca tira o apresentador por completo nos primeiros 25 s. B-roll de tela cheia só aparece da metade para o fim.
- Nada parece gerado por IA; é tudo banco de imagens ou motion design próprio.

### 8. Áudio
- Integrado **−24,5 LUFS**, LRA 2,7 LU, pico −0,6 dBTP. Voz bem comprimida e baixa para padrão de Reels.
- **Trilha:** não há batida identificável (autocorrelação sem tempo claro). Nas pausas, o nível fica só 6–10 dB abaixo da voz, com 76–88% da energia abaixo de 200 Hz entre 0–30 s e 62–65 s. Entre 31–61 s, esse piso grave cai ~25 dB. Isso indica ruído grave de ambiente/take (ar-condicionado, trânsito) que muda entre takes, e **não** uma trilha musical constante. Conclusão: **sem trilha musical evidente** (talvez uma trilha muito baixa só no começo, pouco provável).
- **SFX prováveis:** jatos curtos (50–150 ms) de banda alta (>5 kHz) **dentro de pausas da fala** e alinhados com transições: 18,95–19,05 (corte para cartela preta, 72% da energia acima de 4 kHz na pausa), 27,95–28,07 (flash), 41,40–41,65 (flash do HUD), 49,00–49,13 (flash do logo), 50,73 (entrada da UI, clique) e 21,70–21,78 (antes de "NUNCA"). Padrão: **whoosh/swish curto em cada flash/cartela, clique/pop na entrada de gráfico.**
- O silêncio foi removido por cortes (pausas ≤0,32 s).

### 9. CTA e final
- CTA falado sobre TH nítido (o desfoque sai em 60,0), com legenda base. Sem botão, seta, logo ou end card. Termina com 3 quadros pretos (65,53–65,62). O "link da bio" fica só na fala e na legenda.

### 10. O que é distintivo
- Cinco estilos tipográficos com papel definido (base, desfoque com palavra amarela, palavra única itálica com contorno, cartela preta com karaokê verde, frase-tese verde).
- **"Desfocar o próprio take" como fundo de cartela**, em vez de trocar de imagem.
- Flash branco de 3–4 quadros reservado para os 3 momentos de virada.
- Tela dividida com junção em gradiente no bloco inicial; tela cheia só depois.
- 35,2–39,0 s sem legenda (provável descuido; ao replicar, legendar).

---

## VÍDEO 2: REELS - Frase Blip ID (36,08 s)

### 1. Resumo
- **Tema:** gravado num evento da Blip (Blip ID). Ele aponta para a frase do painel "where conversations drive results" e completa: conversa sozinha não gera resultado, resultado vem do próximo passo (follow-up). A Beeno é um CRM nativo no WhatsApp, integrado com a Blip.
- **Gancho (0–3,7 s):** "Olha o que está escrito atrás de mim: onde conversas geram resultado." O painel aparece com a tradução sobreposta.
- **Virada (3,8–10,9 s):** "Eu concordo, mas falta uma parte nessa frase. Conversa sozinha não gera resultado nenhum, gera resultado quando alguém dá o próximo passo."
- **Problema (10,9–20,4 s):** "É aí que a maioria das empresas perde dinheiro no WhatsApp..." Depois, motion graphic do chat esfriando e gráfico "184 conversas / 0 vendas".
- **Solução/produto (20,4–33,4 s):** motion graphic: logo, "É por isso que o Beeno existe.", checklist de recursos, kanban e "vira venda" (R$ 18.500,00).
- **CTA (33,4–36,08 s):** "Clica no link abaixo e agende uma demonstração com a nossa equipe." Termina em TH, sem end card.

### 2. Shot list / linha do tempo
TH = selfie em pé segurando um microfone de lapela sem fio (botão preto) junto à boca, camiseta verde, crachá azul da Blip, luz roxa do estande.

| # | início–fim (s) | dur | tipo | conteúdo | legenda |
|---|---|---|---|---|---|
| 1 | 0,00–1,70 | 1,70 | TH em frente ao painel "blip id / where conversations drive results." (roxo **#5D54BD**). Rosto cortado na borda esquerda, painel ocupa o centro/direita. Os primeiros ~0,25 s têm movimento vertical forte com motion blur (câmera subindo para o painel; parece movimento real do celular usado como "whip-in") | | base, y≈1400 |
| — | 1,67–1,73 | 0,06 | flash/desfoque de 1–2 quadros | | |
| 2 | 1,73–3,73 | 2,00 | mesmo plano + **tradução sobreposta** à direita, abaixo do painel (x≈420–1020, y≈940–1150), alinhada à esquerda: "Onde / **conversas** / geram resultados". "conversas" em caixa amarela **#F9EA2D** com texto preto, imitando o marca-texto verde-limão do painel. Entra com fade e desfoque em ~4 quadros no "onde" (1,66) | a legenda base sai |
| — | 3,73–3,80 | 0,07 | **flash branco** (desfoque e brilho → 2 quadros brancos) | | |
| 3 | 3,80–6,20 | 2,40 | TH selfie andando (pilar roxo → salão do evento, pan contínuo da câmera) | | base, y≈1470 |
| 4 | 6,20–8,57 | 2,37 | **TH desfocado** (entra com zoom-blur/brilho em ~3 quadros) | | grande e centralizada: "conversa sozinha / **não gera resultado / nenhum**" |
| 5 | 8,57–10,87 | 2,30 | TH nítido (o desfoque sai) | | **tipografia mista**: "gera resultado / QUANDO ALGUÉM / *dá o próximo passo*" |
| — | 10,87–10,93 | 0,07 | **flash branco** (2 quadros) | | |
| 6 | 10,93–13,47 | 2,53 | TH mais fechado (punch-in de ~120%) | | base, y≈1430–1460 |
| 7 | 13,47–33,43 | **19,97** | **Motion graphic de produto em tela cheia** (55% do vídeo), com subcenas abaixo | texto do próprio gráfico, sem legenda palavra por palavra | |
| 7a | 13,47–17,3 | | chat "Mariana Souza" (cabeçalho com ícone do WhatsApp): balões entram sincronizados com a fala. "visto há 5 dias", "há 5 dias", "× ninguém voltou" (pílula vermelha) | "o lead chega, / o vendedor responde, / a conversa esfria" + "**e ninguém volta.**" | |
| 7b | 17,3–20,4 | | gráfico de barras "fim do mês": CONVERSAS sobe com contagem 0 → 168 → 184 (barra verde), VENDAS 0 (barra cinza) | "No fim do mês: / **muito volume de conversa** / **e nenhuma venda.**" (vermelho) | |
| 7c | 20,4–22,2 | | logo "beeno" branco dentro de anel verde (círculo que se desenha), fundo com brilho radial | "É por isso que o / **Beeno existe.**" (verde-menta) | |
| 7d | 22,2–24,2 | | logo pequeno beeno ⟷ blip no topo; chat com "+ Negócio criado · Lead recebido", "follow-up automático" | checklist "✓ CRM nativo no WhatsApp / ✓ integrado com a Blip" | |
| 7e | 24,2–30,0 | | print do kanban "Negócios" (UI clara) entra com crossfade e escala (~6 quadros); pop-ups escuros "Follow-up automático" (WhatsApp/E-mail/Ligação) e "Distribuição automática" (Ana/Bruno/Carla); depois zoom-out para o kanban inteiro com cards de KPI em contagem (24→35 negócios no funil; R$ 298 mil→R$ 437 mil em pipeline; 2x→3x mais follow-up) | "cada conversa entra / **no funil.**"; checklist "✓ follow-up automático ✓ distribuição do lead ✓ visibilidade real" | |
| 7f | 30,0–33,43 | | card se move para a coluna final, pílula de troféu "🏆 R$ 18.500,00", anéis concêntricos | "e a oportunidade / **vira venda.**" | |
| 8 | 33,43–36,08 | 2,65 | TH no salão (entra com quadro superexposto/flash) | | base, y≈1514 ("clica no link abaixo e agende... com a nossa") |

### 3. Ritmo de corte
- Fora o bloco gráfico, os segmentos de TH são **muito regulares: 1,7 / 2,05 / 2,45 / 2,37 / 2,33 / 2,57 / 2,65 s** (média de ~2,3 s). Depois vem um bloco único de 20 s de motion graphic, que tem suas próprias subcenas de ~2–6 s (mudança de tela a cada ~2,6 s em média).
- Cortes no início de frase: entre −0,11 e +0,04 s da primeira palavra (a exceção é 6,20, que fica 0,32 s antes, durante a pausa mais longa, de 0,5 s, preenchida por SFX).
- Pausa máxima entre palavras de 0,5 s, média de 0,025 s; **3,53 palavras/s**. Silêncios removidos.
- Punch-in só em 10,93 (~120%). O resto é selfie em mão, com movimento natural.

### 4. Legendas e tipografia
- **Base:** sans grotesca **Inter (ou SF Pro) SemiBold/Bold**, minúsculas, branca, **sombra suave** (~3 px para baixo, desfoque de ~6 px, preto ~40%). ~58–62 px (cap height ~44 px), centralizada, y≈1380–1515 (72–79% da altura), sobre a camiseta/mão. **Palavra por palavra acumulando**, até 3 linhas, página nova a cada frase. Mesma lógica do Reels 02, **fonte diferente**.
- **Desfoque (6,2 s):** Inter ~88 px, centralizada em y≈960; a primeira linha em Bold e as linhas de ênfase ("não gera resultado nenhum") em **Black**: contraste de peso como destaque. Branco com sombra.
- **Tipografia mista (8,57–10,87 s):** linha 1 em Inter SemiBold minúscula; linha 2 "**QUANDO ALGUÉM**" em Inter Black, caixa alta; linha 3 "*dá o próximo passo*" em **serifada bold itálica** (tipo Playfair Display/DM Serif Italic). Revelação com **letras espalhadas em laranja #FC7828** que se juntam e viram brancas em ~4–6 quadros (efeito de animador de texto estilo CapCut), mais uma **piscada de opacidade** (1 quadro a ~50%) logo depois.
- **Tradução sobreposta:** Inter Bold ~50 px branca, alinhada à esquerda, palavra-chave em **caixa amarela #F9EA2D com texto preto** (marca-texto).
- **Motion graphic:** **Poppins** Medium (linha de contexto, branca ~55 px) + Poppins Bold (linha de impacto, ~62 px). Cores de ênfase: **vermelho #F26966** (dor: "e nenhuma venda.", "× ninguém voltou") e **verde-menta #60E1B4** (solução: "Beeno existe.", "vira venda."). As linhas entram com fade de ~30% → 100% de opacidade e leve desfoque, palavra/linha no tempo da fala; o checklist acumula com ✓ verdes. **O texto do gráfico parafraseia a fala** (fala: "a oportunidade vira conversa e vira depois uma venda" → tela: "e a oportunidade vira venda."; fala: "volume de conversa que não tem venda" → tela: "muito volume de conversa e nenhuma venda.").
- Sem emoji (o único ícone é o troféu da pílula).

### 5. Elementos gráficos
- **Fundo do gráfico:** verde-escuro **#091B15** (o mesmo do Reels 02), com **grade fina** de linhas muito sutis e brilho radial central (#063F2A) nas cenas de logo.
- **Logo:** beeno branco (wordmark ~37% da largura) dentro de anel verde que se desenha (20,4 s), sincronizado com "É por isso que o Bino existe". Depois em versão pequena no topo com o lockup "beeno ⟷ blip" (co-branding com a Blip).
- **Dados animados:** contagem de números (184 conversas; KPIs 24→35, R$ 298 mil→437 mil, 2x→3x), barra verde em gradiente (#1EAB54 → #188A45) e barra cinza "0 vendas".
- **Print do produto:** kanban claro "Negócios" com colunas (Lead recebido, Qualificação, Proposta, Negociação, Fechado) e cards destacados com borda verde; pop-ups escuros sobrepostos. Print real da UI, animado com zoom, crossfade e pop-ups.
- **Cor do TH:** luz roxa do estande (#5D54BD no painel); sem gradação adicional nem P&B.

### 6. Transições e efeitos
- **Flash branco com desfoque** em 3,73 e 10,87 (2–3 quadros), mais um flash/desfoque curto de 1–2 quadros em 1,70 e um quadro superexposto na volta ao TH em 33,43. É a mesma assinatura do Reels 02.
- **Zoom-blur/brilho** na entrada do desfoque em 6,20 (~3 quadros); saída do desfoque por corte em 8,57.
- **Corte seco** do TH para o gráfico (13,47), que entra a partir do fundo verde vazio com os elementos aparecendo em fade em ~4–6 quadros.
- Dentro do gráfico: crossfade com escala (chat → kanban, 24,2 s), push-in e zoom-out no print, pop-ups com escala e fade.
- Abertura: ~0,25 s de movimento vertical com motion blur até o painel.

### 7. B-roll
- **Não há B-roll de banco nem de IA.** O "B-roll" é o **motion graphic da marca** (20 s, 55% da duração), que ilustra literalmente a fala (chat esfriando, gráfico sem vendas, produto). A voz continua por baixo o tempo todo; o rosto some por 20 s.
- O painel físico da Blip funciona como "print do mundo real": o vídeo nasce de uma frase vista no ambiente.

### 8. Áudio
- Integrado **−18,1 LUFS** (6 dB mais alto que o Reels 02), LRA 6 LU, pico +0,1 dBFS (sem limitador de true peak).
- Piso grave constante do salão (50–100 Hz, ~−33 dB nas pausas). **Sem trilha musical evidente.**
- **SFX prováveis:** whoosh de banda alta nas pausas das transições: 1,60–1,75 (flash e entrada da tradução), 3,65–3,75 (flash, 61% da energia >4 kHz na pausa), 6,02–6,20 (entrada do desfoque, 83% >4 kHz na pausa de 0,5 s), 10,68–10,90 (flash) e 33,38–33,50 (volta ao TH). Em 29,8 s, um **tom em ~650 Hz + 970 Hz** no nível da voz (−17,9 dB) entre "comercial" e "A oportunidade": provável **"ding"/chime** na cena "vira venda / R$ 18.500".

### 9. CTA e final
- TH final de 2,65 s com legenda base: "clica no link abaixo e agende uma demonstração com a nossa equipe". Termina no último quadro de vídeo (sem preto, sem end card, sem logo). A legenda nem chega a mostrar "equipe" antes do fim (corta em "com a nossa").

### 10. O que é distintivo
- Gancho situacional: um elemento real do ambiente (painel) com **tradução/legenda gráfica imitando o marca-texto do painel**.
- Estrutura em sanduíche: **~13 s de TH → 20 s de motion graphic de produto → 2,6 s de TH para o CTA**.
- Tipografia mista (sans + CAIXA ALTA black + serifa itálica) com animação de letras em laranja: o recurso mais "CapCut" dos dois vídeos.

---

## Seção cruzada: o que se repete e o que varia

### Padrões que se repetem (receita replicável)
1. **Corte em cada frase:** cortes entre 0 e 3 quadros antes da primeira palavra da frase; cada corte abre uma página nova de legenda. Segmentos de TH de **~1,0–3,4 s (mediana ~2,1–2,3 s)**. Pausas ≤0,3–0,5 s; fala de 3,5–4 palavras/s.
2. **Legenda base:** sans branca bold, **minúscula**, sem contorno, sem caixa, **palavra por palavra acumulando**, até 3 linhas (~3–4 palavras/linha, ≤~65% da largura), centralizada, **abaixo do queixo sobre a roupa escura/colorida** (centro y≈1400–1500 de 1920). Tamanho ~60–66 px.
3. **"Modo ênfase" = desfocar o próprio take** (gaussiano forte) e pôr tipografia grande e centralizada (~85–125 px) sobre ele, com sombra e contraste de cor ou de peso na palavra-chave. Dura ~1,3–2,4 s e aparece 2–5 vezes por vídeo, nas frases-tese.
4. **Flash branco de 2–4 quadros com rampa de desfoque/bloom** como transição de virada (entrada de logo, conceito-chave, mudança de cena), acompanhado de **whoosh curto** de banda alta.
5. **Motion design de produto da Beeno** com a mesma identidade: fundo **#091B15**, cards escuros de vidro, **Poppins**, verde/menta (#12E68A / #60E1B4 / gradientes #1EAB54), chat de WhatsApp ("Mariana", proposta/planos), pipeline com checks, "Resumo por IA". Elementos entram em fade e leve subida, sincronizados palavra a palavra.
6. **Cores de semântica:** amarelo/vermelho = dor/problema; verde = solução/marca/virada.
7. **Logo** só uma vez, no "é exatamente/por isso que o Beeno...", entrando por flash ou anel animado, ~0,3–0,9 s antes do nome ser falado. **Sem end card**, sem logo fixo, sem marca d'água.
8. **CTA falado em TH nítido**, com legenda base ("link"), nos últimos ~3–5 s.
9. **Sem trilha musical evidente**; só voz mais SFX pontuais nas transições. Sem P&B, sem vinheta, sem emoji, sem barra de progresso.
10. Áudio original contínuo por baixo de tudo (B-roll e gráficos nunca interrompem a voz).

### O que varia
| aspecto | Reels 02 | Frase Blip ID |
|---|---|---|
| Fonte das legendas | Montserrat (Bold/ExtraBold/Black Italic) | Inter/SF Pro (SemiBold/Black) + serifa itálica |
| Destaques | cor (amarelo #EFCE1A, limão #EEF20A com contorno preto, verde #A6FD0A/#0ED20E), caixa alta, itálico | peso (Bold → Black), caixa alta, serifa itálica, caixa amarela, letras laranja animadas |
| Ilustração | B-roll de banco (realista + HUD neon) + 5 s de UI da marca | 20 s de motion graphic da marca, sem banco |
| Tela dividida | sim (4 vezes, junção em gradiente em y≈1010) | não |
| Cartela preta com karaokê | sim | não |
| Punch-in/zoom | 3 níveis (100/118/140%) + zoom lento de 3–6%/s | só 1 punch-in (~120%); selfie em mão |
| Loudness | −24,5 LUFS | −18,1 LUFS |
| Duração/estrutura | 65 s, gancho → história longa → solução → produto → CTA | 36 s, gancho situacional → virada → 20 s de produto → CTA |
| Final | 3 quadros pretos | corta no último quadro |

### Notas para replicar (Remotion + B-roll de IA)
- Gerar páginas de legenda por frase a partir do `palavras.json` (quebrar em vírgula/ponto). Revelar cada palavra em `s − 1 quadro`. Página zera no corte.
- Componente `BlurEmphasis` (mesmo vídeo com `filter: blur(30px)` + texto grande centralizado + cor de destaque), `FlashTransition` (desfoque de 0→20 px e branco de 0→1 em 2 quadros, 2 quadros brancos, saída seca) e `BlackKaraoke` (página inteira, palavra ativa em limão).
- Tela dividida: TH em cima (com crop no rosto), máscara de gradiente preto de y 700→1000 e B-roll de y≈1010 a 1920; legenda na junção.
- O B-roll de IA pode substituir o de banco nos mesmos papéis (dinheiro indo embora, celular com WhatsApp, relatório, HUD de dados), mas o produto deve vir do kit verde #091B15 + Poppins.
- Pelas regras do estúdio (vídeo intocável), os jump cuts por frase não podem ser feitos; replicar o ritmo com mudança de punch-in/zoom e eventos sobrepostos a cada ~2 s, nos inícios de frase.
