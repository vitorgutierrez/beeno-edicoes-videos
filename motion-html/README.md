# Motion da Beeno em HTML

Inserções "Beeno dark" (fundo verde quase preto, cards de vidro, Poppins) feitas em HTML/CSS/JS e
renderizadas quadro a quadro com o Chrome em modo headless. Cada elemento é cronometrado na palavra
falada (constantes `T_*` no começo de cada `anim-beeno-0X.html`).

| Arquivo | Assunto | Duração |
|---|---|---|
| `anim-beeno-01.html` | O lead some (ponto verde que vira balões e se desfaz) | 10,4 s |
| `anim-beeno-02.html` | Do canal (Blip) ao pipeline | 27,5 s |
| `anim-beeno-03.html` | O número que não veio | 16,0 s |
| `anim-beeno-04.html` | CRM nativo do Blip | 13,8 s |
| `anim-beeno-05.html` | Volume de conversa sem venda | 15,5 s |
| `anim-beeno-06.html` | A conversa que vira venda | 25,6 s |

## Como renderizar

Precisa de Node 22+, Google Chrome e FFmpeg.

```bash
cd motion-html
bash build-beeno-01.sh            # gera os 3 arquivos em motion-html/saida/
OUT=/outra/pasta bash build-beeno-01.sh
```

Cada build gera três entregáveis, a 60 fps:

- `<slug>-1080x1920-fundo-escuro.mp4`: H.264 CRF 17, para usar em tela cheia;
- `<slug>-1080x1920-alpha-prores4444.mov`: com transparência, para pôr por cima da câmera no CapCut;
- `<slug>-1080x1920-alpha.webm`: VP9 com transparência (mais leve).

Para conferir alguns quadros antes de renderizar tudo: `node preview-beeno-02.js 1.5 8 20` (tempos em segundos).

Os scripts procuram o Chrome em `C:/Program Files/Google/Chrome/Application/chrome.exe`. Em outro
sistema, troque a constante `CHROME` no topo de `render-beeno-0X.js` e `preview-beeno-*.js`.

## Para fazer uma animação nova

1. Copie a mais parecida (`anim-beeno-0X.html` + `render-beeno-0X.js` + `build-beeno-0X.sh`).
2. Ajuste os tempos `T_*` pelo `palavras.json` da fala (cada elemento entra na palavra que o cita).
3. Troque o nome do HTML em `render-beeno-0X.js` e o `BASE` no `build`.
4. Confira com o `preview` e só depois rode o build completo.

Regras: veja [guia-edicao/1-estilo-beeno.md](../guia-edicao/1-estilo-beeno.md), seção 8 (Beeno dark), e
[guia-edicao/2-tecnicas.md](../guia-edicao/2-tecnicas.md).
