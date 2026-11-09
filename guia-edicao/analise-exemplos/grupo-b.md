# Análise forense: Grupo B (Criativo 04, Criativo 05, Reels 01)

Material: 1080x1920, 30 fps, HEVC (Main 10 nos Criativos, Main 8 no Reels), áudio AAC 44,1 kHz estéreo ~200 kb/s.
Método: contact sheets, frames em resolução cheia, tiras de 30 fps em cada transição, detecção de corte por diferença de quadro (mais sensível que o scdet), amostragem de pixels (PIL/numpy), espectrogramas e RMS. Os tempos de palavra vêm de `transcricao/palavras.json`. O Whisper errou alguns nomes ("Bino"/"Bleep"/"Segure"), mas as legendas do vídeo trazem "Beeno"/"Blip"/"Sincroniza".

Métrica de enquadramento usada abaixo: **G% = largura dos óculos ÷ largura do quadro**. É um bom substituto do tamanho do rosto, porque os três apresentadores usam óculos.

---

## 1. Criativo 04 (52,57 s): "Seu cliente já falou com a sua empresa 5 vezes…"

### 1.1 Resumo e estrutura
- Apresentadora em uma mesa de escritório (prateleira com "@", plantas, MacBook preto). Câmera fixa no tripé, várias tomadas e enquadramentos. Fala rápida, 3,45 palavras/s.
- **Gancho (0–6,1 s):** dor concreta com número ("5 vezes") e pergunta retórica ("como se fosse a primeira vez?"). Punch-in em P&B no "cinco vezes".
- **Produto (6,1–11,97 s):** transição blur+flash branco, logo "beeno", B-roll verde-escuro de mãos digitando no celular e a palavra-chave AUTOMATICAMENTE.
- **Problema/agitação (11,97–29,7 s):** tela dividida com stock de um homem ao telefone, depois uma "historinha" ilustrada (cliente × atendentes) e de volta à apresentadora ("o histórico fica preso no WhatsApp").
- **Solução (29,7–48,2 s):** flash, close em "o Beeno resolve isso", cartão preto com ícone de sincronizar, sequência de jump cuts listando o que o CRM mostra e um bloco de texto neon "glow" com os benefícios.
- **CTA (48,2–52,57 s):** apresentadora, "Clica no link e agenda uma reunião com a gente". Os últimos 0,54 s são **tela preta só com a legenda**.

### 1.2 Linha do tempo / shot list
| início–fim (s) | tipo | enquadramento | o que há na tela |
|---|---|---|---|
| 0,00–1,80 | talking head (TH) | médio, G≈18–20%, rosto no terço superior (olhos y≈330) | legenda branca y≈1125–1295 |
| 1,80–3,23 | punch-in **P&B** (dessaturado 100%, sat. média 1,1) | close, G≈35% | "5" e depois "5 vezes" em vermelho gigante (algarismo em vez de "cinco") |
| 3,23–6,13 | TH colorido | médio-close, G≈30% | "e o vendedor atende / como se fosse a / **primeira vez?**" (vermelho) |
| 6,13–6,40 | transição: blur crescente + estouro para branco (≈5 quadros 100% brancos) e volta já em outra tomada | — | legenda some no início do blur |
| 6,40–7,40 | TH plano aberto **desfocado** (blur gaussiano forte) | aberto | logo "beeno" (by skeps) entra grande e encolhe até 59% da largura, centro y≈850 |
| 7,40–10,90 | **B-roll** escuro com tom verde (mediana #061816): mãos digitando num smartphone, desfoque de fundo | detalhe | legenda no **topo** (y≈185–340); pequeno corte interno em 9,37 |
| 10,90–11,97 | TH | médio, G≈26% | "AUTOMATICAMENTE" em caixa alta, branco com contorno verde |
| 11,97–15,87 | **tela dividida** com fusão suave: em cima a TH (corte para close em 15,07), embaixo stock realista de um homem de terno ao telefone, gesticulando | metade de cima: TH, G≈21%→32% | fusão em gradiente de ~y 960 a ~1100 (≈140 px, sem linha dura). Legenda sobre a emenda; "TUDO DE NOVO" em vermelho caixa alta |
| 15,87–23,95 | TH desfocada + **ilustrações chapadas** estilo Irasutoya (clip art japonês) | fundo: planos abertos desfocados (troca de tomada no fundo em 20,57 e 22,5) | cliente com telefone no canto superior direito, atendente com headset no inferior esquerdo, balões de fala (vermelho "…", amarelo com linhas, verde-água "…", azul), avião de papel ("mandou dados"); em 20,8 o atendente vira outra pessoa ("cai com outra pessoa"); em 22,5 o cliente fica vermelho e bravo e surgem balões "?" ("não sabe de nada") |
| 23,95–29,73 | TH (1 quadro aberto e logo médio: "snap" de 2 cortes em 23,93/23,97) | médio, G≈27% | legenda inferior y≈1427–1491 |
| 29,73–29,90 | blur + flash branco (≈2–3 quadros brancos) | — | — |
| 29,90–31,00 | TH close | G≈41% | "o Beeno resolve isso". Blur de 1 quadro antes do corte |
| 31,00–34,60 | **cartão preto** #000000 | — | ícone branco de "sincronizar" (2 setas em círculo, ≈460 px = 43% da largura, centro y≈930) **girando**; legenda acima (y≈185–340) e depois abaixo do ícone (y≈1000–1200) |
| 34,60 / 35,37 / 36,83 / 37,90 / 38,70 / 40,33 | jump cuts de TH alternando escala | 29% → close → médio → médio → close → **aberto** (G≈18%, outra tomada com planta à esquerda) | listagem: "o que foi falado, quando, em que etapa…" |
| 41,27–45,00 | TH desfocada + **texto neon glow** centralizado | — | "Um atendimento / com contexto" (verde neon / branco), "cliente que / não precisa", "**se repetir**" (vermelho glow) |
| 45,00–48,20 | TH | médio | "e um time que parece que sempre soube…" |
| 48,20 / 50,10 / 50,70 | TH, CTA | médio → médio iluminado (mais quente e claro) → close | legenda |
| 52,03–52,57 | **preto** | — | só a legenda "e agenda uma / reunião com a gente" |

### 1.3 Ritmo
- 25 cortes, 26 segmentos: média 2,02 s, mediana 1,46 s, mínimo 0,54 s, máximo 5,87 s (≈28,5 cortes/min).
- **Cortes caem no início de uma palavra:** mediana de |offset| = 0,06 s, 21 de 25 a até 0,1 s do início da palavra, quase sempre no começo de uma frase ou oração.
- Pausas removidas: só uma pausa acima de 0,3 s no vídeo inteiro (0,42 s em 38,26). Os jump cuts ficam escondidos porque **cada corte muda a escala**: aberto (G≈18%) ↔ médio (≈27–30%) ↔ close (≈35–41%), ou seja, cerca de 100% ↔ 150% ↔ 200%. Não há zoom contínuo (Ken Burns): a comparação de quadros em 24,05 s e 29,6 s deu escala 1,00 e deslocamento 0.

### 1.4 Legendas / tipografia
- **Padrão:** Montserrat Bold (700), minúsculas como na fala, branco puro #FFFFFF, **sem contorno**, sombra projetada suave (~3–4 px para baixo e à direita, desfocada, ~40–50% preto).
  - Tamanho ≈74 px (altura de maiúscula ≈52 px, altura-x ≈40 px), entrelinha ≈96 px (≈1,3).
  - Linha de até ~810 px (≈75% da largura), centralizada. Até 3 linhas por bloco, normalmente 2, cerca de 3–5 palavras por linha.
- **Revelação:** palavra por palavra, acumulando, cada palavra surge seca (sem pop, escala ou fade) uns 0,05–0,2 s depois do início dela. **O layout final já está calculado:** as palavras aparecem nas posições definitivas, sem refluxo. A frase inteira some e é trocada no começo da frase seguinte.
- **Posição:** variável, para fugir do rosto e dos gráficos. Na TH fica na altura do peito/mãos (y≈1125–1500). No B-roll e no cartão preto, no topo (y≈185–340). No split, sobre a emenda (y≈950–1000).
- **Regras de destaque:**
  - **Vermelho #EC1D1D** para dor ou negação: "primeira vez?", "TUDO DE NOVO" (caixa alta), número "5 vezes" (algarismo de ~120 px de altura, ≈170 px de corpo, Montserrat ExtraBold/Black, com sombra).
  - **Verde da marca #02CD8B** como contorno (~4 px) em texto branco caixa alta: "AUTOMATICAMENTE".
  - **Estilo glow** (41–45 s): outra fonte, arredondada e muito pesada (tipo Fredoka/Nunito Black), centralizada em y≈880–1060. A linha falada no momento fica **verde neon #17FF17**, com contorno verde-escuro e brilho externo verde; a outra linha fica branca, com contorno cinza e brilho branco (destaque karaokê por linha). "se repetir" em **vermelho #F71616** com brilho vermelho. O bloco refaz a quebra de linha e pulsa de escala na troca (3 linhas → 2).
- Sem emoji. A marca aparece escrita "Beeno" na legenda.

### 1.5 Elementos gráficos
- **Logo:** "beeno" verde #00CB88 + "by skeps" branco pequeno embaixo à direita. Largura ~633 px (59%), centralizado em x e y≈850. Entra com **zoom-out a partir de muito grande** (≈3x, cortado nas bordas), com blur de movimento, e assenta em ~8 quadros (0,27 s). Fica sobre a TH desfocada por 1 s. Aparece em 6,4 s, no "conheça", 0,6 s antes do "Bino".
- **P&B** só no gancho, como ênfase do número da dor.
- Ilustrações estilo Irasutoya com entrada deslizando (o cliente de cima, o atendente de baixo) e blur de movimento direcional, ~9 quadros (0,3 s) com leve overshoot. Os balões entram em escala.
- Ícone de sincronizar girando sobre preto, estilo ícone outline branco.
- Não há barra de progresso, sticker ou print do produto.

### 1.6 Transições e efeitos
- Corte seco na maioria das vezes.
- **Blur + flash branco** duas vezes (6,13–6,40 e 29,73–29,90): ~3 quadros de blur crescente com ganho de brilho, 2–5 quadros 100% brancos e 1–2 quadros de "revelação" desfocada. Serve para marcar o virar de capítulo (gancho → produto, problema → solução).
- **Blur de 1 quadro** antes do corte para o cartão preto (30,97).
- Corte "snap" de 2 quadros em 23,93 (1 quadro aberto e depois médio).
- O fundo desfocado vira palco de gráficos: 6,4–7,4, 15,87–23,95 e 41,27–45,0.
- Sem shake, glitch ou speed ramp. Sem vinheta perceptível.

### 1.7 B-roll
- 7,40–10,90 (3,5 s): mãos em smartphone, escuro, graduado em verde-petróleo. Parece stock (ou IA) com grade verde forte e profundidade de campo rasa. A voz continua, a legenda vai para o topo. Relação semi-literal com a fala ("puxa o histórico de conversa").
- 11,97–15,87 (3,9 s): stock realista (homem de terno ao telefone, cenário branco), metade de baixo do split. Literal: o cliente explicando de novo.
- 15,87–23,95 (8,1 s): ilustração 2D como storytelling literal frase a frase.

### 1.8 Áudio
- **Trilha de fundo contínua:** banda limitada a ~15,4 kHz (típico de MP3) por baixo da voz, sem nenhum silêncio abaixo de −40 dB. A banda de 40–150 Hz tem o mesmo nível com e sem fala (14,7 vs 15,0 dB rel.). Na cauda preta (52,0–52,55) a trilha sozinha fica em **−37 dBFS**, contra fala ≈−22 dBFS: trilha ~15 dB abaixo da voz.
- **SFX prováveis:** faixa larga até 19 kHz em ~2,0 s (impacto no punch P&B do "cinco"); whoosh/riser largo em 6,05–6,40 (−22 dBFS num trecho quase sem fala) coincidindo com o flash; nova faixa larga perto de 29,7 (segundo flash).

### 1.9 CTA / final
- Apresentadora sorrindo, legenda "Clica no link e agenda uma reunião com a gente". A imagem corta para **preto em 52,03** e a legenda fica sozinha sobre o preto até o fim. Não há cartão final, logo nem URL.

### 1.10 Distintivo
Vídeo de maior "produção" do grupo: combina 4 linguagens (P&B com número, logo, ilustração 2D narrativa, cartão preto com ícone, texto glow neon). Usa o vermelho de forma sistemática para dor e o verde para solução.

---

## 2. Criativo 05 (23,52 s): "Se a sua empresa usa Blip… e seu CRM é HubSpot, RD Station…"

### 2.1 Resumo e estrutura
- Apresentador de camisa polo preta, mesmo cenário ("@", plantas), MacBook prata. Câmera fixa. Fala de 3,85 palavras/s.
- **Gancho/qualificação (0–5,43 s):** chama o público pelas ferramentas que usa (Blip + HubSpot/RD Station), com os logos aparecendo numa tela de notebook.
- **Confronto (5,43–8,37 s):** "Desculpe, mas você não tá aproveitando nem metade do potencial", em **P&B** com legenda amarela.
- **Solução (8,37–20,03 s):** "porque nenhum deles faz o que o Beeno faz de forma nativa na Blip". Logo sobre a TH, depois fundo desfocado + logo central + 4 ícones de funcionalidade, um por benefício.
- **CTA (20,03–23,52 s):** "Quer ver o que você tá perdendo? Clica aqui no link e eu te mostro como funciona". Termina na TH, sem cartão final.

### 2.2 Shot list
| início–fim (s) | tipo | detalhe |
|---|---|---|
| 0,00–5,43 | **split vertical** com fusão em gradiente (~y 900–1000) | em cima a TH (corte do peito para cima). Embaixo, **B-roll POV de mãos digitando num notebook**, luz quente/laranja lateral, tela branca com logo composto: **Blip** (0–2,5) → **HubSpot** (2,5, na palavra "HubSpot" em 2,52) → **RD Station** (3,4, na palavra "RD" em 3,38). Troca por whip horizontal com blur de movimento (~6 quadros, 0,2 s), e o logo novo desliza e assenta. Legenda na emenda (y≈886–1000) |
| 5,43–8,37 | punch-in **P&B** | close, G≈37%. Legendas **amarelas** |
| 8,37–11,03 | TH colorida | médio, G≈29%. Em **9,27** (na palavra "Beeno") o logo "beeno" entra **sobre a TH nítida**, centro y≈920, 633 px (59%), por esticamento/whip horizontal com blur de movimento (~4 quadros) |
| 11,03–16,77 | TH **desfocada** (outra tomada, aberta) + logo central fixo + ícones | ícones em círculo branco com aro preto (~230 px de diâmetro = 21%): canto superior esquerdo "sincroniza tickets" (11,03), inferior esquerdo avião de papel "dispara mensagens" (12,15), superior direito "extensão" (13,8; ícone animado que vira fluxo/check), inferior direito coroa "automatiza follow-up" (16,7). Legendas no topo (y≈99–152) ou embaixo (y≈1630–1700) |
| 16,77–20,03 | igual, com fundo trocado por tomada mais fechada (ainda desfocada) | os 4 ícones ficam e seguem animados em loop |
| 20,03–21,25 | TH | médio, G≈25% |
| 21,20–21,30 | **flash de brilho** (1–2 quadros superexpostos e quentes) + punch-in | na palavra "Clica" (21,20) |
| 21,25–22,17 | TH close | G≈37% |
| 22,17–23,52 | TH médio-close | G≈32%. Legenda final "e eu te mostro como funciona" |

### 2.3 Ritmo
- 7 cortes de câmera (8 segmentos): média 2,94 s, mediana 2,80 s, mínimo 0,92, máximo 5,73.
- Contando as trocas de logo e os ícones, há **um evento visual a cada ~1,5 s** (12 eventos, |offset| mediano até o início da palavra = 0,06 s, 10 de 12 a até 0,1 s).
- Os ícones entram até 0,2 s **antes** da palavra (avião em 12,15, "dispara" em 12,34).
- Pausas: nenhuma acima de 0,28 s. Zoom contínuo: não há (8,4 vs 11,0: escala 1,00).

### 2.4 Legendas
- Mesmo sistema do C04: Montserrat Bold branca, sombra suave, centralizada, entrelinha ≈95 px, até 3 linhas ("porque nenhum / deles faz o que o / Beeno"), revelação palavra a palavra com layout fixo.
- **No trecho P&B a legenda inteira é amarela #F4C70F** (mesma fonte e sombra).
- Posição: na emenda do split (y≈900–1000), no peito na TH (y≈1370–1500), no topo ou no rodapé no trecho dos ícones, para não cobrir logo e ícones.
- Sem caixa alta de ênfase e sem emoji. Grafias corrigidas pela marca ("Beeno", "Blip").

### 2.5 Gráficos
- Logos de terceiros (Blip, HubSpot, RD Station) na "tela" do notebook. Parecem compostos em pós (screen replacement) sobre um B-roll POV.
- Logo Beeno #00CB88.
- **Ícones animados tipo Lottie/Lordicon:** traço preto dentro de disco branco com aro preto. Entram **girando** com blur de movimento e leve escala (~4 quadros), o aro gira, o desenho interno se redesenha em loop (check sendo traçado, fluxo, coroa).
- P&B como "momento de verdade/confronto".

### 2.6 Transições
- Cortes secos.
- Whip horizontal com blur entre os logos.
- Entrada do logo Beeno por esticamento horizontal.
- Flash de exposição curto no "Clica".
- Fundo desfocado como palco dos ícones.

### 2.7 B-roll
- Só o POV de notebook (0–5,43, metade de baixo). Iluminação quente e cinematográfica, mãos fora de foco: candidato a IA ou stock com tela substituída. Literal: as ferramentas que o público usa.

### 2.8 Áudio
- Trilha contínua (degrau espectral em ~15,4 kHz como no C04; nenhum silêncio).
- **SFX:** no intervalo de fala 12,06–12,33 o nível fica em **−11,2 dBFS** sem voz, que é o "pop/whoosh" da entrada do ícone do avião. Há um transiente largo em ~21,2 (flash do "Clica").
- Entre 5,9 e 8,2 s (trecho P&B) aparece energia extra em 2–4 kHz, possível camada sonora de tensão (não conclusivo).

### 2.9 Final
- Termina na TH falando, legenda completa na tela. Sem logo nem cartão final.

---

## 3. Reels 01 (31,56 s): "Muita gente acha que CRM é uma agenda de contato chique. Não é."

### 3.1 Resumo e estrutura
- Selfie na mão (celular), apresentador de jaqueta preta contra janela com prédios e céu (contraluz). Tom mais orgânico/UGC. Fala de **4,31 palavras/s** (a mais rápida).
- **Gancho (0–3,43):** quebra de crença + negação seca ("Não é.", com punch-in).
- **Reenquadramento (3,43–10,17):** "CRM não é onde você guarda o nome… isso o WhatsApp já faz. CRM de verdade é onde você enxerga a jornada inteira".
- **Prova/demonstração (10,17–14,8):** 4 cartões de **UI mockup do produto** em tela cheia, sincronizados com a lista falada.
- **Contraste (14,8–18,1):** "É a diferença entre ter o contato e saber o que fazer com ele", com caixas de texto em máquina de escrever.
- **Benefício (18,1–24,3):** "Um bom CRM não te dá mais cadastro, te dá mais venda fechada… Se o seu CRM é uma planilha cara…".
- **Produto (24,3–29,42):** logo + "o CRM ROBUSTO DE VERDADE", "integra marketing e venda".
- **CTA (29,42–31,56):** flash, "Chama a gente agora mesmo e conheça a plataforma". Sem cartão final.

### 3.2 Shot list
| início–fim (s) | tipo | detalhe |
|---|---|---|
| 0,00–2,87 | selfie TH | G≈34%, olhos y≈520 |
| 2,87–3,43 | **punch-in** seco | G≈55% (≈160%). Na palavra "Não" (2,94) |
| 3,33–3,43 | blur + flash branco (~3 quadros) | volta ao médio no "CRM" (3,44) |
| 3,43–5,57 / 5,57–10,17 | TH, **jump cut** em 5,57 (pausa removida, mesmo enquadramento, leve reposicionamento da mão) | G≈34% |
| 10,17–14,80 | **tela cheia de UI mockup** sobre fundo verde-escuro (#061913 a #0D281E) com manchas verdes desfocadas (bokeh) | cartão escuro estilo glassmorphism (#0A1E14) de ~940 px de largura (87%), y≈590–1380. Sequência: "Origem do lead" (Mariana Ribeiro, canais Instagram/WhatsApp/Site/Google Ads), "Conversas" (balões de chat verde #22C891 + "Resumo por IA"), "Pipeline de vendas" (etapas Lead → Contato → Proposta R$ 24.000 → Negociação → Fechamento), "Próximo passo" (Ligar para Mariana, Enviar follow-up, Agendar demonstração). Troca por **corte seco** em 11,03, 12,33 e 13,77, sempre na palavra que inicia o item. Legenda no topo, alinhada à esquerda (x≈130, y≈240–310) |
| 14,80–15,90 | TH | G≈34% |
| 15,90–18,10 | TH **desfocada** (blur que entra em ~3 quadros) + caixas de texto | caixa branca/creme no topo, **digitada letra a letra** "Ter o contato" em fonte **serifada** verde; ícone de seta verde para cima e vermelha para baixo (estilo emoji 3D) entra em escala grande → normal **sobre o rosto (nariz/boca)**; caixa verde #1FCB91 (cantos ~16 px) embaixo com texto serifado branco "O que fazer com ele" digitado com **cursor bloco branco** |
| 18,10–19,73 | TH | G≈37% |
| 19,73–21,10 | punch-in | G≈54%. "te dá mais venda fechada" |
| 21,10–24,30 | TH | G≈36%. "porque nada cai no esquecimento / se o seu CRM é uma planilha cara" |
| 24,30–27,30 | TH **desfocada** + logo e texto | "beeno" entra **gigante pela direita**, deslizando e encolhendo com blur de movimento (~0,4 s), centro y≈1100. Depois "◉ CRM" e "**ROBUSTO DE VERDADE**" em caixa alta extra-pesada e larga (tipo Montserrat Black/Archivo Black); "ROBUSTO" com preenchimento branco, "DE VERDADE" **só contorno** branco (vazado) |
| 27,30–29,42 | TH | G≈36%. "integra **marketing** e **venda**" |
| 29,33–29,47 | blur + flash branco (~3 quadros) | — |
| 29,42–31,56 | TH | CTA, legenda em 3 linhas |

### 3.3 Ritmo
- 15 cortes, 16 segmentos: média 1,97 s, mediana 1,88 s, mínimo 0,56 s, máximo 4,60 s (≈28,5 cortes/min).
- |offset| mediano até o início da palavra = 0,05 s (13 de 15 a até 0,1 s).
- Punch-ins secos de ~160% em palavras de impacto ("Não é", "te dá mais venda fechada"), com volta a 100% por corte ou flash.
- Selfie na mão: movimento natural, sem zoom digital contínuo detectável.
- Pausas: nenhuma acima de 0,28 s.

### 3.4 Legendas
- Montserrat Bold branca, sombra suave, centralizada.
  - Corpo ≈65 px (entrelinha ≈84 px), um pouco menor que nos Criativos.
  - Linha de até ~830 px (77%), 1–3 linhas, y≈1400–1620 (zona do peito/jaqueta escura, abaixo do queixo).
- Mesmo comportamento: palavra a palavra com layout fixo, troca por frase.
- **Destaques:** "marketing" em **amarelo #F2C50F** e "venda" em **verde #00AF08**, palavra a palavra conforme é dita (cores diferentes para os dois conceitos que o produto integra).
- No trecho de UI a legenda fica no topo, alinhada à esquerda.

### 3.5 Gráficos
- UI mockup do produto em tela cheia: a peça mais "produto" do grupo. Fundo verde muito escuro com bolhas verdes desfocadas, cartões escuros com acentos verde-menta #22C891, tipografia sans pequena (Poppins/Inter).
- Caixas de texto estilo "nota" com máquina de escrever (~15 caracteres/s), fonte serifada (tipo DM Serif/Georgia), duas cores (creme #F7F3D4 com texto verde × verde #1FCB91 com texto branco).
- Ícone de setas ⇅ (verde para cima, vermelho para baixo) como metáfora de contraste.
- Logo "beeno" #00C985 + "by skeps".
- Tipografia de impacto em caixa alta com mistura cheio/contorno.

### 3.6 Transições
- Corte seco.
- **Blur + flash branco** em 3,4 e 29,4 (~0,1 s, 2–3 quadros brancos).
- Blur rápido (~0,1 s) para entrar no "palco" desfocado (15,9 e 24,3); saída por corte seco para a TH nítida (18,1 e 27,3).

### 3.7 B-roll
- Não há B-roll filmado. A demonstração é toda em **UI mockup** (provavelmente feito em Figma/código) e tipografia.

### 3.8 Áudio
- Voz com banda até ~18,5 kHz, mais uma componente musical que fica abaixo de ~15,4 kHz.
- Trilha contínua: cauda em **−33,8 dBFS**; no intervalo de 2,78–2,94 s, −28 dBFS.
- **SFX:** whoosh na entrada do logo (intervalo 24,10–24,38 a **−13,6 dBFS** sem fala); faixa larga em 29,3–29,6 (flash do CTA).

### 3.9 Final
- TH com a legenda "chama a gente agora mesmo e conheça a plataforma". Sem cartão final, logo nem CTA gráfico.

---

## 4. Padrões transversais (o que se repete × o que varia)

### Repete-se nos 3
1. **Legenda base idêntica:** Montserrat Bold 700, branco #FFFFFF, sem contorno, sombra suave (~3–4 px, blur, ~45% preto), corpo 65–74 px (≈6–7% da largura), entrelinha ≈1,3, centralizada, até 3 linhas de ~75% da largura. **Palavra a palavra acumulando, sem animação, com layout final pré-calculado**, e troca do bloco a cada frase. A posição muda para não cobrir rosto nem gráfico: peito (y≈1130–1620), topo (y≈100–340) sobre B-roll, UI ou cartões, ou a emenda do split.
2. **Cor como semântica:** vermelho #EC1D1D = dor/erro ("primeira vez", "TUDO DE NOVO", "se repetir", "5 vezes"); verde = solução/marca (#00CB88 do logo, #02CD8B de contorno, neon #17FF17, #00AF08); amarelo #F2C50F/#F4C70F = alerta/confronto ou conceito-chave ("Desculpe…", "marketing").
3. **Logo "beeno" #00CB88 + "by skeps"** sempre centralizado, ~59% da largura (633 px), sobre a apresentadora **desfocada** (2 de 3) ou nítida (C05). Entrada sempre com movimento rápido e blur (zoom-out de 3x, whip horizontal ou deslize gigante pela direita), ~0,25–0,4 s. Entra junto da menção à marca, até 0,9 s antes.
4. **"Palco desfocado":** cortar para uma tomada da TH com blur gaussiano forte e pôr gráficos/texto por cima (logo, ilustrações, ícones, caixas de texto, glow). É o recurso mais usado para inserir conteúdo sem sair da pessoa e sem cobrir o rosto nítido.
5. **Transição de capítulo = blur + flash branco** (2–5 quadros 100% brancos, ≈0,1–0,4 s), com whoosh. Usada para passar do gancho ao produto e do problema à solução ou ao CTA.
6. **Punch-in** seco de ~150–200% (G de ~18–34% para 35–55%) em palavras de impacto. Nos Criativos, **o primeiro punch-in do gancho é em P&B** (C04 "cinco vezes", C05 "Desculpe…").
7. **Cortes no início da palavra** (mediana de 0,05–0,06 s), segmentos de ~2 s (mediana 1,5–2,8 s), ritmo de ~28 cortes/min (C04, R01). Pausas removidas: nenhuma acima de 0,3 s, fala de 3,4–4,3 palavras/s.
8. **Trilha musical contínua** ~12–15 dB abaixo da voz (banda limitada a 15,4 kHz) + **SFX de whoosh/pop** nos flashes e nas entradas de logo/ícone.
9. **Fim seco:** sem cartão final, sem logo, sem URL. O CTA é falado ("clica no link", "chama a gente") com a legenda. Só o C04 termina em preto (0,54 s, só com a legenda).
10. Câmera estática, sem zoom contínuo (Ken Burns), sem shake, glitch nem speed ramp. Sem emoji.

### Varia
- **Captação:** Criativos em estúdio, tripé, várias tomadas e escalas. Reels em selfie na mão, contraluz, jump cuts no mesmo enquadramento.
- **Tipo de inserção:**
  - C04: ilustração 2D narrativa (Irasutoya), stock realista em split, cartão preto com ícone, texto neon glow com fonte arredondada.
  - C05: split com B-roll POV de notebook + logos de concorrentes, ícones Lottie em disco branco.
  - R01: UI mockup do produto em tela cheia (verde-escuro), caixas em máquina de escrever com fonte serifada, título vazado "DE VERDADE".
- **Fonte de destaque:** Montserrat ExtraBold/Black (números, caixa alta), arredondada pesada com glow (C04), serifada (R01).
- **Duração e densidade:** 52 s com 5 linguagens gráficas (C04); 23 s muito enxuto (C05); 31 s com prova de produto (R01).
- **Posição do split:** C04 TH em cima e stock embaixo (fusão ~y 960–1100); C05 TH em cima e B-roll embaixo (fusão ~y 900–1000). Nos dois a legenda fica sobre a emenda.
- **Atenção:** o R01 coloca o ícone de setas **sobre o rosto** (com o fundo desfocado), o que quebra a regra "rosto livre" do estúdio. Ao replicar, posicionar fora da região do rosto.

### Receita mínima para replicar (Remotion)
1. Legenda Montserrat 700, ~72 px, branca com `text-shadow: 3px 4px 6px rgba(0,0,0,.45)`, layout por frase pré-quebrado em ≤3 linhas centralizadas; cada palavra com `opacity` 0→1 instantâneo no `start` do `palavras.json`; y dinâmico (peito ou topo).
2. Mapa de cores de palavra: dor → #EC1D1D; benefício → contorno #02CD8B ou neon #17FF17 com glow; alerta → #F4C70F.
3. Componentes: `FlashBranco` (blur 0→40 px + brilho, 3 quadros, 3 quadros brancos, 2 de saída), `PunchIn` (scale 1,5–1,8 recortando o vídeo master, sem cortar o tempo), `PalcoDesfocado` (o próprio master com blur 30–40 px, mesmo timestamp), `LogoEntrada` (scale 3→1 com motion blur, 8 quadros), `IconeCirculo` (disco branco de 230 px com aro preto, spin-in de 4 quadros), `MockupUI` sobre fundo #061913 com blobs verdes, `CaixaDigitada` (serifada, 15 caracteres/s, cursor bloco), `TrechoPB` (saturação 0 + legenda amarela).
4. Trilha a ~−15 dB da voz + whoosh em cada flash e pop em cada entrada de logo/ícone.

Observação para o Studio: nestes vídeos-referência os cortes e os punch-ins trocam a **tomada**. No Studio o master é intocável, então o equivalente é simular as escalas (100% ↔ 150–180%) com zoom recortado e manter o áudio contínuo.
