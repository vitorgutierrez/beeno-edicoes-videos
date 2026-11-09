# Estilo Beeno: manual de edição dos criativos

Este manual descreve, com números, como são editados os 11 vídeos de referência da Beeno (`Drive da Beeno, pasta dos vídeos de referência`). Use-o como **especificação** quando a pessoa pedir "no estilo Beeno" ou "igual aos criativos". O ponto de partida é sempre o vídeo bruto gravado: daí em diante, Claude Code faz a montagem no Remotion e, no Nível 2, gera B-roll na Higgsfield.

Fonte dos números: detecção de corte, quadros em resolução cheia, tiras a 30 fps em cada transição, cores amostradas em pixel, transcrição por palavra e análise espectral do áudio. Os relatórios completos, vídeo a vídeo, estão em [`analise-exemplos/`](analise-exemplos/) (`grupo-a.md` a `grupo-d.md`), com as transcrições.

> **Como ler:** a seção 1 é o resumo de bolso; as seções 2 a 11 são as regras; a 12 é a receita de automação; o anexo traz a ficha de cada vídeo. Coordenadas em px de um quadro 1080×1920. Tempos em segundos.

---

## 1. Resumo de bolso (as 15 regras que definem o estilo)

1. **Vertical 1080×1920, 30 fps, 23 a 65 s** (mediana de ~41 s).
2. **Fala corrida, sem respiro:** pausas cortadas até no máximo ~0,3–0,5 s. Ritmo de 3,3 a 4,3 palavras/s. A fala começa no quadro 0 e termina 0,15–0,6 s antes do fim.
3. **Um corte por frase:** cada corte cai de 0 a 3 quadros **antes** da primeira palavra da frase seguinte.
4. **Plano de câmera dura ~2 s** (mediana de 1,5 a 2,8 s). Nunca passam mais de ~5,5 s de câmera parada sem algum evento visual, exceto no CTA final.
5. **Punch-in alternado:** cada corte troca a escala do mesmo take (aberto 100%, médio ~120–150%, fechado ~140–200%), o que esconde os jump cuts.
6. **Legenda palavra por palavra, acumulando, sem animação:** branca, bold, sem contorno, com sombra suave, até 3 linhas, sobre o peito (y ≈ 1400–1550). A página zera a cada frase.
7. **Cor com significado, usada pouco:** vermelho = dor, amarelo = alerta/conceito, verde = solução/marca. Texto comum não leva cor.
8. **Palco desfocado:** o próprio take, com desfoque gaussiano forte, vira fundo para logo, tipografia grande, ícones e listas. É o recurso mais usado.
9. **Flash branco com rampa de desfoque (3–6 quadros) + whoosh** marca cada virada de capítulo (gancho → produto, problema → solução, entrada do CTA).
10. **Logo Beeno uma vez só**, grande e centralizado, entrando rápido com borrão de movimento, de 0,3 a 0,9 s **antes** de o nome ser dito.
11. **Motion design "Beeno dark"** para explicar o produto: fundo verde quase preto, grade fina, cards escuros, Poppins, prints reais da UI com zoom, contadores e checklist ✓/✗.
12. **B-roll literal ou metáfora direta da fala**, de 1,4 a 4 s. Geralmente em tela dividida (câmera em cima, B-roll embaixo, emenda em degradê) e às vezes em tela cheia.
13. **Som:** whoosh nos flashes, impacto grave em logo e tipografia de ênfase, pop em cada item que estala, teclado no texto datilografado. Trilha opcional, baixa (12–18 dB abaixo da voz), que muitas vezes só entra na virada.
14. **Final seco:** CTA falado ("clica no link e agenda uma reunião"), com legenda, **sem cartela final, sem logo, sem URL**. Termina na imagem ou com 3–16 quadros de preto.
15. **Arco fixo:** gancho (0–5 s) → problema/agitação → "é aí que entra o Beeno" → benefícios → CTA (últimos 3–8 s).

---

## 2. As três famílias de vídeo

Os 11 vídeos se dividem em três "sotaques" do mesmo estilo. Antes de planejar, escolha uma família de acordo com o material bruto.

| Família | Vídeos | Captação | Marcas registradas |
|---|---|---|---|
| **A. Estúdio** | Criativo 02, 03, 04, 05 | Tripé, mesa com notebook, estante com "@" e plantas, luz quente | 3 escalas de punch-in, P&B no gancho, palco desfocado, tela dividida com B-roll de banco, ilustração/ícones, legenda Montserrat com cores semânticas, trilha baixa |
| **B. Selfie / UGC** | Criativo 01, Reels 01, Reels 02 | Celular na mão, janela ao fundo, contraluz | Jump cuts no mesmo enquadramento ou punch-in leve, tela dividida com B-roll, mockup de UI em fundo escuro, cartela preta com karaokê, palavra única gigante |
| **C. Evento (Blip ID)** | Frase Blip ID, 16-09, beeno 08-09, beeno 10-09 | Selfie em pé num evento, microfone na mão | O cenário vira gancho ("tá vendo esse logo?"), **blocos longos de motion graphic Beeno dark (6–20 s, 27–56% do vídeo)**, flash de exposição, impactos graves, legenda SF Pro/Inter, sem B-roll |

**Regra prática:**
- vídeo de tripé com o cenário do escritório → A;
- celular na mão → B;
- gravado em evento ou com algo físico para apontar → C;
- assunto muito "de produto" (fluxo, funil, integração) → puxe os blocos de motion graphic da família C, qualquer que seja a família.

---

## 3. Estrutura narrativa e roteiro

### 3.1 Arco (tempos medianos)
| Ato | Duração | O que acontece | Recurso visual típico |
|---|---|---|---|
| Gancho | 0 → 3–5 s | Qualifica o público ou crava a dor | Logo do Blip na palavra "Blip", P&B com número vermelho, palavra gigante, cenário apontado |
| Problema / agitação | até ~15–30 s | Historinha concreta do lead perdido / cliente repetindo / ferramentas separadas | Tela dividida com B-roll, palco desfocado com palavra-chave, cartela preta, gráfico dark com ✗ |
| Virada | 1 momento | "É aí que entra / é exatamente isso que / é por isso que o Beeno existe" | Flash branco → logo Beeno no palco desfocado |
| Solução / benefícios | 8–20 s | Lista do que o produto faz | Mockup/print da UI, pílulas ou ✓ que entram uma a uma, ícones, contadores |
| CTA | últimos 3–8 s | "Clica no link (abaixo) e agenda uma reunião/demonstração (comigo / com a gente)" | Volta para a câmera nítida, flash de entrada, punch-ins curtos, sem cartela |

### 3.2 Fórmulas de gancho que aparecem
- **Qualificação por ferramenta:** "Se você usa Blip…", "Se a sua empresa usa Blip e seu CRM é HubSpot, RD Station…"
- **Número da dor:** "Seu cliente já falou com a sua empresa **5 vezes** e o vendedor atende como se fosse a **primeira vez**?"
- **Quebra de crença:** "Muita gente acha que CRM é uma agenda de contato chique. **Não é.**"
- **Storytelling:** "Deixa eu te contar sobre a venda mais cara que a sua empresa perde…"
- **Cenário:** "Tá vendo esse logo aqui atrás de mim?", "Olha o que está escrito atrás de mim…"
- **Metáfora:** "Se você usa o Blip, parabéns, você tem uma **Ferrari** na mão. Agora, se o seu CRM não tem… é um **Fusca**."
- **Dor de custo:** "Você paga uma ferramenta pro marketing, outra pro comercial, outra pra registrar os leads…"

### 3.3 Frases de virada e de CTA
- **Virada:** "conheça o Beeno", "o Beeno resolve isso", "é exatamente esse buraco que o Beeno resolve", "é por isso que o Beeno existe", "é aí que entra o Beeno".
- **CTA:** "Clica no link (abaixo / aqui) e agenda uma reunião comigo", "…que eu mesmo vou te mostrar na prática", "Chama a gente agora mesmo e conheça a plataforma", "Quer ver como isso funciona na sua operação?".

### 3.4 Correções de transcrição frequentes
O Whisper erra a marca e o parceiro. Corrija **sempre** antes de gerar legenda:
- Bino / Bin / Binance → **Beeno**
- Bleep / Blipe → **Blip**
- link da Bill → link da **bio**
- Segure → **Sincroniza**

---

## 4. Ritmo e montagem

### 4.1 Números de referência
| Medida | Faixa nos 11 vídeos | Alvo |
|---|---|---|
| Palavras por segundo | 3,27 – 4,31 | ~3,7 |
| Maior pausa que sobrou | 0,28 – 0,50 s | ≤ 0,35 s |
| Duração média de plano de câmera | 1,9 – 3,2 s | ~2,2 s |
| Plano mais curto | 0,47 – 1,27 s | ~0,6–0,9 s em palavra de impacto |
| Cortes por minuto (só câmera) | 18 – 28,5 | ~25 |
| Eventos visuais (corte, texto especial, gráfico, ícone) | 1 a cada ~1,5–2 s | 1 a cada ~2 s |
| Posição do corte | −0,13 a +0,05 s do início da 1ª palavra | 1–2 quadros antes da palavra |
| Fala → fim do vídeo | 0,14 – 0,63 s | ~0,3 s |

### 4.2 Pausas e cortes no estúdio (atenção à regra `locked-final-cut`)
Nos vídeos de referência, as pausas são cortadas e cada frase é um corte seco. No estúdio, **o vídeo gravado é intocável** (ver `CLAUDE.md` na raiz). Há dois caminhos, e quem decide é a pessoa:
- **Com pedido explícito para tirar as pausas** (como já aconteceu no projeto 001): gere uma **cópia** com `ferramentas/cortar_pausas.py`. Ele corta pausas ≥ 0,4 s deixando 0,1 s de respiro, tira a espera do início e mantém 0,35 s depois da última fala. O script também remapeia o `palavras.json`. O master original fica intocado e a edição se faz sobre a cópia, que passa a ser o novo "master" daquela edição. Registre isso no `plano.md`.
- **Sem esse pedido:** não corte nada. Imite o ritmo com **eventos a cada ~2 s no início das frases**: troca de escala (punch-in simulado com `scale` sobre o vídeo, sem mexer no tempo), palco desfocado, flash, tela dividida, gráfico.

### 4.3 Punch-in (escala por plano)
- **Família A:** 3 escalas, trocando a cada corte (aberto 100% → médio ~140–150% → fechado ~185–200%). O Criativo 03 sincroniza as três escalas com três itens falados ("marketing / comercial / registrar leads").
- **Família B/C:** 2–3 níveis mais suaves (100 / 110–120 / 140–145%). Em selfie na mão, às vezes não há punch-in, só jump cut.
- **Punch-in seco de impacto** (~150–200%) em palavras de negação ou números ("Não é.", "5 vezes", "te dá mais venda fechada").
- **Zoom lento dentro do plano:** só no Reels 02 (+3 a 6% por segundo). O padrão geral é escala **parada** dentro do plano: nada de efeito Ken Burns contínuo.
- No Remotion, a âncora do `scale` é o centro do rosto. Calcule-a pelos quadros reais (regra do rosto livre) e nunca corte o queixo nem a testa.

---

## 5. Legendas

### 5.1 Legenda base (vale para 100% dos vídeos)
| Propriedade | Valor |
|---|---|
| Fonte | **Montserrat Bold 700** (8 de 11 vídeos). Alternativa na família C: SF Pro Display / Inter SemiBold |
| Corpo | 65–78 px (Montserrat); 80–84 px (SF Pro). Alvo: **72 px** Montserrat |
| Entrelinha | ~1,3 (≈ 96 px para 74 px de corpo) |
| Cor | `#FFFFFF` |
| Contorno | nenhum |
| Sombra | suave: `text-shadow: 3px 4px 6px rgba(0,0,0,.45)` |
| Caixa | baixa, como na fala; maiúscula só no início do vídeo e em nomes próprios (Beeno, Blip, CRM) |
| Pontuação | mantém "?" e "!"; sem ponto final |
| Alinhamento | centralizado, largura máxima de ~810–870 px (75–80%) |
| Linhas | até 3, com ~3–4 palavras / ~22 caracteres cada |
| Posição padrão | **sobre o peito, abaixo do queixo:** centro em y ≈ 1450 (faixa de 1370–1620). Em plano fechado sobe para y ≈ 1110–1300 |
| Revelação | **palavra por palavra, acumulando**, seca (sem pop, fade ou escala), no quadro de início da palavra (0–2 quadros antes; nunca antes disso). **Layout da página pré-calculado:** cada palavra já surge na posição final, sem reorganizar o bloco |
| Página | uma por frase (quebra em vírgula/ponto). Zera em cada corte; pode ficar 1–6 quadros sem legenda entre páginas |
| Some quando | entra logo, cartela, gráfico de tela cheia ou tipografia especial (o texto da cena substitui a legenda) |

**Posição por tipo de plano:**
- tela dividida → sobre a emenda (y ≈ 860–1000);
- B-roll ou cartão escuro → topo (y ≈ 185–340) ou a ~58% da altura;
- mockup de UI → topo, alinhada à esquerda (x ≈ 130).

### 5.2 Cores semânticas (destaque em palavra)
| Função | Cor | Exemplos |
|---|---|---|
| Dor, erro, negação | vermelho **`#EC1D1D`** (legenda) / `#EF404A` (gráfico) | "primeira vez?", "TUDO DE NOVO", "se repetir", "5 vezes" |
| Alerta, confronto, conceito-chave | amarelo **`#F4C70F`** (`#EFCE1A` em caixa alta) | "Desculpe…" (P&B), "marketing", "SEGUNDA" |
| Solução, marca, virada | verde **`#00CB88`** (marca), `#00AF08` (palavra), `#0ED20E` (frase-tese) | "venda", "agora se torna visível", contorno em "AUTOMATICAMENTE" |
| Parceiro Blip | azul **`#0090FF` / `#2A8EF6`** | "comercial", "Blip" |

**Regras de uso:**
- No máximo 1–2 palavras coloridas por página e 3–6 por vídeo. Texto comum fica branco.
- Uma cor por conceito, mantida no vídeo inteiro. Por exemplo, Marketing é sempre amarelo e Vendas sempre azul, inclusive nos painéis de tela dividida.
- Palavra de ênfase em **CAIXA ALTA** e ~1,3× maior, dentro da própria legenda ("SEM CRM", "É TER UM CRM", "NINGUÉM").

### 5.3 Tipografias especiais (substituem a legenda base por 1–3 s)
Use 2–5 por vídeo, sempre nas frases-tese e sempre sobre o **palco desfocado** ou uma **cartela preta**.

| Nome | Visual | Animação | Onde apareceu |
|---|---|---|---|
| **Palavra única de impacto** | Montserrat Black Italic, CAIXA ALTA, ~105 px, amarelo-limão `#EEF20A` com contorno preto de 8 px | uma palavra por vez, trocando no tempo de cada palavra | Reels 02 ("NUNCA", "PREJUÍZO", "INVISÍVEL") |
| **Linha-chave grande** | Montserrat ExtraBold ~100 px, palavra-chave em caixa alta ~125 px colorida | acumula palavra a palavra | Reels 02 ("O time só vê na SEGUNDA") |
| **Cartela preta com karaokê** | fundo `#000`, caixa alta pesada ~85 px, palavra falada em verde-limão `#A6FD0A` | página inteira de uma vez, cor anda com a fala | Reels 02, Criativo 03 ("TODOS OS DIAS", só branca) |
| **Karaokê vazado** | sans extra larga black (estilo Unbounded/Monument), caixa alta; palavra falada sólida branca, demais só contorno branco de 4 px | avança por palavra | 08-09 ("BELEZA, O LEAD / CHEGOU PELO BLIP / E AGORA?") |
| **Máquina de escrever** | serifada (Playfair/DM Serif/Libre Caslon) ou sans regular fina, com cursor em bloco ▌ piscando | ~11–15 caracteres/s, com som de tecla | 08-09, Reels 01, Criativo 02 (lista de recursos) |
| **Tipografia mista** | linha sans + linha CAIXA ALTA black + linha serifa itálica | letras espalhadas em laranja `#FC7828` se juntam e ficam brancas em 4–6 quadros | Frase Blip ID |
| **Palavra com eco** | sans black branca ~110 px | cópias espaçadas convergem em ~0,3 s + impacto grave | 16-09 ("APOSTA") |
| **X desenhado** | linha em Bold caixa alta + X vermelho `#E90002` | traçado em 2 traços (~0,2 s + 0,15 s) + som de rabisco | 10-09 ("É TER UM CRM") |
| **Neon glow** | arredondada pesada (Fredoka/Nunito Black), linha ativa verde neon `#17FF17` com brilho, vermelho `#F71616` na dor | karaokê por linha | Criativo 04 |
| **Contorno vazado** | "ROBUSTO" cheio + "DE VERDADE" só contorno, Montserrat/Archivo Black | entra seco | Reels 01 |
| **Texto atrás do sujeito** | "ATENÇÃO" vermelho `#D1000C` atrás da cabeça, com fogo | requer máscara de recorte da pessoa (avançado, opcional) | 16-09 |

Sem emoji em nenhum dos 11 vídeos.

---

## 6. Identidade visual

### 6.1 Paleta medida
| Uso | Hex |
|---|---|
| Logo Beeno (wordmark) | **`#00CB88`** (aparece com brilho até `#12E68A`) |
| Pílula/tag verde | `#00CD8A` |
| Menta de destaque nos gráficos | `#60E1B4`, `#5EDDB1`, `#45D49E` |
| Verde de check ✓ | `#15A56B` |
| Gradiente de barra/balão | `#1EAB54 → #188A45`, `#2BB673 → #3ED598` |
| Fundo "Beeno dark" | **`#091B15`** (faixa `#04100C`–`#091C16`) |
| Brilho radial do fundo | `#09402D` / `#083D2B` (azul-petróleo `#082E37` nas cenas da Blip) |
| Título branco dos gráficos | `#FAFFFE` |
| Linha de contexto (cinza-verde) | `#8CA69E`–`#A9BAB3` |
| Vermelho de dor (gráfico) | `#EF404A`, `#F26966`, ✗ `#D94852` |
| Azul Blip | `#0096FB` / `#0C94F8` |
| Amarelo marca-texto | `#F9EA2D` (caixa com texto preto) |
| Painéis sólidos de tela dividida | amarelo `#FFE226`, azul `#2666FF` |

### 6.2 Logo
- **Lockup:** "beeno" verde + "by skeps" pequeno em branco, alinhado à direita, embaixo. Arquivos em `assets/brand/`.
- **Tamanho e posição:** centralizado, 59–80% da largura (~633 px), com centro em y ≈ 850–1150.
- **Fundo:** o palco desfocado (padrão), um overlay verde sobre o palco (`rgba(0,203,136,.6)`, Criativo 03) ou um card branco (Criativo 03, versão verde).
- **Entradas, sempre em 5–12 quadros com borrão de movimento e ease-out forte, uma das três:**
  - **whip horizontal** (desliza de −120% → 0);
  - **zoom-out** de ~3× para 1×;
  - **deslize gigante pela direita** encolhendo.
- **Timing:** de 0,3 a 0,9 s **antes** da palavra "Beeno". Fica na tela de 1 a 1,5 s.
- **Som:** boom grave ou whoosh junto com a entrada.
- **Variação de diagrama** (Criativo 02): o logo sobe para o topo (y 144–310), uma linha tracejada branca em "S" se desenha até um mockup de notebook que sobe de baixo, e um selo verde de check estala no canto.
- **Co-branding:** lockup "beeno ⇄ blip" pequeno no topo dos gráficos de produto.
- **Logo de parceiro:** o logo do Blip (balão azul + "blip") entra **exatamente na palavra "Blip"**, no topo (y 270–474) ou no peito, com escala + borrão em 8–9 quadros e boom grave. Logos de HubSpot / RD Station aparecem na tela de um notebook (B-roll), trocando por whip na palavra.
- **Nunca:** marca d'água fixa, logo no canto, cartela final com logo.

### 6.3 Tipografia
- **Legenda:** Montserrat Bold (padrão) ou SF Pro / Inter SemiBold (família C).
- **Gráficos e motion:** **Poppins** em 3 níveis:
  - contexto: Medium ~44 px, cinza-verde;
  - título: Bold ~84 px, branco;
  - destaque: a palavra do título em verde-menta, vermelho ou azul.
- **Ênfase:** Montserrat Black / ExtraBold (Italic na palavra única).
- **Contraste:** uma serifada (Playfair / DM Serif) só para máquina de escrever ou tipografia mista.

### 6.4 Tratamento de cor da câmera
- Sem LUT, cor natural.
- **P&B 100%** só no punch-in do gancho, no momento de confronto (Criativo 04 "5 vezes", Criativo 05 "Desculpe…"). Nesse trecho, a legenda vai para amarelo ou o número para vermelho.
- Sem vinheta.

---

## 7. Catálogo de cenas (os blocos de montagem)

Para o plano, dê a cada trecho um destes formatos. As durações são as dos exemplos.

| Cena | Duração | Como é | Quando usar |
|---|---|---|---|
| `camera` | 0,6–4 s | Talking head nítido, com escala do punch-in; legenda base | Padrão; opinião e ligação entre ideias |
| `camera-impacto` | 0,6–2 s | Punch-in seco 150–200%, opcionalmente P&B, número ou palavra em cor | Número, negação, "Não é." |
| `palco` (palco desfocado) | 1,3–6 s | Mesmo take com `blur(25–40px)`, geralmente mais aberto; tipografia especial, logo, ícones, lista, caixas digitadas | Frase-tese, lista de recursos, entrada do logo |
| `split` (tela dividida) | 1,4–4 s | Câmera em cima (~45–53%), B-roll embaixo a partir de y ≈ 850–1010; emenda em **degradê** de 140–300 px (a parte de baixo da câmera escurece para preto de y ≈ 700 a 1000); legenda na emenda | Toda vez que a fala cita um objeto ou uma situação concreta |
| `split-painel` | ~1 s | Split lateral: câmera de um lado (~50%), painel de cor sólida do outro com um rótulo | Contraste entre dois lados ("Marketing" × "Vendas") |
| `broll` | 2,4–4 s | B-roll em tela cheia com legenda no topo ou a 58% | Metáfora de "sistema", ambiente |
| `cartela` | 1–2 s | Fundo preto `#000`, tipografia caixa alta, karaokê ou palavra a palavra | Consequência dura ("ELA SIMPLESMENTE VAI NO CONCORRENTE") |
| `logo` | 1–1,5 s | Logo Beeno sobre o palco | Virada para a solução, uma vez |
| `ui` (motion de produto) | 4–20 s | **Beeno dark** (seção 8) | Explicar o produto, mostrar a dor em números |
| `faixa-ui` | ~7 s | Painel horizontal escuro (y 426–1610) com print da UI sobre o take aberto e desfocado | Demonstração de print sem tirar a pessoa de cena |
| `tela-real` | 3–15 s | Celular filmando a tela do notebook, com a câmera acompanhando a fala | Demonstração crua (**dados fictícios**, nunca contatos reais) |
| `ilustracao` | ~8 s | Ilustrações chapadas estilo clip art (tipo Irasutoya) sobre o palco, balões de fala, deslizes de 9 quadros com overshoot | Contar uma historinha frase a frase |
| `pilulas` | 3–4 s | Tags `#00CD8A`, raio 20 px, Montserrat Bold 76 px branca, padding 40×30, empilhadas com 35 px de vão, cada uma estalando na sua palavra + pop | Lista de etapas ou recursos |
| `icones` | 5–9 s | Logo central + 4 ícones animados em disco branco (230 px, aro preto), um por benefício, entrando com giro em 4 quadros | Lista de 3–4 benefícios |
| `cta` | 3–8 s | Câmera nítida, legenda base, 2–4 punch-ins curtos | Fechamento |

**Proporção típica de um vídeo de 40 s:**
- **família A:** ~60% `camera`, ~20% `palco`, ~10% `split`, ~10% `ui` / ilustração;
- **família C:** 40–55% `ui`.

---

## 8. Motion design "Beeno dark" (gráficos de produto)

Este é o sistema gráfico que se repete em 6 vídeos (Reels 01, Reels 02, Frase Blip ID, 16-09, 08-09, 10-09).

**Fundo**
- `#091B15` com radial-gradient `#09402D` a ~40% no centro;
- grade fina de ~40 px a `rgba(255,255,255,.03)`;
- manchas de bokeh verdes desfocadas nos cantos (opcional).

**Composição**
- Ilustração na metade de cima (y ≈ 200–1150).
- Texto em baixo, em y ≈ 1300–1500: linha de contexto cinza-verde (~44 px) + título branco Bold (~84 px) com a palavra de destaque colorida.
- Listas ✓/✗ de ~48 px alinhadas à esquerda (x ≈ 340), montadas item a item na palavra falada.

**Elementos**
- Cards escuros "de vidro" (`#0A1E14`, borda verde de 1 px com brilho, cantos de 12–16 px).
- Prints reais da UI (Blip Desk, extensão Beeno, kanban "Negócios") em cards com sombra.
- Chat de WhatsApp com balões entrando um a um. O lead fictício recorrente é "Mariana".
- Card "★ Resumo por IA" e pipeline com etapas e checks.
- Contadores subindo (184 conversas / 0 vendas; R$ 298 mil → 437 mil), barra de meta enchendo.
- Popups ("Follow-up automático", "Distribuição automática") e cursor clicando.
- **Motivo-personagem:** um ponto verde brilhante = o lead (cai do topo, vira balões, dissolve em partículas quando "some").

**Animação**
- Cada cena começa com ~6 quadros de fundo vazio.
- O texto entra com fade + subida de 20–30 px em 6–8 quadros.
- A linha anterior escurece quando entra a seguinte.
- Popups entram com escala + fade.
- Câmera virtual com push-in e zoom-out dentro do print.
- Uma mudança interna a cada 1–2,5 s, **sempre na palavra-chave**.

**Texto**
- **Parafraseia** a fala em frases curtas, não transcreve.
- Por exemplo, fala "volume de conversa que não tem venda" → tela "muito volume de conversa / **e nenhuma venda.**".

**Cores por marca:** brilho azul-petróleo nas cenas sobre o Blip e verde nas cenas sobre o Beeno. O nó muda de azul para verde quando o Beeno entra.

**Legenda base:** some durante o bloco.

---

## 9. Transições e efeitos

| Efeito | Quadro a quadro | Uso |
|---|---|---|
| **Corte seco** | — | ~80% das trocas |
| **Flash branco com desfoque** (assinatura) | q1–2: desfoque 0 → 20 px + brilho subindo; q3–4: branco puro (a legenda ou o logo novo já pode aparecer no branco); q5–6: novo plano revelado, às vezes com tom quente `#FFD27A` a 40% → 0. Total: 3–6 quadros (0,1–0,2 s) | 2–4 por vídeo: gancho → produto, problema → solução, entrada do logo, entrada do CTA |
| **Estouro de exposição** (sem chegar ao branco) | clareia em 3 quadros, 1 quadro estourado, o novo plano entra claro e decai em 2 | Família C, entre planos de câmera e antes de cortar para o fundo escuro |
| **Flash quente** | superexposição amarelada decaindo em 1–6 quadros | Virada problema → solução (Criativo 02 e 03) |
| **Entrada no palco** | corte seco para a versão desfocada ou rampa de desfoque em ~3 quadros; saída por corte seco | Sempre |
| **Whip com borrão de movimento** | translateX com blur direcional, 5–12 quadros | Logos e troca de logos |
| **Zoom-blur + bloom** | rosto aumenta, desfoca e estoura; a cena nova entra desfocada com zoom-out, 8 quadros | Câmera → tela/demonstração |
| **Dissolve com zoom** | 4 quadros | Entrada de B-roll em tela cheia |
| **Blur de 1 quadro** antes do corte | — | Entrada em cartão preto |

**Nunca usados:** shake, glitch digital, speed ramp, whip pan de câmera, vinheta, fade para preto longo.

---

## 10. Som

### 10.1 Medições
| Vídeo | Loudness | Trilha | Observação |
|---|---|---|---|
| Criativo 01 | −20,8 LUFS | baixa, contínua | ~15 dB abaixo da voz |
| Criativo 02 | −19,8 | **entra aos ~15 s**, na virada | antes disso, só voz |
| Criativo 03 | −20,2 | contínua | |
| Criativo 04 | −22,4 | contínua | ~15 dB abaixo |
| Criativo 05 | −17,3 | contínua | |
| Reels 01 | −23,1 | contínua | ~12 dB abaixo |
| Reels 02 | −24,5 | **sem trilha** | só voz + SFX |
| Frase Blip ID | −18,1 | sem trilha | ambiente do evento |
| 16-09 | −18,6 | sem trilha | ambiente do evento |
| beeno 08-09 | −15,0 | **120 BPM entrando aos 16,5 s**, na virada para o problema | mono |
| beeno 10-09 | −13,6 | sem trilha | mono |

**O que tirar disso:**
- Nenhum vídeo tem silêncio (pausas cortadas + ambiente ou trilha por baixo).
- Quando há trilha, ela fica 12–18 dB abaixo da voz, sem melodia que dispute com a fala. Pense em batida discreta de 100–125 BPM.
- É comum a trilha **entrar na virada**, não no início.
- Os exemplos chegam a picos de +0,6 dBFS (estouram). **Aqui entregue entre −16 e −14 LUFS com pico em −1 dBTP**, usando `ferramentas/masterizar.sh`.

### 10.2 Efeitos sonoros (mapa evento → som)
Os sons estão em `ferramentas/gerar_sfx.py` (gera os arquivos).

| Evento visual | Som | Arquivo sugerido | Volume relativo à voz |
|---|---|---|---|
| Flash branco / troca de capítulo | whoosh curto (0,15–0,3 s, ruído estéreo de banda larga), às vezes precedido de riser | `whoosh_curto.wav` (+ `riser.wav` na virada principal) | −6 a −10 dB, caindo na pausa |
| Entrada do logo Beeno ou do logo Blip | boom/impacto grave (40–110 Hz) + whoosh | `impacto.wav` + `whoosh.wav` | −6 dB |
| Tipografia de ênfase (APOSTA, ATENÇÃO, SEM CRM, painel de split) | impacto grave | `impacto.wav` | −8 dB |
| Pílula, ícone ou item de lista que estala | pop | `pop.wav` | −12 dB |
| Máquina de escrever | teclas a cada novo item | `tick.wav` / `clique.wav` | −15 dB |
| Entrada de gráfico / UI | clique | `clique.wav` | −14 dB |
| X desenhado / erro | rabisco de marcador / erro | `erro.wav` | −10 dB |
| Card chegando em "Fechado" / venda | ding de sucesso | `notificacao.wav` | −10 dB |
| B-roll com ambiente próprio (ex.: carro na estrada) | o som do próprio B-roll, baixo | — | −20 dB |

**Regras gerais:**
- O SFX começa 1–2 quadros **antes** do evento visual.
- Os cortes que só tiram pausa **não** levam som.
- Nunca mais de um SFX forte a cada ~1,5 s.

---

## 11. B-roll e Higgsfield (Nível 2)

### 11.1 O que os exemplos usam
Todo o B-roll é de banco de imagens, realista. Nada foi gerado por IA.

| Fala | B-roll | Relação |
|---|---|---|
| "a venda mais cara que sua empresa perde" | mãos dobrando/rasgando notas de dinheiro | metáfora |
| "alguém vê seu anúncio" | mão rolando um app no celular | literal |
| "manda mensagem no WhatsApp" | celular com conversa, dedo digitando | literal |
| "estatística de venda perdida" | relatório impresso com barras vermelhas e caneta | literal |
| "sistema / funil / dono" | HUD de dados neon (magenta/ciano) | metáfora (**fora da paleta**: prefira em verde) |
| "Ferrari" / "Fusca" | carro esportivo vermelho na estrada / Fusca em estrada de terra | metáfora da fala |
| "sua planilha, seu controle" | mãos digitando numa planilha | literal |
| "o cliente explica tudo de novo" | homem de terno ao telefone, gesticulando | literal |
| "puxa o histórico de conversa" | mãos digitando no celular, tom verde-petróleo escuro | semiliteral |
| "usa Blip / HubSpot / RD" | POV de notebook com o logo na tela (trocado na pós) | literal |

### 11.2 Regras para gerar na Higgsfield
- **Sem texto, letras, logos ou telas legíveis** na imagem gerada (ver `CLAUDE.md` na raiz). Telas de celular e notebook saem desfocadas ou vazias. Logos, números e prints entram no Remotion por cima (screen replacement).
- Sem rostos identificáveis em primeiro plano; mãos e objetos funcionam melhor.
- **Duração útil:** 1,5–4 s (gere 4–5 s e use o trecho do meio).
- **Enquadramento:** como o B-roll vai para a metade de baixo do split, componha o assunto no centro de uma área 9:8. Gere em 9:16 e recorte.
- **Dois "looks" possíveis:**
  - **Realista neutro** (padrão dos splits): luz natural ou de escritório, cores reais, sem grade.
  - **Verde escuro de marca** (B-roll de tela cheia): ambiente escuro, tom verde-petróleo, profundidade de campo rasa.
- Sufixo de prompt sugerido:
  - Neutro: `Realistic stock-style footage, natural daylight, true-to-life colors, shallow depth of field, close-up on hands and objects, no readable text, no letters, no logos, no watermark, no faces. Vertical 9:16.`
  - Dark de marca: `Cinematic dark moody shot, deep teal-green color grade (#061816), soft green rim light (#00CB88), shallow depth of field, bokeh, no readable text, no letters, no logos, no watermark, no faces. Vertical 9:16.`
- Respeite o orçamento (ver `CLAUDE.md` na raiz). Uma edição neste estilo costuma usar **2 a 6 B-rolls**; a família C usa zero.

---

## 12. Receita de automação (passo a passo para o Claude Code)

1. **Assistir e transcrever:** `ferramentas/transcrever.py` → `palavras.json`. Aplique as correções da seção 3.4.
2. **Classificar a família** (seção 2) pelo cenário e pela captação.
3. **Pausas:** perguntar à pessoa se pode gerar a cópia sem pausas (seção 4.2). É o que mais aproxima o resultado do estilo. Sem autorização, seguir sem cortar.
4. **Mapear o arco:** marcar no `palavras.json` o gancho, a virada (a frase com "Beeno"), o início dos benefícios e o CTA.
5. **Montar a timeline**, uma linha por frase:
   - cada frase recebe uma cena (seção 7) e uma escala de punch-in diferente da anterior;
   - no máximo ~5,5 s sem evento;
   - flash + whoosh nas 2–4 viradas;
   - logo Beeno 0,3–0,9 s antes do nome;
   - 2–5 tipografias especiais nas frases-tese;
   - tela dividida com B-roll quando a fala citar objeto ou situação;
   - bloco Beeno dark quando o assunto for o produto.
6. **Legenda:** páginas por frase, ≤3 linhas e ≤22 caracteres por linha, palavras reveladas no `s` de cada uma, posição y por cena, 3–6 palavras coloridas no vídeo inteiro (seção 5.2).
7. **Som:** SFX pelo mapa da seção 10.2. Trilha opcional a −15 dB, de preferência entrando na virada. Masterizar entre −16 e −14 LUFS, pico −1 dBTP.
8. **Final:** CTA na câmera nítida, sem cartela. Terminar ~0,3 s depois da última palavra.
9. **Validar:**
   - duração igual à do master usado (±1 quadro);
   - nenhum conteúdo antes de ser dito;
   - rosto livre (seção 13);
   - prints com dados fictícios;
   - stills de revisão para aprovação.

### 12.1 Componentes Remotion a ter (parâmetros)
- `LegendaBeeno`: Montserrat 700, 72 px, `#FFF`, sombra `3px 4px 6px rgba(0,0,0,.45)`, layout fixo por página, `opacity` em degrau no quadro de `s`, prop `y` por cena, prop `cores` (mapa palavra → hex).
- `PunchIn`: `scale` 1,0 / 1,2–1,5 / 1,4–2,0 por segmento, âncora no centro do rosto. Sem animação dentro do plano.
- `PalcoDesfocado`: `<OffthreadVideo>` do mesmo trecho com `filter: blur(30px)`, `scale(0.9–1.0)` (take mais aberto) e overlay verde opcional `rgba(0,203,136,.6)`.
- `FlashBranco`: 2 quadros de blur 0 → 20 px + `brightness` 1 → 3, 1–2 quadros `#FFF`, branco 0,85 → 0 no plano novo, tom quente opcional.
- `LogoEntrada`: `variante` = `whip` | `zoom` | `deslize`, 5–12 quadros, ease-out forte, borrão direcional (feGaussianBlur `stdDeviation="40 0"` ou 6–8 cópias com opacidade decrescente).
- `SplitBroll`: câmera em `translateY(-22%)`, `scale` 1,4; B-roll de y 850/1010 → 1920; máscara `linear-gradient(to bottom, transparent 850px, black 1050px)`; escurecimento da câmera de y 700 → 1000.
- `CenaBeenoDark`: fundo, grade, brilho, Poppins em 3 níveis, spring de opacidade + `translateY(24px → 0)` em 8 quadros, ✓/✗ por palavra, contador, print com zoom.
- `TipografiaEspecial`: variantes `palavra-unica`, `karaoke`, `karaoke-vazado`, `maquina`, `mista`, `eco`, `x-desenhado`.
- `Pilulas`, `IconesCirculo`, `CartelaPreta`, `TrechoPB` (`saturate(0)` + legenda amarela).

---

## 13. Onde os exemplos quebram as regras do estúdio (não copiar)

- **Rosto coberto:**
  - No Reels 01, um ícone de setas fica sobre o nariz e a boca.
  - Nos palcos desfocados, a tipografia grande cai sobre o rosto (y ≈ 900–1000).
  - **Aqui o rosto continua livre** (ver `CLAUDE.md` na raiz): no palco, posicione o texto abaixo do queixo (y ≈ 1050–1350) ou recue o take (`scale 0.9`) para o rosto subir, e mantenha ícones fora da área do rosto.
- **Dados reais:** no Criativo 01, a tela filmada mostra nomes e telefones reais de contatos. Use dados fictícios ("Mariana Souza", "Ana / Bruno / Carla").
- **Trecho sem legenda:** no Reels 02 (35–39 s), a legenda some sobre o B-roll. Aqui, legende sempre.
- **Pico estourado:** vários exemplos passam de 0 dBFS. Masterize.
- **HUD neon magenta/ciano:** foge da paleta. Prefira as versões verdes.
- **Legenda cortada no fim:** no Frase Blip ID, a última palavra não chega a aparecer. Garanta que o vídeo dure até ~0,3 s depois da última palavra.

---

## Anexo: ficha de cada vídeo

| Vídeo | Duração | Família | Gancho | Recursos marcantes |
|---|---|---|---|---|
| Criativo 01 | 33,2 s | B | "Se você usa Blip… você precisa conhecer o Beeno" | Logo Blip na palavra; logo Beeno com whip sobre palco; zoom-blur para a tela filmada (66% do vídeo); mão na lente como transição |
| Criativo 02 | 30,6 s | A | Ferrari × Fusca | 3 escalas; splits com B-roll de carros; lista em máquina de escrever sobre palco (5,9 s); logo → linha tracejada → notebook → selo ✓; flash quente; trilha entra aos 15 s |
| Criativo 03 | 42,2 s | A | "Você paga uma ferramenta pro marketing, outra…" | 3 cores no gancho (amarelo/azul/verde) + escalas sincronizadas; cartela preta "TODOS OS DIAS"; splits com painel amarelo/azul; funil animado de 7,5 s; pílulas com pop |
| Criativo 04 | 52,6 s | A | "…já falou com a sua empresa 5 vezes" | P&B + "5" vermelho; B-roll verde escuro; split com homem ao telefone; ilustração narrativa de 8 s; ícone de sync girando; texto neon glow; termina em preto só com a legenda |
| Criativo 05 | 23,5 s | A | "Se a sua empresa usa Blip e seu CRM é HubSpot, RD…" | Split com notebook trocando logos por whip na palavra; P&B com legenda amarela; logo + 4 ícones em disco branco |
| Reels 01 | 31,6 s | B | "CRM não é uma agenda de contato chique. Não é." | Punch-in de 160% no "Não"; 4 cards de UI em Beeno dark; caixas digitadas com serifa; "ROBUSTO DE VERDADE" vazado; fala mais rápida (4,3 p/s) |
| Reels 02 | 65,6 s | B | "A venda mais cara que sua empresa perde…" | 4 splits com B-roll de banco; 5 estilos de legenda; cartela preta com karaokê verde; palavra única itálica amarela; UI Beeno dark; 3 flashes; sem trilha |
| Frase Blip ID | 36,1 s | C | Aponta o painel "where conversations drive results" | Tradução com marca-texto amarelo; tipografia mista com letras laranja; 20 s de motion de produto (chat, 184 × 0, logo no anel, kanban, R$ 18.500) |
| 16-09 | 40,9 s | C | "Tá vendo esse logo aqui atrás de mim?" | "ATENÇÃO" atrás da cabeça com fogo; dois blocos Beeno dark (12,5 s + 10,5 s) com contadores e popups; "APOSTA" com eco; impactos graves |
| beeno 08-09 | 49,8 s | C | "Deixa eu te contar por que trouxemos o Beeno pro Blip ID" | Karaokê vazado "BELEZA, O LEAD… E AGORA?"; máquina de escrever serifada; ponto-lead que some; faixa de UI sobre palco; batida de 120 BPM a partir da virada |
| beeno 10-09 | 45,2 s | C | "Se você usa Blip… confusão que custa caro" | X vermelho desenhado sobre "É TER UM CRM"; bloco de 20 s Blip (azul) → Beeno (verde); sem punch-in; "O Blip conversa, o Beeno converte" |
