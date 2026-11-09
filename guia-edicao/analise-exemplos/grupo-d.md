# Grupo D: análise forense de 16-09, beeno 08-09 e beeno 10-09

Todos os vídeos têm 1080x1920, 30 fps, HEVC, áudio AAC 44,1 kHz estéreo. O mesmo apresentador (camiseta verde, crachá Blip, óculos) segura um microfone de lapela sem fio diante da câmera. É selfie de celular gravada em evento (Blip ID / estande WhatsApp). O ritmo de fala é alto, de 3,6 a 4,1 palavras/s. Nenhuma pausa passa de 0,42 s, o que indica pausas cortadas.

Tempos vêm de scdet, de tiras quadro a quadro a 30 fps e de `palavras.json` (whisper). Medidas em px referem-se ao quadro 1080x1920.

---

## 1. 16-09 (40,94 s): "Tá vendo esse logo aqui atrás de mim?"

### Resumo e estrutura
- **Gancho (0–5,3 s):** usa o cenário como gancho. "Tá vendo esse logo aqui atrás de mim? Se a sua empresa vende por aqui, presta ATENÇÃO nos próximos 30 segundos."
- **Problema (5,3–21,7 s):** "O WhatsApp virou o principal canal de vendas... a maioria trata como caixa de mensagens... conversa espalhada... follow-up que ninguém faz... no fim do mês o número não veio. Canal de venda sem CRM não é canal de venda, é APOSTA."
- **Solução / produto (21,7–34,1 s):** "Esse é o motivo do Beeno existir. Um CRM nativo integrado com a Blip... funil, automação de follow-up, distribuição do lead, visibilidade ponta a ponta."
- **CTA (34,1–40,57 s):** "Se você quer saber mais... clica no link aqui que eu mesmo vou fazer uma demonstração." Fecha com 0,37 s de preto.

### Lista de planos
TH significa talking head. A escala é a largura dos óculos medida em % da largura do quadro: plano aberto ≈ 36–37%.

| # | início–fim (s) | dur | tipo | enquadramento / conteúdo |
|---|---|---|---|---|
| 1 | 0,00–1,53 | 1,53 | TH aberto (100%) | Rosto centralizado, logo WhatsApp/Meta atrás. Legenda de 3 linhas. |
| T | 1,47–1,57 | 3 f | transição | 1 quadro desfocado, 1 quadro **branco puro**, corte |
| 2 | 1,57–3,20 | 1,63 | TH **punch-in ~145%** | Rosto grande (óculos 52% da largura), olhos em y≈38% |
| 3 | 3,20–5,30 | 2,10 | TH aberto (≈100%) | **"ATENÇÃO"** vermelho gigante **atrás da cabeça** (o cabelo encobre as letras). Entrada com brilho/faísca de fogo laranja em ~6 quadros. Ao fim, quadro de bloom de exposição. |
| 4 | 5,33–17,83 | 12,50 | **Gráfico em tela cheia** | Animação vetorial escura (ver §5), cerca de 7 momentos internos |
| 5 | 17,83–20,70 | 2,87 | TH médio (100%) | Legenda em bloco **alinhado à esquerda**, "SEM CRM" em caixa alta mais pesada |
| 6 | 20,70–21,67 | 0,97 | mesmo take **desfocado** | Palavra **"APOSTA"** grande com entrada em eco/estiramento horizontal. Impacto grave. |
| 7 | 21,67–23,53 | 1,86 | TH médio | "esse é o motivo do beeno existir". Sai com 3 quadros de bloom de exposição e corte para o escuro. |
| 8 | 23,60–34,10 | 10,50 | **Gráfico de produto** | Prints de UI Blip + Beeno, zooms, popups e KPIs com contagem |
| 9 | 34,10–37,75 | 3,65 | TH médio | Início do CTA |
| T | 37,63–37,87 | 7 f | transição flash | Desfoque em 2 quadros, 1 quadro branco, branco a ~85% sobre o novo plano |
| 10 | 37,87–38,83 | 0,96 | TH punch-in ~120% | "clica no link aqui" |
| 11 | 38,83–40,57 | 1,74 | TH punch-in ~125% (jump cut) | "que eu mesmo vou fazer uma demonstração" |
| 12 | 40,57–40,94 | 0,37 | preto | fim |

**Momentos internos do bloco gráfico 4.** Cada momento muda na palavra-chave:
- 5,33: fundo vazio, ícone WhatsApp verde com halo.
- 5,9: "O WhatsApp virou" em cinza pequeno, depois "o principal canal" em branco bold e "de vendas." em verde. Balões de mensagem flutuam ao redor e o badge de notificação conta 1→4→12→19.
- 8,0: painel "Conversas" com o contador "41 não lidas" subindo até 223, linhas de chat aparecendo, "caixa de mensagens.".
- 11,0: três celulares inclinados (Vendedor 1/2/3), "✗ conversa em cada celular".
- 13,4: chips "Follow-up" aparecem nos celulares, "✗ follow-up que ninguém faz".
- 14,7: calendário "MÊS 01→08→29→30" com barra de meta 5%→51%→58% subindo. No dia 30 o cabeçalho fica vermelho, aparece a caixa tracejada "?" e "o número **não veio.**" em vermelho.

**Momentos internos do bloco gráfico 8:**
- 23,6: print da caixa de entrada da Blip, lockup "blip ⇄ beeno" desce com fade, "um CRM nativo / integrado com a **Blip.**" (Blip em azul).
- 25,9: câmera dá zoom no painel lateral Beeno, cursor clica "+Negócio", "Cada conversa vira **oportunidade.**".
- 27,6: quadro "Negócios" (kanban), lista ✓ se monta: "dentro de um funil".
- 28,5: popup escuro "Follow-up automático" (Dia 1 WhatsApp enviado / Dia 3 E-mail enviado / Dia 5 Ligação agendado).
- 30,0: popup "Distribuição automática" (Ana/Bruno/Carla com contadores).
- 31,4: zoom out para o kanban inteiro, KPIs contam 29→48→49 negócios, R$369→606→614 mil, R$157→258→262 mil, "visibilidade de / **ponta a ponta** / para o time comercial.".

### Ritmo
- **Talking head:** 9 segmentos, média 1,9 s, mínimo 0,96 s, máximo 3,65 s.
- **Gráficos:** 23,0 s, ou seja **56%** do vídeo, em dois blocos longos de 10–12 s com momentos internos a cada 1,2–2,5 s.
- **Escala:** o enquadramento alterna 100% e 120–145%. Cada novo corte de TH muda a escala, sem jump cut no mesmo enquadramento.
- **Posição dos cortes:** caem 0–0,05 s antes do início da primeira palavra da frase seguinte, no fim da frase anterior. Exemplos: corte 5,33 / "O" 5,32; 17,83 / "Canal" 17,86; 23,60 / "Um" 23,60; 34,10 / "Se" 34,10.

### Legendas
- **Fonte:** sans de sistema estilo **SF Pro Display Semibold**, com "a" de dois andares. É o "System" do CapCut/iOS.
- **Estilo:** branco #FFFFFF, sem contorno, sombra quase imperceptível, caixa baixa, sem pontuação final na maioria.
- **Tamanho:** altura da x ≈ 46 px e ascendente+descendente ≈ 77–80 px, ou seja corpo ≈ **80–84 px** (~7,5% da largura). Entrelinha ≈ 100 px.
- **Posição:** centralizada em x≈540, bloco entre y≈1420 e 1610 (74–84% da altura), sobre o peito, abaixo do queixo. Linha máxima de ~956 px (89% da largura).
- **Revelação:** **palavra por palavra, acumulando**. A palavra aparece no quadro exato do início dela, sem fade nem pop, e o bloco centralizado recentraliza ao crescer. Até ~3–4 palavras por linha e **até 3 linhas**. O bloco é zerado no início de cada frase ou corte.
- **Ênfase (bloco 5):** layout alinhado à esquerda em x≈60. "canal de venda" regular; **"SEM CRM"** em caixa alta Bold/Heavy ~1,3× maior (altura de caixa alta 65 px contra 48 px); "não é canal de venda" regular.
- **Palavras de impacto viram tipografia própria e substituem a legenda:**
  - "ATENÇÃO": grotesca black (Arial Black / Helvetica Black), vermelho **#D1000C**, caixa alta, x 132–945 (75% da largura), y 498–649, **atrás do sujeito** (precisa de máscara de segmentação).
  - "APOSTA": sans black branco ~110 px de caixa alta, y≈980, sobre fundo desfocado.
- **Números por extenso** ("trinta segundos") e marca em minúscula ("beeno").
- **Sem emoji.**
- **Sem legendas durante os gráficos:** o texto do gráfico substitui a legenda.

### Elementos gráficos (padrão "Beeno dark")
- **Fundo:** #04100C quase preto esverdeado, com brilho radial no centro #022014 e uma **grade fina** sutil (linhas ~2–3% mais claras, célula de ~40 px).
- **Tipografia dos gráficos:** **Poppins** ("a" de um andar).
  - Linha de abertura: ~44 px Medium, cinza-verde **#8CA69E–#98AEA6**, em y≈1305–1345.
  - Título: ~84–90 px **Bold** branco **#FAFFFE**, em y≈1390–1490.
  - Palavra de destaque no título: verde **#45D49E** (positivo), vermelho **#EF404A** (perda) ou azul Blip **#2A8EF6**.
  - Listas: ~50 px SemiBold **#D5EBE5**, ícone ✗ vermelho #D94852 ou ✓ verde #15A56B.
- **Ilustração:** ocupa y≈200–1150. São mockups de UI em cards escuros com bordas verdes de 1 px e brilho, ícone WhatsApp #1AAA49 com halo, badges vermelhos com contadores, prints reais de UI (Blip desk, Beeno) em cards brancos com cantos arredondados (~16 px) e sombra.
- **Animação:**
  - Texto entra com fade e subida de ~20–30 px em 6–8 quadros.
  - A linha anterior escurece ou fica cinza quando entra a seguinte.
  - Contadores sobem.
  - A barra de progresso enche.
  - A câmera dá push/zoom dentro do print, com cursor clicando.
  - Popups entram com scale e fade e saem com fade (ficam fantasma por ~3 quadros).
- **Logo:** lockup "blip ⇄ beeno" só no bloco de produto (24 s). Não há cartela de logo nem logo no fim.
- **Cor da filmagem:** natural, sem P&B. A filmagem não tem LUT; só os gráficos são verdes.

### Transições e efeitos
- **"Flash branco com desfoque"** (1,5 s e 37,7 s): rampa de desfoque em 1–2 quadros, 1 quadro 100% branco, 1 quadro branco ~85% sobre o novo plano, depois o plano limpo. Total de 4–5 quadros.
- **Bloom/estouro de exposição** antes de cortar para o gráfico escuro (5,30 e 23,5 s): 2–3 quadros clareando, depois corte seco para o fundo vazio. O gráfico começa vazio por ~6 quadros.
- **Do gráfico para o TH:** corte seco (17,83 e 34,10).
- **Desfoque de ênfase** (20,70–21,67): o fundo vira gaussiano forte (~20–30 px) e a palavra entra com eco/estiramento (cópias espaçadas que convergem em ~0,3 s). Volta nítida com corte seco.
- **Texto atrás do sujeito com entrada de fogo/brilho** (3,20).
- Sem shake, whip ou glitch digital. Talking head estático, sem drift de zoom.

### B-roll
Nenhum B-roll de banco nem de IA. Todo o visual de apoio é **motion graphic vetorial**, entre o literal e a metáfora de interface (celulares, kanban, calendário). A voz continua por cima. O texto do gráfico é uma paráfrase curta da fala e aparece na palavra dita.

### Áudio
- **Volume:** −18,6 LUFS, LRA 5,1, pico −0,2 dBFS. Nenhum silêncio abaixo de −40 dB (há ambiente de feira o tempo todo).
- **Impactos graves (40–110 Hz)** em 0,15 s (abertura), 3,15–3,35 (ATENÇÃO), 15,65 (dia 30 vermelho / "não veio"), 18,6 (SEM CRM) e 20,75–20,95 (APOSTA). São **SFX de boom/impacto em cada momento tipográfico de ênfase**.
- **Trilha:** sem batida clara (autocorrelação 0,09). No máximo uma trilha muito baixa ou nenhuma.

### Final
CTA falado com punch-in progressivo (120% e depois 125%). Corta no fim da última palavra +0,17 s, depois 0,37 s de preto. Sem cartela final.

---

## 2. beeno 08-09 (49,81 s): "Deixa eu te contar por que a gente trouxe o Beeno para o Blip ID"

### Estrutura
- **Gancho / contexto (0–11,4):** "Deixa eu te contar por que trouxemos o Beeno para o Blip ID, o maior evento conversacional do Brasil... o WhatsApp é onde a venda acontece e a Blip é onde a conversa acontece com inteligência."
- **Pergunta-ponte (11,4–16,5):** "Só que aí vem a pergunta que eu mais escuto: BELEZA, O LEAD CHEGOU PELO BLIP, E AGORA?"
- **Problema (16,5–24,0):** "é onde a maioria perde dinheiro. O lead entra, a conversa é ótima e some. Sem funil, sem cadência..."
- **Solução (24,0–41,2):** "é exatamente esse buraco que o Beeno resolve. A GENTE NÃO É MAIS UM CRM GENÉRICO... extensão nativa... sem sair da plataforma."
- **CTA (41,2–49,8):** "Se você não teve a oportunidade de conhecer a gente aqui pessoalmente, agenda uma reunião..."

### Lista de planos
Fundo de parede lilás/violeta com o logo "blip id". Base: óculos ≈ 40% da largura.

| # | início–fim | dur | tipo | notas |
|---|---|---|---|---|
| 1 | 0,00–5,00 | 5,00 | TH base (100%) | Legenda logo abaixo do queixo |
| T | 4,93–5,10 | 5 f | flash de exposição | Clareia em ~3 quadros, quadro estourado, novo plano entra claro e decai em ~2 quadros |
| 2 | 5,07–8,23 | 3,16 | TH ~110% | |
| 3 | 8,23–11,40 | 3,17 | TH ~110%, enquadramento deslocado | Jump cut seco |
| T | 11,30–11,47 | 5 f | flash de exposição | idem |
| 4 | 11,47–12,37 | 0,90 | TH ~100% | |
| 5 | 12,37–13,83 | 1,46 | TH punch-in ~120% | |
| 6 | 13,83–16,47 | 2,64 | **mesmo take, ainda mais aberto (mostra o teto preto) e muito desfocado** | Tipografia **larga/expandida** em caixa alta, estilo karaokê com contorno (ver §4). Centro y≈925–1000. |
| 7 | 16,47–18,13 | 1,66 | TH ~110% | "e agora é onde a maioria perde dinheiro" |
| 8 | 18,13–24,00 | 5,87 | **gráfico em tela cheia** | "O lead entra. / A conversa é ótima. / **E some.**" e depois a lista ✗ |
| 9 | 24,00–26,83 | 2,83 | TH ~110% | |
| 10 | 26,83–28,70 | 1,87 | mesmo take **desfocado** | **Serifada caixa alta com efeito máquina de escrever** e cursor em bloco ▌: "A GENTE NÃO É MAIS / UM CRM GENÉRICO" |
| 11 | 28,70–31,83 | 3,13 | TH | |
| 12 | 31,83–39,23 | 7,40 | **faixa de produto** | Painel escuro horizontal em y **426–1610** (1184 px, 62% da altura) sobre o take **aberto e desfocado** (teto em cima, camiseta embaixo). Sem legendas. |
| 13 | 39,23–41,17 | 1,94 | TH punch-in ~122% | "e é tudo isso sem sair da plataforma" |
| T | 41,10–41,30 | 6 f | flash de exposição | |
| 14 | 41,30–42,57 | 1,27 | TH | |
| 15 | 42,57–45,57 | 3,00 | TH | corte seco |
| 16 | 45,57–49,81 | 4,24 | TH | Termina no rosto, sorriso de boca fechada após a última palavra (49,46). Sem cartela. |

**Momentos internos do gráfico 8:**
- 18,13: fundo vazio por ~6 quadros.
- 18,4: um ponto verde cai do topo com rastro e brilho, "O lead entra." em cinza.
- 18,9: balões de chat saem do ponto, "A conversa é ótima.".
- 19,7: "**E some.**" em bold branco, o ponto se dissolve em partículas.
- 20,4: "✗ sem funil", pontos espalhados.
- 21,0: "✗ sem cadência", trilha de pontos de cadência.
- 22,4: "✗ sem saber o que fechou", caixas tracejadas "FECHOU ? / FICOU PARA TRÁS ?".
- 23,2: "✗ nem o que ficou para trás".

**Momentos internos da faixa de produto 12:**
- 31,9–33,3: aparece o ticket da Blip "Vitor Gutierrez" e as mensagens surgem uma a uma.
- ~33,4: o painel lateral Beeno (cabeçalho verde) **desliza da direita** e é preenchido (dados do contato, +Negócio, +Tarefa, +Nota, "Skeps – 40 licenças / Proposta enviada").
- ~36,0–37,5: chips de recurso entram um por vez acima do print: "• Ficha do contato", "• Cria negócio na hora", "• Histórico do ticket sincronizado". Pílulas escuras com ponto verde, Poppins SemiBold branco ~34 px.

### Ritmo
- **Talking head:** 14 segmentos, média ≈ 2,6 s, mínimo 0,90 s, máximo 5,0 s.
- **Gráficos e faixa de produto:** 13,3 s, ou seja 27%.
- **Momentos de tipografia sobre desfoque:** 2 (4,5 s).
- **Escala:** alterna 100%, ~110% e ~120%.
- **Posição dos cortes:** sempre na fronteira de frase, 0–0,1 s antes da palavra (5,00 / "Aqui" 5,06; 18,13 / "O" 18,12; 24,00 / "É" 24,16; 31,83 / "Através" 31,88; 45,57 / "agenda" 45,58).

### Legendas
- **Fonte:** **Montserrat Bold**, diferente de 16-09 e 10-09.
- **Estilo:** branco #FEFEFD com **sombra suave escura** (blur ~6 px, ~40%), sem contorno.
- **Tamanho:** ascendente+descendente 59–73 px, corpo ≈ **70–72 px**. Entrelinha ≈ 97 px.
- **Posição:** centralizada, bloco entre y≈1370 e 1540 (71–80%). Varia ±50 px entre planos para ficar abaixo do queixo.
- **Revelação:** palavra por palavra acumulando, até 3 linhas, sem animação. Some em pausas e cortes.
- **Caixa:** caixa baixa, com inicial maiúscula só no início ("Deixa..."). "Beeno" capitalizado.
- **Sem destaques de cor** nas legendas normais.
- **Tipografias especiais (substituem a legenda):**
  - **(a) Pergunta do cliente** (13,83–16,47): sans **extra larga/expandida black** (tipo Monument Extended / Unbounded Black / Lemon Milk), caixa alta, ~75 px de altura, até 2 linhas.
    - **Karaokê invertido:** a palavra falada fica **branca sólida** e as demais ficam **vazadas** (só contorno branco de ~4 px).
    - Avança por palavra: "BELEZA, O LEAD" / "CHEGOU PELO BLIP" / "E AGORA?".
    - Posição y≈925–1000, sobre o rosto desfocado.
  - **(b) Frase de posicionamento** (26,83–28,70): **serifada clássica** (tipo Times / Libre Caslon / Cormorant SemiBold), caixa alta, branco com sombra suave, ~62 px de caixa alta, 2 linhas centralizadas em y≈887–1034.
    - Efeito **máquina de escrever, letra por letra, com cursor em bloco** branco piscando, sincronizado com a fala (~11 caracteres/s).

### Gráficos
- **Fundo:** #091C16 com brilho radial verde #09402D no centro e grade fina.
- **Tipografia:** a mesma do sistema de 16-09, Poppins.
  - Linhas narrativas centralizadas ~44 px em cinza **#A9BAB3** ("O lead entra. / A conversa é ótima.").
  - Golpe em ~60 px Bold branco ("E some.").
  - Lista ✗ ~46 px SemiBold **#E2EDE8** com ✗ **#E36A6E**, alinhada à esquerda em x≈340.
- **Motivo:** um nó/ponto verde brilhante que representa o lead.
- **Faixa de produto:** prints reais de UI (Blip desk + extensão Beeno), cantos ~12 px e sombra.

### Transições
- **Flash de exposição curto** (não chega a branco puro, ~5 quadros) em 5,0, 11,4 e 41,2.
- Corte seco nas demais, inclusive na entrada e saída dos gráficos e dos momentos com desfoque.
- **Momentos com desfoque:** o take recua para ~100% de escala, mostrando mais do teto, e recebe desfoque gaussiano forte. Começam com 1 quadro de rampa de desfoque.

### B-roll
Nenhum. Só gráficos e prints.

### Áudio
- **Volume:** −15,0 LUFS, LRA 2,9, pico +0,3 dBFS. Sem silêncios.
- **Trilha:** **batida a 120 BPM** (bumbo a cada 0,50 s, autocorrelação 0,28) **começa exatamente em ~16,5 s**, no corte que sai de "E AGORA?", e segue até o fim. Os primeiros 16 s não têm batida. A trilha entra na virada para o problema.

### Final
Fala do CTA no rosto. Termina 0,35 s após a última palavra, com um olhar parado. Sem cartela final nem logo.

---

## 3. beeno 10-09 (45,19 s): "Se você usa Blip... achar que ter Blip é ter um CRM"

### Estrutura
- **Gancho (0–4,8):** "Se você usa Blip na operação, deixa eu te contar uma confusão que custa caro pra muita empresa."
- **Equívoco (4,8–7,3):** "achar que ter Blip É TER UM CRM", com um X vermelho desenhado à mão por cima. "E não é."
- **Explicação (7,3–31,5):** "não é porque um é melhor... são coisas diferentes, da mesma jornada", seguido do bloco gráfico de 20 s sobre Blip × Beeno.
- **Fórmula (31,5–36,1):** "O Blip conversa, o Beeno converte. Juntos vira uma operação de vendas de verdade."
- **CTA (36,1–45,2):** "Se você já usa a Blip e seu lead ainda some... clica aqui no link abaixo, agende uma demo..."

### Lista de planos
Filmado no corredor do evento, com público ao fundo. Óculos ≈ 35–37%. **Sem punch-in**: escala constante.

| # | início–fim | dur | tipo | notas |
|---|---|---|---|---|
| 1 | 0,00–4,80 | 4,80 | TH (100%) | |
| T | 4,70–4,87 | 5 f | **flash branco com desfoque** | Rampa de desfoque em 2 quadros e 2 quadros brancos (a nova legenda "achar" já aparece no branco) |
| 2 | 4,87–7,30 | 2,43 | mesmo take **desfocado** | Legenda sobe para y≈700–990. "achar que ter blip" em regular e **"É TER UM CRM"** em Bold caixa alta. Em 6,6–7,0 um **X vermelho #E90002** é **desenhado traço a traço**: traço 1 da esquerda para baixo em ~0,2 s, traço 2 em ~0,15 s. Segura até o corte. Com SFX de rabisco. |
| 3 | 7,30–8,57 | 1,27 | TH nítido | "e não é" |
| 4 | 8,57–11,67 | 3,10 | TH (jump cut) | |
| 5 | 11,67–31,53 | 19,86 | **gráfico em tela cheia** | Começo com fundo vazio de ~6 quadros e logo da Blip entrando com fade |
| T | 31,53–31,60 | 2 f | flash branco | Quadro branco com o rosto vazando, entra o TH |
| 6 | 31,60–36,07 | 4,47 | TH | "o blip conversa / o Beeno converte / juntos..." |
| 7 | 36,07–40,30 | 4,23 | TH (jump cut sutil) | |
| 8 | 40,30–43,10 | 2,80 | TH (jump cut) | "clica aqui no link abaixo" |
| 9 | 43,10–45,19 | 2,09 | TH (jump cut) | Corta 0,19 s após "funciona". Sem cartela. |

**Momentos internos do gráfico 5.** Duas cores por marca:

Parte **Blip** (11,7–22,3): brilho **azul-petróleo** #082E37 sobre a base #0A1F1A.
- Logo blip branco + balão azul **#0C94F8** no topo, ~200 px de altura.
- 12,0: "O Blip é o canal.", ~80 px Poppins Bold branco em y≈1290.
- 13,2: "✓ a inteligência da conversa" + cards de conversa.
- 14,7: "✓ o atendimento que escala" + grade 4×5 de cards.
- 16,0: "✓ o lead qualificado no WhatsApp". Os cards se fundem num **nó azul com check**.
- 17,9: o texto troca em crossfade para "Isso o Blip faz muito bem.".
- 19,6: o logo some e o nó sobe, "E depois?" + caixa tracejada vazia com "?" + "A conversa precisa virar negócio." em cinza #88938E.

Parte **Beeno** (22,3–31,5): o brilho vira **verde** #083D2B.
- 22,3: "É aí que entra o Beeno." O card Beeno (cabeçalho verde #1BC186, chip blip, +Negócio/+Tarefa) desliza e se conecta ao nó por linha tracejada. O nó fica verde.
- 23,9: "O lead vira pipeline.", kanban de 4 colunas (Lead recebido / Qualificação / Proposta / Fechado). O card do lead anda entre as colunas.
- 26,5: "✓ cadência" + trilha de 5 pontos de progresso que se preenche.
- 27,5: "✓ follow-up no tempo certo".
- 28,5–29,0: o card chega a "Fechado" com anel de pulso e o selo "Fechado ✓", "✓ caminha até o fechamento".
- 29,9: "**Sem se perder no meio.**" em verde-menta **#5EDDB1**, ~80 px.

### Ritmo
- **Talking head:** 8 segmentos, média ≈ 3,2 s, mínimo 1,27 s, máximo 4,80 s. É o vídeo mais calmo.
- **Gráfico:** 19,9 s contínuos (44%), com 14 momentos de ~1,0–2,0 s.
- **Jump cuts:** no mesmo enquadramento, só para tirar pausa (7,30; 8,57; 36,07; 40,30; 43,10).
- **Posição dos cortes:** sempre no início da frase (4,87 / "Achar" 4,80; 11,67 / "O" 11,64; 31,53 / "O" 31,56; 40,30 / "Clica" 40,32).

### Legendas
- **Fonte:** **SF Pro Semibold**, a mesma de 16-09.
- **Estilo:** branco, sem contorno.
- **Tamanho:** ~80 px (altura ascendente–descendente 70–74 px).
- **Posição:** centralizada em y≈1447–1566 (75–82%).
- **Revelação:** palavra por palavra, até 3 linhas.
- **Caixa:** caixa baixa, "Se" maiúsculo no início, "blip" minúsculo.
- **Ênfase:** linha em **SF Pro Bold caixa alta** (altura de caixa alta 57 px) dentro do bloco. Na tela com desfoque a legenda sobe para o centro do quadro, y≈700–990.

### Áudio
- **Volume:** −13,6 LUFS, LRA 2,4, pico +0,1 dBFS.
- **SFX:** textura de **rabisco de marcador** em 6,6–7,1 s (banda 6–14 kHz, sincronizada com o X), **impacto grave** em 22,4 (entrada do card Beeno), outro em 26,45 (cadência) e um **toque tonal/sino** em ~29,3 (card em "Fechado").
- **Trilha:** sem batida detectável. Se houver, é muito baixa.

### Final
Corte seco no rosto ao fim da última palavra. Sem cartela.

---

## 4. Padrões entre os 3 vídeos

### O que se repete (base para replicar)
1. **Formato:** selfie de 40–50 s, um único apresentador, filmagem crua do evento sem color grade. A pós-produção é toda composição por cima.
2. **Arco fixo:** gancho de contexto (o lugar ou a "confusão"), problema com perda, frase-golpe, "é aí que entra o Beeno", benefícios em lista ✓, CTA falado ("clica no link / agenda") **sem cartela final nem logo**.
3. **Bloco gráfico em tela cheia de 6–20 s** (27–56% do vídeo) cobrindo **problema + solução**. A voz continua e a legenda some.
   - **Estilo dos gráficos:** fundo verde-quase-preto (#04100C a #091C16), brilho radial (verde #083D2B–#09402D, ou azul #082E37 para a Blip), grade fina, UI vetorial com bordas finas e brilho, nó/ponto brilhante como personagem "lead".
   - **Tipografia dos gráficos:** Poppins com hierarquia em 3 níveis: cinza #8CA69E–#A9BAB3 ~44 px, título branco #FAFFFE Bold ~84 px, palavra de destaque em verde #45D49E/#5EDDB1, vermelho #EF404A ou azul #2A8EF6.
   - **Listas ✓/✗:** ~48 px, construídas item a item na palavra falada.
   - **Momentos internos:** a cada 1–2,5 s, sempre na palavra-chave.
   - **Marcas:** prints reais de UI (Blip desk e extensão Beeno) com zoom, cursor, popups e contadores.
   - **Entrada:** começa com ~6 quadros de fundo vazio e o texto entra com fade+subida.
4. **Legenda dinâmica palavra por palavra, acumulando:** sem pop nem cor, branca, 70–84 px, centralizada a 72–82% da altura (sobre o peito), até 3 linhas de ~3–4 palavras, zerada a cada frase. A palavra aparece no início exato dela.
5. **Frase-golpe com fundo desfocado:** o mesmo take recua (fica mais aberto), recebe desfoque gaussiano forte (~20–30 px em 1080) e ganha uma tipografia especial grande no centro: APOSTA, BELEZA/E AGORA? e A GENTE NÃO É MAIS UM CRM GENÉRICO em karaokê ou máquina de escrever, ou "É TER UM CRM" com X desenhado. Dura de 1 a 2,6 s. Entra por corte ou flash e sai por corte seco.
6. **Transição característica: flash/estouro de exposição** com rampa de desfoque, 4–7 quadros, às vezes com 1–2 quadros de branco puro. Fica no início de frase, entre TH e TH, entre TH e desfoque, ou entre gráfico e TH. Para entrar no gráfico escuro: bloom curto e corte seco.
7. **Cortes no início da próxima frase** (0–0,1 s antes da palavra). As pausas são cortadas (gap máximo 0,42 s). Não há B-roll de banco nem de IA.
8. **SFX:** **impactos graves** nos momentos tipográficos, **rabisco** no X desenhado e **sino** no "Fechado". O ambiente do evento fica como piso (sem silêncios). LUFS integrado entre −13,6 e −18,6.

### O que varia
- **Fonte da legenda:** SF Pro Semibold (16-09, 10-09) ou Montserrat Bold com sombra (08-09).
- **Punch-ins:** forte em 16-09 (100↔120–145%), médio em 08-09 (100/110/120%) e ausente em 10-09 (só jump cuts).
- **Formato do gráfico:** tela cheia em 16-09 e 10-09. 08-09 também usa uma **faixa horizontal** (y 426–1610) sobre o take desfocado para o print do produto.
- **Trilha:** batida de 120 BPM só em 08-09, entrando na virada para o problema (16,5 s). 16-09 e 10-09 sem batida clara.
- **Ênfase na legenda:**
  - 16-09: bloco alinhado à esquerda com "SEM CRM" caixa alta ~1,3×, mais texto atrás do sujeito (ATENÇÃO #D1000C com fogo).
  - 10-09: linha Bold caixa alta "É TER UM CRM" e X vermelho #E90002 animado.
  - 08-09: tipografia expandida com contorno/karaokê e serifada com máquina de escrever.
- **Duração do bloco gráfico:** 2 blocos de 10–12 s (16-09), 1 de 6 s + faixa de 7,4 s (08-09), 1 contínuo de 20 s com troca de cor por marca (10-09).

### Receita de replicação (Remotion)
- **Legenda:** componente que lê `palavras.json`, agrupa por frase e quebra em ≤3 linhas de ≤24 caracteres, e mostra as palavras com `s <= t`. SF Pro Display/Inter SemiBold 80 px #FFF, centralizada em `top ≈ 1420`. Fica oculta nos gráficos e nos momentos especiais.
- **`EmphasisBlur`:** `<OffthreadVideo>` do mesmo trecho com `scale(0.9–1.0)` e `filter: blur(24px)`, mais tipografia central (karaokê com `-webkit-text-stroke: 4px #fff`, máquina de escrever com cursor, ou palavra única com eco). Entrada por `FlashTransition`.
- **`FlashTransition`:** 4–6 quadros: blur 0→12 px e brightness 1→3 no plano de saída, 1 quadro `#FFF`, depois branco com opacidade 0,85→0 sobre o plano de entrada.
- **`DarkScene`:** fundo #091C16, radial-gradient com #09402D a 40% do centro, grade de 40 px a rgba(255,255,255,0.03). Texto Poppins em 3 níveis com spring de opacidade e translateY 24 px→0 em 8 quadros. Gatilhos sempre pelo tempo da palavra.
- **Punch-in:** alternar `scale` 1,0 / 1,2 / 1,45 por segmento de TH, com âncora no rosto, a cada 1–3 s.
- **SFX:** boom grave nos momentos tipográficos, whoosh/bloom nas entradas de gráfico, rabisco no X, ding de sucesso. Batida de 120 BPM opcional a −28 dB a partir da virada para o problema.
