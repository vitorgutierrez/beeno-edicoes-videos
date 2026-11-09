# Técnicas de edição (repertório)

Técnicas testadas e aprovadas em dezenas de anúncios, podcasts e reels editados no mesmo fluxo
(Remotion + HTML + FFmpeg), já traduzidas para a identidade da Beeno. São **repertório**, não regra:
escolha poucas por vídeo e varie entre criativos.

Cores da Beeno usadas aqui: verde `#00CD8A` (só como acento), tinta `#0A1C15`, fundo dark `#091B15`,
vermelho de dor `#EF404A`, amarelo de alerta `#F4C70F`. Fonte: Poppins (motion) e Montserrat (legenda).
Quadro 1080×1920, 30 fps, salvo indicação.

---

## 1. Ganchos e teste A/B

### Um corpo, vários ganchos
- Grave os ganchos em sequência num arquivo só (`GANCHOS.mp4`) e o corpo em outro. Cada gancho + o mesmo corpo vira uma versão (V1, V2, V3…).
- O gancho começa **exatamente** no corte entre tomadas, detectado com `ffmpeg -vf "select='gt(scene,0.3)',showinfo"` ou `scdet`. Começar alguns quadros antes aparece como "pedaço de outro vídeo".
- Nomes: `BEENO_C2_H1_OBJETO` (criativo 2, gancho 1, ideia do gancho).
- Como ler o vencedor: taxa de gancho (views de 3 s ÷ impressões), retenção (ThruPlay ÷ views de 3 s), CTR e custo por lead. Em 3–5 dias escala o vencedor e troca os perdedores.

### Tipos de gancho que funcionaram
- Pergunta direta ao gestor ("Quantos leads o seu time perdeu essa semana sem perceber?").
- **Objeto físico** em cena (algo que se pega na mão e simboliza a dor).
- Repetição com contador: "Mesmo lead. Mesma pergunta. Terceira vez." com o número subindo.
- Abrir direto num depoimento de cliente.
- Loop aberto: começa no resultado e volta para mostrar como chegou lá.
- Os ganchos próprios da Beeno (qualificação por ferramenta, número da dor, quebra de crença, cenário, metáfora) estão em [1-estilo-beeno.md](1-estilo-beeno.md), seção 3.2.

### Como tratar o gancho
- **Com objeto real:** pouco motion por cima. Ênfase no próprio objeto: punch-in, "mira" (cantoneiras nos 4 cantos que fecham sobre ele) e texto grande em blocos curtos **iguais à fala**.
- **Faixa headline** (desde o 1º quadro, no peito ou no topo): caixa verde com a qualificação do público em caixa alta + caixa branca "ESSE VÍDEO É PARA VOCÊ". Poppins ExtraBold ~44–50 px, texto tinta. Já existe em `editor/scenes.py` (`hook`) e em `remotion/_shared/faixa-publico.tsx`.
- **Evitar:** zoom de abertura seguido de outro enquadramento; filtro vermelho quando já há informação na tela. Prefira câmera estável com empurrão lento (100 → 106% no gancho).

## 2. Legendas (escolha uma família por vídeo)

| Família | Como é | Quando |
|---|---|---|
| **Base Beeno** | Montserrat 700, 72 px, branca, sombra suave, palavra a palavra acumulando (ver 1-estilo-beeno, seção 5) | Padrão dos anúncios |
| **Em pedaços** | 1–4 palavras que se substituem no quadro exato de cada palavra; no máximo uma palavra-chave por frase em cor | Ritmo mais rápido |
| **Karaokê** | Caixa alta condensada (Bebas Neue), palavra falada dentro de uma caixa verde com texto tinta | Tela dividida, conteúdo de lista |
| **"Hormozi"** | 2–3 palavras enormes, branco com contorno tinta grosso, palavra-chave verde; cada palavra entra com escala 1,25 → 1 | Criativo mais energético |
| **Nativa do Instagram** | Caixa branca arredondada, texto tinta ExtraBold, 1–2 linhas; outra cor de caixa para outra pessoa falando (ex.: depoimento) | Cara de post orgânico |
| **Sóbria** | Poppins/DM Sans 500, ~46 px, frase normal, 2 linhas, y≈1380, sem caixa, no máximo uma palavra colorida | Cortes de podcast, evento, reels calmos |

Regras que valem para todas:
- Texto grande, número grande, CTA ou cartela na tela → **a legenda some** (nunca duplicar).
- A legenda não pisca nas bordas das transições: o pedaço que começa dentro (ou logo antes) de um destaque fica oculto até o fim dele.
- Tela dividida → legenda no meio, sobre a emenda.
- **Sem transparência no texto** (legendas, títulos, chips e cards sólidos).
- Corrija a transcrição antes de legendar (Bino → Beeno, Blipe → Blip, link da Bill → link da bio).

## 3. Transições

- **Corte seco** é o padrão (~80%).
- **Sem "janela":** ao sair de uma inserção em tela cheia para a câmera desfocada, o desfoque começa **antes**, por baixo do fade. Nunca aparece a câmera nítida por alguns quadros no meio.
- **Sem buraco:** nunca deixar quadros de câmera crua entre um elemento que sai e outro que entra. Card → números: corte seco para a câmera já desfocada.
- **Sem dois cortes seguidos:** um destaque segura até o próximo plano; nada de voltar à câmera crua e dar zoom seco 0,3 s depois.
- **Jump cut escondido:** troca de escala no corte (100% ↔ 108–115%), âncora no centro do rosto, nunca com borda preta. Superimpose de 0,2 s (os dois planos sobrepostos) suaviza cortes do mesmo take.
- **"Assentada":** no corte de cena, o plano novo entra a 104% e assenta em 100% em 0,2 s, com clique de mouse baixo (usado na v5 dos reels).
- **Flash branco com rampa de desfoque** só nas 2–4 viradas de capítulo (ver 1-estilo-beeno, seção 9).
- Para conteúdo sóbrio (podcast, evento): corte seco ou dissolve de 6–10 quadros, corte em J/L (a voz continua sobre o B-roll), sem whoosh nem glitch.
- Glitch e tremor de tela: só em criativo de energia alta, nos impactos, nunca mais de 2–3 por vídeo.

## 4. Tela dividida

- Painel em cima (B-roll, tela do produto ou animação), pessoa embaixo com o rosto inteiro, **filete verde de 2–3 px** na emenda (y≈960).
- A divisão abre e fecha (0,3 s) para a câmera cheia nos clímax.
- Painel com o próprio quadro desfocado e escurecido por trás, para não ter fundo "vazio".
- **Poucos splits, cada um com tempo de leitura** (≥ 2,5 s) — ajuste da v5.
- Diagonal para comparar dois cenários (antes × depois, Blip sozinho × Blip + Beeno).
- Componente: `remotion/_shared/synchronized-split.tsx` (câmera e painel andam juntos) e `CameraEPainel` em `remotion/_beeno/componentes.tsx`.

## 5. Motion e inserções

### Formatos de inserção (cada criativo novo deve usar uma "roupagem" diferente)
| Roupagem | Como é | Bom para |
|---|---|---|
| **Beeno dark** | Fundo `#091B15` com brilho verde a ~7%, grade fina, cards de vidro, Poppins; diagramas que se montam na palavra | Explicar o produto (padrão) |
| **Cards claros** | Cards brancos sólidos sobre o vídeo desfocado; etiquetas, carimbo ("NÃO REGISTRADO"), botão liga/desliga | Processos do dia a dia, antes/depois |
| **Contas na tela** | "8 leads × R$ 15 mil = R$ 120 mil" com números rolando como caixa registradora; barras que sobem | Custo da dor |
| **Painel de controle** | A câmera vira um **card flutuante** que cresce e encolhe sobre um fundo temático; barra de progresso no topo; tipografia cinética gigante | Criativo de energia alta |
| **Papel e caneta** | Papel creme `#F2EDE3`, fita crepe, traço "à mão" em SVG animado (círculo, ✓ verde, risco vermelho, "?"), marca-texto | Planilha/caderno vs. CRM |
| **Diário do caso** | Carimbos "DIA 01 / DIA 30" em fonte mono com som de carimbo, linha do tempo de 3 marcos no topo, card "● DEPOIMENTO REAL" com grão | Case de cliente |
| **Texto atrás da pessoa** | Palavra gigante (Anton/Poppins Black) na parede, cabeça na frente; máscara da pessoa quadro a quadro com `rembg` (`u2net_human_seg`) | Palavra-tese, no máximo 5 por vídeo |
| **Tela real** | Print ou gravação da tela com zoom, cursor clicando, marca-texto | Mostrar recurso específico |

### Peças reutilizáveis
- Diagrama de nós ligados por linhas que se desenham (canal → Beeno → time).
- Lista que acende item a item na palavra; ✓ verde / ✗ vermelho.
- Contadores, barra de meta enchendo, radar ("o lead esfria"), lupa, rede de pontos que acendem.
- O **ponto verde = lead** (cai, vira balões, some em partículas) — motivo-personagem da Beeno.
- Celulares com chat entrando balão a balão; nomes fictícios (Mariana, Ana, Bruno, Carla).
- P&B na dor e a cor voltando na virada.

### Regras de motion
- Cada elemento entra **na palavra que o cita** (tempos do `palavras.json`), nunca antes.
- **Texto de motion nunca repete a legenda**: ou o motion fica só visual (ícone, número, objeto) e a legenda leva a fala, ou a legenda some.
- Texto grande igual à fala (não resumir, não trocar palavra, não deixar pedaço de fora). Exceção: título de bloco dark, que parafraseia em frase curta.
- Nada atrás do rosto nem vazando do elemento.
- Nada de zoom no cenário para "mostrar" um objeto: faça um motion próprio.
- Mudança visual a cada 1,5–2,5 s; entradas com `easeOutCubic` e `easeOutBack` leve.

## 6. Áudio

- **Voz:** limpa com `ferramentas/preparar_bruto.sh` (RNNoise a 85% + passa-alta 90 Hz + presença em 3,5 kHz + compressão leve).
- **Trilha:** só licenciada (Pixabay, com o arquivo de licença salvo) ou enviada pelo time; nunca faixa tirada do YouTube em anúncio pago.
  - ~13–15 dB abaixo da voz em anúncio; 17–20 dB em podcast.
  - Sidechain sob a voz, vale de −3 dB em 2,5 kHz, fade de saída de 1,2 s: `ferramentas/mixar.sh`.
  - Muitas vezes a batida cheia **entra quando termina o gancho** (ou na virada).
  - Pergunte antes de pôr trilha: há quem prefira receber sem música e colocar a própria na revisão.
- **Efeitos:** −14 a −20 dB abaixo da voz, começando 1–2 quadros antes do evento. Mapa: clique na palavra gigante, swoosh no título, obturador no P&B, pop nos chips, whoosh na virada e no logo, impacto grave nos números. Estilo "nada eletrônico, sem estalo". Gerador: `ferramentas/gerar_sfx.py`.
- **Loudness final:** −14 LUFS (Reels) ou −15 LUFS, pico −1 dBTP, loudnorm em duas passadas (`ferramentas/masterizar.sh`, `mixar.sh`).

## 7. CTA

- **Pílula + seta:** pílula verde com texto tinta e a seta encaixada **numa peça só**, entrando e saindo juntas, apontando para o botão do anúncio. A legenda quebra antes do texto da pílula (não mostra a palavra duas vezes). Já existe em `editor/scenes.py` (`cta_full`).
- **Cartela final de 2 s** (quando pedirem): último quadro congelado e desfocado + logo + frase + pílula. A faixa de público sai nesse momento. O estilo dos criativos de referência é sem cartela (ver 1-estilo-beeno, seção 1, item 14).
- CTA de engajamento (orgânico): "Marca aqui o gestor que…".

## 8. Faixa de público e regras da Meta

- **Faixa de público:** linha fina no topo (y≈46, ~32 px), pílula tinta com borda verde e o número do público em verde. Nunca uma caixa grande no meio. Some nos trechos em que o topo está ocupado. Componente: `remotion/_shared/faixa-publico.tsx`.
- **Copy na 3ª pessoa:** "EMPRESAS QUE ATENDEM PELO WHATSAPP", "TIMES COM MAIS DE 5 VENDEDORES". Nunca "se você…" (atributo pessoal).
- Sem logo do WhatsApp ou de outras marcas que não sejam parceiras oficiais (use balão genérico). Blip só como parceiro, com o logo oficial.
- Sem promessa de ganho; sem close que faça dinheiro de cena parecer real.

## 9. Podcast e YouTube

- **Vinheta de abertura (16:9, ~10 s):** logo entra de 112% → 100%; pilares da marca em corte seco a cada ~0,9 s; flash branco na virada com o drop da música; slogan palavra a palavra; cartela e fade.
- **Tarja de nome:** barra vertical verde de 7 px, nome em Poppins 700 ~64 px caixa alta, função em verde; sobe 24 px em 10 quadros, sai em 8; entra quando a pessoa diz o nome.
- **Selo no canto:** cápsula pequena, no lado oposto à luz.
- **Inscreva-se:** card de ~6,5 s com o canal certo (mão clica em INSCREVER-SE → "✓ INSCRITO" → clica no sino, que balança). Duas vezes por episódio: na maior pausa entre 1:30 e 3:30 e na despedida.
- Episódio longo: sem legenda, −14 LUFS, conteúdo original intocado; as camadas com alfa saem do Remotion e são compostas por FFmpeg.
- **Thumbnail 1280×720:** quadro do episódio desfocado e escuro, convidado recortado (rembg, olhos abertos) à direita, frase curta à esquerda, < 2 MB.
- **Cortes 9:16 de podcast:** empurrão lento 100 → 104%, título do tema no meio, tarja de 1–5 s, cartela de ~2 s.
- **Reels de evento:** voz contínua sobre B-roll a cada 1,5–3 s; planos aberto/fechado simulados recortando o 4K com o rosto rastreado (`ferramentas/rastrear_rosto.py`); estabilização (vidstab); cor quente com curva em S; gancho reordenado para a frase mais forte.
