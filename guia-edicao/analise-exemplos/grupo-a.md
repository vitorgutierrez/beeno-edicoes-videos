# Grupo A: análise forense (Criativo 01, 02, 03)

Fonte: `videos exemplo/drive-download-20261008T221217Z-1-001/Criativo 0{1,2,3}.mp4`.
Todos estão em 1080x1920, 30 fps, HEVC Main10 (BT.709), AAC 44.1 kHz estéreo, com loudness integrada de −20 a −21 LUFS (pico de +0.3 a +0.6 dBFS, ou seja, sem limiter ajustado).
Método: scdet (cortes), todos os quadros a 30 fps em 216x384 para tiras quadro a quadro, quadros em resolução cheia para medir posição, cor e fonte, palavras.json (faster-whisper) para alinhar com a fala, e bandas de áudio (<120 Hz e >5 kHz) a cada 1/30 s para achar SFX.
Coordenadas em px de 1080x1920. Tempos em segundos.

---

## Criativo 01 (33,20 s): "CRM nativo para Blip" + demonstração de tela

### 1. Resumo
- **Tema:** o Beeno é o primeiro CRM nativo para Blip. Mostra a extensão lateral dentro do Blip Desk.
- **Captação:** selfie com a câmera frontal do celular, na mão, em escritório (rosto ~40% da largura, olhos em y≈950). Depois, o celular filma a tela do notebook (não é gravação de tela).
- **Estrutura:**
  - Gancho de público (0–5,3): "Se você usa Blip... você precisa conhecer o Bino".
  - Promessa (5,3–10,9): "primeiro CRM criado nativamente para Blip... vou te mostrar".
  - Demonstração (11,17–28,87): tela filmada, com fala descrevendo o painel.
  - CTA (28,87–33,2): "Clica no link abaixo e agende uma reunião comigo".
- Ritmo de fala de 3,4 palavras/s (112 palavras). Só três pausas acima de 0,25 s em todo o vídeo, o que indica pausas removidas.

### 2. Shot list
| # | início–fim | tipo | enquadramento / conteúdo |
|---|---|---|---|
| 1 | 0,00–4,23 | talking head selfie | Plano médio-curto, rosto centrado. **Logo Blip** oficial (balão azul #0096FB + "blip" preto #000) no topo, x 266–815, y 270–474 (~51% da largura). Entra em 0,60 s exatamente na palavra "Blip": desliza e encolhe com motion blur horizontal forte e assenta em ~9 quadros (0,60→0,90). Sai por corte seco em 2,867 (na troca de página da legenda, palavra "robusto"). |
| 2 | 4,23 | flash/whip | 1 quadro com fundo branco e o wordmark "beeno" verde borrado horizontalmente (whip). |
| 3 | 4,27–5,30 | logo sobre fundo desfocado | O mesmo take da selfie com desfoque gaussiano forte (~25–30 px). **Logo Beeno** verde #00CB88 + "by skeps" branco, centralizado (x 164–914, y 819–1096, ~70% da largura). Entra em whip horizontal com motion blur e assenta em ~4,67 s (12 quadros). **Legenda some** durante o bloco. O logo entra 0,77 s **antes** da palavra "Bino" (5,00), sobre "você precisa conhecer". |
| 4 | 5,30–6,30 | talking head (mesmo take, jump cut) | "é o primeiro CRM" |
| 5 | 6,30–8,27 | jump cut | "criado nativamente para Blip" |
| 6 | 8,27–10,93 | jump cut | "vem aqui que eu vou te mostrar..." |
| 7 | 10,93–11,17 | transição | Zoom-in com desfoque e bloom: o rosto aumenta, desfoca e estoura de brilho em 4 quadros; a tela do notebook entra igualmente desfocada e clara, com zoom-out, e assenta em 11,167. São 8 quadros no total, sem legenda. |
| 8 | 11,17–25,80 | tela filmada (take único de 14,6 s) | Notebook com o Blip Desk. A câmera passeia: começa no chat e, quando ele diz "do lado direito" (13,9 s), panorama para o painel verde do Beeno. O movimento de câmera acompanha a fala. |
| 9 | 25,80–28,87 | tela filmada, take 2 | Corte seco. Por volta de 28,7, a mão passa na frente da lente e funciona como **wipe natural** até o take 3. |
| 10 | 28,87–33,20 | tela filmada, take 3 | Teclado aparece embaixo. CTA. **Sem end card**: termina na imagem, ~0,25 s depois da última palavra. |

### 3. Ritmo de corte
- 8 planos, média de 4,15 s. No talking head (0–10,9) a média é ~2,2 s (1,0 / 1,97 / 2,66). Mínimo de 1,0 s; máximo de 14,6 s (tela).
- Jump cuts no mesmo take com **o mesmo enquadramento** (sem punch-in alternado). Os cortes caem nas fronteiras de frase, onde a pausa foi removida.
- Não há zoom drift no talking head.

### 4. Legendas (padrão do grupo; detalhes no item cruzado)
- Montserrat Bold, branca #FFFFFF, sem contorno. Sombra projetada suave preta (~50%, deslocamento ~+4/+4 px, blur ~4 px).
- Corpo ~76–78 px (altura de maiúscula 54 px, altura-x 40 px), entrelinha ~96 px. Texto centralizado, até ~870 px de largura (80%).
- Posição y: linha única em 1500–1550 (centro ≈1525, 79% da altura). Com duas linhas, 1444–1598.
- Revelação **palavra por palavra acumulando**, sem animação (aparece seca no quadro).
- Nenhuma palavra colorida. Caixa de frase: maiúscula só no início do vídeo e em nomes próprios (Blip, CRM). Mantém "?" e não usa ponto final.

### 5. Elementos gráficos
- Logo Blip (oficial, colorido) no gancho, sincronizado com a palavra.
- Logo Beeno grande ao centro sobre a selfie desfocada.
- Nenhum outro gráfico, ícone ou número. A "prova" é a tela real filmada.
- **Atenção:** a tela filmada mostra nomes e telefones reais de contatos do CRM. Numa réplica, desfocar ou usar dados fictícios.

### 6. Transições
- Logo Blip: entrada com motion blur, ~9 quadros, ease-out.
- Beeno: 1 quadro de flash branco com o logo, depois whip com motion blur, ~12 quadros.
- Selfie → tela: zoom blur + bloom (8 quadros).
- Tela → tela: corte seco, e uma vez wipe natural com a mão.

### 7. B-roll
Nenhum B-roll de banco. O "B-roll" é a filmagem real da tela (14,6 + 3,1 + 4,3 s, ~66% do vídeo), com a voz contínua por cima e legendas na mesma posição.

### 8. Áudio
- Fundo contínuo de graves (<90 Hz) em ~−39 dBFS RMS em todo o vídeo, e −38 dB RMS na cauda depois da fala: **trilha de fundo baixa** (~15 dB abaixo da voz, cuja RMS fica entre −20 e −26 dB).
- **SFX:** boom grave em 0,67 (entrada do logo Blip, +15 dB na banda grave); whoosh/transiente agudo em 4,17 (+26 dB, whip do Beeno); transiente em 10,87 (transição zoom).
- Pausas removidas.

### 9. Final
Corta direto na tela com a legenda "e agende uma reunião comigo". Sem logo final, end card ou fade.

### 10. Distintivo
É o mais "cru" do grupo: selfie e tela filmada, e quase nenhum motion. A produção se concentra só nos dois logos do gancho.

---

## Criativo 02 (30,63 s): metáfora Ferrari × Fusca

### 1. Resumo
- **Tema:** "Blip é uma Ferrari; se o seu CRM não tem X, Y, Z, você usa um Fusca". O Beeno é o único nativo.
- **Captação:** câmera fixa em tripé, apresentador sentado à mesa com notebook e estante ao fundo (luz quente, plantas, "@" decorativo). O mesmo take aparece em três escalas de recorte.
- **Estrutura:**
  - Gancho (0–3,80): "Se você usa o Blip... parabéns, você tem uma Ferrari na mão".
  - Problema (3,80–16,97): lista de recursos que faltam, depois "Fusca".
  - Solução (16,97–25,97): "conheça o Bino, a única plataforma... nativa" e "Soluções integradas...".
  - CTA (25,97–30,5): "Quer saber como funciona? Clica no link abaixo...".
- Ritmo de fala de 3,76 palavras/s, com uma única pausa acima de 0,25 s.

### 2. Shot list
| # | início–fim | tipo | enquadramento / conteúdo |
|---|---|---|---|
| 1 | 0,00–2,37 | TH **aberto** (largura dos óculos ≈14% da largura) | **Logo Blip** versão branca (balão azul + "blip" branco), sobre o peito (y 938–1082), em 0,633 s na palavra "Bleep" (0,62). Entra com escala, blur e assentamento em 8 quadros. Jump cut leve em 1,767 dentro do take. Legenda em y≈1350–1480. |
| 2 | 2,37–3,80 | **split vertical TH + B-roll** | TH reenquadrado (plano médio) empurrado para cima, ocupando os ~45% superiores. B-roll de Ferrari vermelha (traseira, estrada com montanhas, luz do dia, realista/stock) nos ~55% inferiores. Emenda por **máscara em degradê** entre y≈850 e 1050 (~200 px de feather), sem linha divisória. Legenda sobe para y≈895, na emenda. "você tem uma Ferrari na mão". |
| 3 | 3,80–5,40 | TH **médio** (óculos ≈20%) | "agora, se o seu CRM não tem" |
| 4 | 5,40–11,30 | **modo desfoque + máquina de escrever** | TH aberto com desfoque gaussiano forte. Em vez da legenda, texto **digitado letra a letra** (~1 caractere a cada 1–2 quadros, cursor "▏" piscando), numa fonte sans humanista **Regular**, fina e sem sombra (estilo Open Sans/Noto), ~58 px, branca, centralizada em y≈965. Itens: "Histórico de Ticket Sincronizado", "Mensagens Ativas", "Extensão no Blip Desk", "para não precisar trocar de tela". Plano único de 5,9 s; o desfoque esconde a falta de cortes. |
| 5 | 11,30–11,77 | TH médio | "me desculpa" (0,47 s, o plano mais curto) |
| 6 | 11,77–14,33 | split TH + B-roll | Fusca branco em estrada de terra vermelha com barrancos de capim (Brasil rural, realista, leve posterização que sugere IA ou compressão). Mesmo layout do plano 2. "...um CRM que basicamente é um Fusca". |
| 7 | 14,33–16,97 | TH médio | **Flash quente amarelo** no corte: superexposição amarelada que decai em ~6 quadros (0,2 s). "E se você não quer mais utilizar um Fusca..." |
| 8 | 16,97–21,47 | **motion graphic sobre TH aberto desfocado** | Logo Beeno verde: (a) whip-in da esquerda com motion blur horizontal, 5 quadros (16,97–17,13), e fica ao centro em y≈650; (b) em 17,67–17,80 sobe para o topo (x 224–855, y 144–310; "by skeps" branco em y 340–380, alinhado à direita); (c) linha **tracejada branca em S** (traço ~8 px, tracinho ~30 px) se desenha de um ponto branco (Ø~36 px) sob o logo até outro ponto em y≈1195 (17,93–18,6); (d) **mockup de notebook** com print real do Blip+Beeno sobe e cresce de baixo (19,13–19,53; final x 185–895, y 1275–1720); (e) **selo verde de check** (círculo verde, check branco, sombra) estala no canto superior direito do notebook em 19,9 s. A legenda continua no centro (y 840–990). O logo entra 0,43 s antes de "Bino" (17,40). |
| 9 | 21,47–24,83 | TH **fechado** (óculos ≈26%) | "Soluções integradas para facilitar o dia a dia do seu vendedor" |
| 10 | 24,83–25,97 | TH médio | "e do seu time comercial" |
| 11 | 25,90–26,10 | **transição desfoque → flash branco** | 2 quadros de desfoque crescente, depois clareia, fica 2 quadros quase branco puro (26,00–26,03) e revela com vazamento de luz quente (26,07). São ~6 quadros e a legenda fica visível por cima. Marca a entrada do CTA. |
| 12 | 26,07–27,10 | TH médio-aberto | "Quer saber como funciona?" |
| 13 | 27,10–28,13 | TH médio-fechado | "clica no link abaixo" |
| 14 | 28,13–29,53 | TH médio | "que eu vou te mostrar na prática" |
| 15 | 29,53–30,50 | TH médio | "em uma demonstração" |
| 16 | 30,50–30,63 | preto | 4 quadros de preto |

### 3. Ritmo de corte
- 15 planos de imagem, média de 2,0 s. Mínimo de 0,47 s ("me desculpa"); máximo de 5,9 s (desfoque com digitação).
- **Punch-in alternado em 3 escalas** do mesmo take: aberto (100%), médio (~140%), fechado (~185%). A escala troca em quase todo corte.
- Na reta final (26–30,5) os cortes são regulares, a cada ~1,0–1,4 s, sempre na fronteira de frase.

### 4. Legendas
- Mesmo estilo base (Montserrat Bold branca com sombra suave, ~76 px).
- **A posição y muda conforme o plano**, para ficar sobre o peito ou as mãos e nunca sobre o rosto: aberto ≈1350–1480 (70–77%); médio ≈1295–1346 (68%); fechado ≈1110–1260 (58–65%); split ≈895 (na emenda); logo/mockup ≈840–990 (centro).
- Revelação palavra a palavra, com layout final da página já calculado: as palavras aparecem **no lugar definitivo**. A 2ª linha começa deslocada e só fica centralizada quando a página completa.
- Pontuação expressiva: "Parabéns!" vira página própria.
- Sem cor de destaque.

### 5. Elementos gráficos
- Logo Blip branco no peito.
- Logo Beeno com caminho tracejado, mockup de notebook e selo de check (bloco de 4,5 s).
- Texto digitado com cursor.
- Duas metáforas visuais em split.
- Fundo de todos os gráficos: o próprio TH desfocado. Não há cards sólidos.

### 6. Transições
- Corte seco na maioria.
- Flash amarelo quente decaindo em 6 quadros (14,33), na virada problema → solução.
- Desfoque → branco → luz quente em 6 quadros (25,9–26,1), antes do CTA.
- Whip com motion blur nos logos.

### 7. B-roll
- **Ferrari** (1,43 s) e **Fusca** (2,56 s): metáfora literal da fala, realistas, sem cor aplicada, só na metade de baixo, com o rosto sempre visível em cima.
- A voz segue por cima. O Fusca traz **ambiência própria** (ruído largo até 16 kHz no espectrograma, 11,8–14,3 s).

### 8. Áudio
- **A trilha entra em ~15,0 s:** a banda <90 Hz sobe de ~−48 para ~−34 dBFS e fica assim até o fim. Isso coincide com a virada para a solução ("E se você não quer mais..."). Antes, o fundo é quase só voz.
- **SFX:**
  - Boom grave em 0,60 (logo Blip) e em 16,97 (logo Beeno, +18 dB).
  - "Ding"/brilho tonal em ~1,8–2,1 s ("Parabéns!"; harmônicos ~3,5 kHz visíveis).
  - Transientes agudos em 5,37, 7,23 e 8,40 (+21 a +24 dB): **digitação/teclas** a cada novo item datilografado.
  - Transientes em 14,27 (flash), 25,93 (flash branco) e 27,03 (corte).

### 9. Final
Corte para preto de 4 quadros depois de "demonstração". Sem end card ou logo.

### 10. Distintivo
- Metáfora de produto (Ferrari/Fusca) ilustrada por B-roll em split com degradê.
- "Lista de recursos" digitada sobre fundo desfocado.
- Logo Beeno que vira um diagrama (logo → caminho → produto → check).

---

## Criativo 03 (42,21 s): "um funil, uma ferramenta" (apresentadora)

### 1. Resumo
- **Tema:** ferramentas separadas entre marketing e vendas versus um funil único no Beeno.
- **Captação:** mesmo cenário do 02 (estante, "@"), apresentadora sentada. Mesmo take em 3 escalas.
- **Estrutura:**
  - Dor (0–7,57): "Você paga uma ferramenta para o marketing, outra para o comercial... ninguém conversa entre si".
  - Agitação (7,57–16,6): "Esse é o buraco que faz a empresa perder venda todos os dias", "Marketing de um lado, vendas do outro", "planilha".
  - Solução (16,6–33,47): logo, funil animado, "nutre o lead", tags "Campanha / Follow Up / E-mail / Venda".
  - Tagline (32,9–33,7): "Um funil, uma ferramenta".
  - CTA (34,3–42,2): "Quer ver na prática? Clique aqui nesse link embaixo...".
- Ritmo de fala de 3,27 palavras/s.

### 2. Shot list
| # | início–fim | tipo | conteúdo |
|---|---|---|---|
| 1 | 0,00–2,20 | TH **aberto** (óculos ≈15%) | "Você paga uma ferramenta para o **Marketing**" (amarelo) |
| 2 | 2,20–3,70 | TH **médio** (≈22%) | "outra para o **comercial**" (azul) |
| 3 | 3,70–5,50 | TH **fechado** (≈28%) | "outra pra **registrar os leads**" (verde) |
| 4 | 5,50–7,57 | **modo desfoque** (TH médio desfocado, corte seco para a versão desfocada) | Texto central em y 746–923: "e mesmo assim" em caixa baixa com **tracking largo** (~+10–15%), ~70 px, e "**NINGUÉM**" em caixa alta maior (~100 px, altura de maiúscula ~70 px), depois "conversa entre si". Aqui o texto passa por cima do rosto desfocado. |
| 5 | 7,57–9,73 | TH aberto | "esse é o buraco que faz empresa perder venda" |
| 6 | 9,73–10,83 | **card preto** #000 | "TODOS" → "TODOS OS" → "TODOS OS DIAS": caixa alta, Montserrat Bold branca ~76 px, centro y≈885, palavra a palavra. Preto puro sem texto nos últimos ~0,13 s. |
| 7 | 10,83–11,93 | **split horizontal** | TH à esquerda (0–523 px) + **painel amarelo sólido #FFE226** à direita (523–1080); rótulo "Marketing" branco centralizado no painel, entrando 1 quadro depois (na palavra). |
| 8 | 11,93–12,93 | split espelhado | **Painel azul #2666FF** à esquerda (0–546) com "Vendas" + TH à direita. Há 1 quadro de glitch em 11,933 com o rótulo antigo. |
| 9 | 12,93–14,20 | TH médio | "cada um com a sua ferramenta" |
| 10 | 14,20–16,60 | **B-roll stock** | Mãos digitando num MacBook com planilha estilo Excel (cabeçalho verde), vista de cima/lateral, realista. Entra por **dissolve com zoom** em 4 quadros. A legenda continua (y≈1100–1140, 58%). "sua planilha, seu próprio controle". |
| 11 | 16,60–18,57 | **TH desfocado + overlay verde** | Desfoque forte com camada verde Beeno (tons resultantes #147047 a #50A373; overlay ~60–70% sobre a imagem). Logo "beeno" **branco** em whip-in da esquerda com motion blur, 9 quadros (16,63–16,90), centralizado em y≈1150. A legenda some. Entra em "Bino" (16,72). |
| 12 | 18,57–26,07 | **card branco cheio** #FDFDFD (7,5 s, o maior bloco) | Logo Beeno verde #00CB88 desce do topo com motion blur vertical em 7 quadros e fica em x 248–830, y 188–402. **Funil flat** azul acinzentado #729EC8 (x 218–791, y ~500–1299) com 3 avatares de usuário caindo dentro (19–20,5). Rótulos em inglês **ATTRACT / CONVERT / ENGAGE / SELL** (fonte condensada bold, estilo Bebas/Oswald) se revelam um por um (21,5–23,5). **Moeda dourada $** #FDB934 cai pela boca do funil (~24,3, "até a venda fechada"). **Sem legenda** o bloco inteiro. Tem cara de motion template de banco (rótulos em inglês). |
| 13 | 26,07–28,07 | TH médio | "nutre o lead sem trocar de plataforma" |
| 14 | 28,07–29,57 | TH aberto/médio | **Flash quente** de 1–2 quadros no corte. "tudo isso dentro do CRM" |
| 15 | 29,57–32,87 | TH aberto + **tags-pílula** | Pílulas verde Beeno **#00CD8A**, raio ~20 px, texto branco Montserrat Bold ~76 px, centralizadas em x≈554 e empilhadas: "Campanha" (y 1140–1285, 481 px), "Follow Up" (1323–1457), "E-mail" (1485–1627), "Venda" (1662–~1800). Padding horizontal ~30 px, vão de ~35 px. Cada uma **estala seca** na sua palavra (29,70 / 30,37 / 31,33 / 32,47), cada uma com SFX de "pop". A legenda normal fica oculta. |
| 16 | 32,87–33,47 | TH médio | "um funil" |
| 17 | 33,47–34,33 | TH médio-fechado | "uma ferramenta" e, depois, a transição **desfoque → branco → revelação** (34,27–34,40, ~5 quadros) |
| 18 | 34,40–42,21 | TH aberto (take único de 7,8 s) | CTA. Sem drift. Termina na imagem, sem end card. |

### 3. Ritmo de corte
- 18 blocos, média de 2,35 s. Sem contar o card do funil (7,5 s) e o CTA (7,8 s), a média é ~1,6 s. Mínimo de 0,6 s ("um funil").
- **Alternância de escala aberto → médio → fechado nos três primeiros cortes**, em sincronia com as três "ferramentas" faladas. Cada escala ganha também uma cor de palavra.
- Os cortes caem 0,05–0,2 s antes do início da frase seguinte, ou seja, no lugar da pausa removida. A legenda zera no corte e só volta na próxima palavra, deixando 1–6 quadros sem legenda.

### 4. Legendas
- Base igual ao grupo: Montserrat Bold branca ~76 px com sombra suave.
- Posição fixa no TH: linha única com altura-x em y 1436–1476 (≈76%); duas linhas em 1376–1524. No B-roll sobe para ~58%.
- **Regra de destaque (só no gancho):** o nome de cada ferramenta ou área ganha uma cor própria, e são três cores diferentes:
  - Marketing → **#F4C70F** (amarelo);
  - comercial → **#0090FF** (azul);
  - registrar os leads → **#00B20A** (verde).
  - Depois disso, nenhuma palavra colorida.
- **Ênfase por caixa alta:** "NINGUÉM" (maior, no modo desfoque) e "TODOS OS DIAS" (card preto).
- Até 3 linhas ("clica aqui nesse link / embaixo e marque / uma call"), com ~3–4 palavras e ~22 caracteres por linha.

### 5. Elementos gráficos
- Card preto de texto.
- Splits com painéis sólidos amarelo e azul. As mesmas cores do destaque (amarelo = Marketing; azul = Vendas/comercial) criam um **código de cor** consistente.
- Overlay verde de marca no logo.
- Card branco com funil.
- Tags-pílula verdes.
- Nenhum print do produto.

### 6. Transições
- Corte seco (padrão).
- Dissolve com zoom em 4 quadros (para o B-roll).
- Whip com motion blur (logos).
- Flash quente de 1–2 quadros (28,1).
- Desfoque → branco em ~5 quadros antes do CTA, idêntico ao do Criativo 02.

### 7. B-roll
Um único B-roll de banco (planilha, 2,4 s), literal, sem tratamento de cor, com legenda por cima.

### 8. Áudio
- **Trilha contínua** em todo o vídeo: banda <90 Hz estável em −34 dBFS (de 0 a 42 s) e cauda de −33 dB RMS depois da fala.
- **SFX:**
  - Boom/impacto grave em 10,87 (painel amarelo), 11,97 (painel azul), 16,67–16,83 (logo) e 18,57–18,73 (card do funil).
  - Transientes agudos fortes (+25 a +27 dB) em 7,43, 9,67, 14,07 e 28,13: whoosh/swish nos cortes e transições.
  - **4 "pops"** (+31 a +34 dB) em 29,73 / 30,37 / 31,33 / 32,47, um por tag.
- Pausas removidas (4 gaps acima de 0,25 s, todos ≤0,44 s).

### 9. Final
Take aberto de 7,8 s, com a legenda revelando até "como tudo isso aconteceria na sua operação". Termina na imagem, ~0,25 s depois da fala. Sem logo ou end card.

### 10. Distintivo
É o mais "gráfico" do grupo:
- código de cor amarelo/azul/verde;
- card preto de ênfase;
- split com painéis sólidos;
- funil animado de 7,5 s sem legenda;
- tags-pílula com pop.

---

## Padrões cruzados (grupo A)

### O que se repete (receita)
1. **Duração de 30–42 s.** Fala de 3,3–3,8 palavras/s com **pausas removidas** (praticamente nenhum gap acima de 0,3 s). Loudness de ~−20 LUFS.
2. **Estrutura de 4 atos:**
   - gancho de público ou dor nos primeiros 3–5 s, sempre citando o **Blip** ou a dor;
   - problema/agitação;
   - **entrada do logo Beeno** como virada (entre 4,2 e 17 s);
   - **CTA de reunião/demonstração** nos últimos 4–8 s ("clica no link abaixo... te mostrar na prática").
   - **Nenhum tem end card**: termina na imagem (2 vídeos) ou com 4 quadros de preto (1 vídeo).
3. **Legenda, que é a assinatura do grupo:**
   - Montserrat Bold (700), branca #FFFFFF, **sem contorno**, com **sombra projetada suave** (preta, ~50%, ~4 px de deslocamento e de blur).
   - ~76–78 px (altura de maiúscula 54 px, altura-x 40 px), entrelinha ~96 px.
   - Centralizada, largura máxima ~870 px; 1–3 linhas, ~3–4 palavras e ~22 caracteres por linha.
   - **Revelação palavra a palavra acumulando, sem animação**, com cada palavra já no lugar final da página.
   - A página troca nas fronteiras de frase e **zera em cada corte**.
   - Caixa baixa (exceto o início do vídeo e nomes próprios). "?" e "!" mantidos, sem ponto final.
   - **A legenda some** nos blocos de logo e nos cards cheios.
   - A posição y padrão é ~76–79% da altura, sobre o peito. Sobe para ~55–65% em planos fechados ou B-roll, para nunca cobrir o rosto nítido.
4. **Logos:**
   - Logo do Blip (parceiro) aparece **exatamente na palavra "Blip"** nos dois vídeos que a citam, com entrada de escala e motion blur (~8–9 quadros) e boom grave.
   - Logo Beeno (#00CB88, com "by skeps") entra em **whip horizontal com motion blur** (5–12 quadros) sobre o **próprio talking head desfocado** (ou com overlay verde), de 0,0 a 0,8 s antes de a palavra "Bino" ser dita.
5. **Modo desfoque:** TH com gaussiano forte + texto central, usado para listas ou ênfase (5,9 s no 02; 2,1 s no 03) e como fundo dos logos. É o recurso que substitui o B-roll quando não há imagem.
6. **Transição de entrada do CTA:** desfoque → flash branco → revelação quente (~6 quadros), idêntica no 02 e no 03. Flashes quentes de 1–6 quadros também marcam viradas.
7. **Áudio:** trilha de fundo baixa, ~12–18 dB abaixo da voz (no 02 entra só na virada para a solução). SFX de boom grave em logos e cards, whoosh nos cortes, pop em elementos que estalam, digitação no texto datilografado.
8. **Punch-in do mesmo take em 3 escalas** (aberto 100%, médio ~140%, fechado ~185%), alternando a cada corte, nos vídeos de tripé (02 e 03). Sem zoom drift contínuo.

### O que varia
| aspecto | Criativo 01 | Criativo 02 | Criativo 03 |
|---|---|---|---|
| captação | selfie na mão + tela filmada | tripé, 3 escalas | tripé, 3 escalas |
| plano médio | ~4,2 s (tela longa) | ~2,0 s | ~2,35 s (~1,6 s sem os blocos longos) |
| prova visual | tela real filmada (66% do vídeo) | mockup de notebook + check | funil genérico animado |
| B-roll | nenhum | 2 metáforas (Ferrari/Fusca) em split com degradê | 1 literal (planilha) em tela cheia |
| cor nas palavras | nenhuma | nenhuma | 3 cores no gancho (#F4C70F / #0090FF / #00B20A) |
| cards cheios | nenhum | nenhum | preto (texto), amarelo/azul (split), branco (funil) |
| trilha | o vídeo todo | entra aos 15 s | o vídeo todo |
| final | imagem | 4 quadros de preto | imagem |

### Paleta medida
- Verde Beeno, logo: #00CB88.
- Verde Beeno, pílula: #00CD8A.
- Azul Blip: #0096FB.
- Amarelo do painel: #FFE226.
- Amarelo da palavra: #F4C70F.
- Azul do painel: #2666FF.
- Azul da palavra: #0090FF.
- Verde da palavra: #00B20A.
- Funil: #729EC8.
- Moeda: #FDB934.
- Fundo do card: branco #FDFDFD e preto #000000.
- Legenda: #FFFFFF com sombra preta.

### Notas para replicar no Remotion
- **Componente de legenda:** a partir do `palavras.json`, agrupar em páginas de ≤3 linhas e ~22 caracteres por linha, quebrando em pontuação e nos cortes. Calcular o layout da página inteira (centralizada) e renderizar cada palavra com `opacity` 0→1 em degrau no quadro do início da palavra, ou até +0,2 s; nunca antes. `y` por plano: 0,77·H no plano aberto/médio, ~0,60·H no fechado ou B-roll.
- **WhipLogo:** translateX de −120% (ou +120%) → 0 em 5–12 quadros com ease-out forte, mais blur direcional proporcional à velocidade (dá para simular com 6–8 cópias deslocadas e opacidade decrescente, ou com um filtro SVG feGaussianBlur stdDeviation="40 0"). Fundo: o vídeo com `filter: blur(28px)`, opcionalmente com overlay verde rgba(0,203,136,0.6) com mix-blend `color`/`multiply`.
- **FlashTransition:** blur 0→20 px em 2 quadros, depois branco 0→100% em 2 quadros, segura 1–2 quadros e revela com tint quente (#FFD27A, 40% → 0) em 2–3 quadros.
- **SplitBroll:** TH em `translateY(-22%)` e escala 1,4 na metade de cima; B-roll na metade de baixo (y 850–1920) com máscara `linear-gradient(to bottom, transparent 850px, black 1050px)`.
- **PillTags:** retângulo #00CD8A com raio 20 px e padding 40×30, Montserrat Bold 76 px branca, empilhado com gap de 35 px, aparecendo seco + SFX de pop por palavra.
- Prompts de B-roll por IA: metáfora literal da fala (carro esportivo × carro velho, mãos numa planilha), realista, luz natural, sem texto e sem tratamento de cor. Fica só na metade de baixo ou em tela cheia por 1,4–2,6 s.
