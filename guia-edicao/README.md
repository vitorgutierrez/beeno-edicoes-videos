# Guia de edição dos vídeos da Beeno

Tudo o que já se aprendeu editando vídeos curtos (anúncios, reels, cortes de podcast) organizado para
os vídeos da Beeno: o estilo medido nos criativos de referência da Beeno, um repertório de técnicas de
edição já testadas, o checklist de revisão e o caminho do bruto até a entrega.

## Decisões mais recentes (valem acima do resto)

Feedback dos reels 01 e 02 (v5), que define o tom atual:

- **Edição calma, sóbria, documental.** Ritmo natural, menos zoom, splits mais longos e em menor número.
- Cortes secos em toda pausa acima de ~0,2 s (com a borda ajustada pela energia do áudio, para não comer palavra); começa na primeira palavra e termina logo após a última.
- Enquadramento fixo; troca aberto/fechado só em corte seco no fim de frase, sem zoom animado.
- Troca de cena com uma "assentada" de 4% em 0,2 s + clique de mouse baixo.
- **Nada de transparência em texto:** legendas, títulos, cards e chips sólidos.
- Frase que vira título não se repete na legenda.
- Trilha com a batida cheia entrando quando termina o gancho, com ducking sob a voz.
- Tom de gestor para gestor; o problema é o processo, nunca a pessoa.

Quando um capítulo abaixo sugerir algo mais agitado (flashes, glitch, tipografia tremendo), trate como
opção para um criativo específico e combine antes.

## Capítulos

1. [Estilo Beeno](1-estilo-beeno.md): manual medido nos 11 criativos de referência (ritmo, legenda, cores, logo, motion "Beeno dark", som, B-roll). Análises vídeo a vídeo em [analise-exemplos/](analise-exemplos/).
2. [Técnicas de edição](2-tecnicas.md): ganchos e A/B, famílias de legenda, transições, tela dividida, roupagens de motion, áudio, CTA, faixa de público, podcast/YouTube.
3. [Checklist de revisão](3-revisao.md): o que conferir antes de mandar para aprovação.
4. [Roteiro e copy](4-roteiro-e-copy.md): arco, regras de copy, tom da Beeno.
5. [Pipeline e entrega](5-pipeline-e-entrega.md): do bruto ao arquivo final, formatos e nomes.

Exemplos de plano de edição: [exemplos/](exemplos/).

## Onde está cada ferramenta

| Pasta | Para quê |
|---|---|
| `editor/` | Editor em Python dos reels (versão em uso, v5) |
| `remotion/` | Componentes Remotion do estilo Beeno |
| `motion-html/` | Inserções "Beeno dark" em HTML, renderizadas em MP4/ProRes/WebM |
| `ferramentas/` | Transcrição, corte de pausas, limpeza de voz, mixagem, masterização, efeitos, trilha sintetizada, rastreio de rosto |
| `posts/` | Carrosséis e estáticos |
| `assets/` | Logo e fontes oficiais |
