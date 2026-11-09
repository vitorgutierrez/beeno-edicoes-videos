// Estilo Beeno (guia-edicao/1-estilo-beeno.md): câmera com punch-in por plano, palco desfocado, split com B-roll,
// painéis de cor, flash branco, logo com borrão de movimento, tipografias especiais, blocos "Beeno dark" e a legenda base.
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import {progresso, useT} from './componentes';
import {FONTE, PROJETO, Palavra, normalizar} from './tema';

export const {fontFamily: MONTSERRAT} = loadFont('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']});

// Paleta medida nos criativos (seções 5.2 e 6.1).
export const BEENO = {
  verde: '#00CB88',
  menta: '#60E1B4',
  check: '#15A56B',
  fundo: '#091B15',
  brilho: '#09402D',
  brilhoBlip: '#082E37',
  card: '#0A1E14',
  titulo: '#FAFFFE',
  contexto: '#8CA69E',
  vermelho: '#EC1D1D',
  vermelhoG: '#EF404A',
  amarelo: '#F4C70F',
  azul: '#0090FF',
  painelAmarelo: '#FFE226',
  painelAzul: '#2666FF',
  xVermelho: '#E90002',
};

const QUADRO = 1 / 30;

// ---------- Linha do tempo de cenas ----------

export type TipoCena = 'camera' | 'impacto' | 'palco' | 'split' | 'painel' | 'dark';
export type CenaBeeno = {de: number; tipo: TipoCena; escala?: number; pb?: boolean};

export const cenaEm = (t: number, cenas: CenaBeeno[]) => {
  let atual = cenas[0];
  let inicio = cenas[0].de;
  for (const c of cenas) if (t >= c.de) {
    atual = c;
    inicio = c.de;
  }
  return {...atual, inicio};
};

export type Enquadramento = {s: number; x: number; y: number}; // escala e deslocamento do canto (origem 0,0)

export type ConfigCamera = {
  rosto: {x: number; y: number}; // âncora do punch-in
  split: Enquadramento; // rosto inteiro acima de y ≈ 800
  palco: Enquadramento; // queixo acima de y ≈ 900–1000
  painelX: number; // deslocamento para centrar o rosto na metade esquerda
};

const W = 1080;
const H = 1920;

const punchIn = (s: number, fx: number, fy: number): Enquadramento => ({
  s,
  x: Math.min(0, Math.max(W - W * s, fx - fx * s)),
  y: Math.min(0, Math.max(H - H * s, fy - fy * s)),
});

// Uma única instância do vídeo gravado (áudio contínuo). Cada cena só muda escala, posição, recorte e filtro.
// Troca seca entre cenas: câmera e painéis mudam no mesmo quadro (sem animação, então sempre sincronizados).
export const CameraBeeno: React.FC<{video: string; cenas: CenaBeeno[]; config: ConfigCamera}> = ({video, cenas, config}) => {
  const t = useT();
  const c = cenaEm(t, cenas);
  let e: Enquadramento = punchIn(c.escala ?? 1, config.rosto.x, config.rosto.y);
  let filtro: string | undefined;
  let recorte: string | undefined;
  if (c.tipo === 'split') e = config.split;
  if (c.tipo === 'palco') {
    e = config.palco;
    // rampa de desfoque de 3 quadros na entrada
    filtro = `blur(${Math.min(32, ((t - c.inicio) / (3 * QUADRO)) * 32)}px) brightness(.82) saturate(1.1)`;
  }
  if (c.tipo === 'painel') {
    e = {s: 1, x: config.painelX, y: 0};
    recorte = 'inset(0 50% 0 0)';
  }
  if (c.pb) filtro = 'grayscale(1) contrast(1.12)';
  return (
    <AbsoluteFill style={{background: '#000', clipPath: recorte}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: `translate(${e.x}px, ${e.y}px) scale(${e.s})`}}>
        {/* O áudio do celular é mono; ao virar estéreo o Remotion perde 3 dB. +3 dB devolve o volume original. */}
        <OffthreadVideo src={staticFile(`${PROJETO}/video/${video}`)} volume={1.4125} style={{width: W, height: H, filter: filtro}} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- Split com B-roll (câmera em cima, B-roll embaixo, emenda em degradê) ----------

export const SplitBroll: React.FC<{arquivo: string; de: number; ate: number; desloc?: number; escala?: number}> = ({arquivo, de, ate, desloc = 300, escala = 1}) => {
  const t = useT();
  const {fps} = useVideoConfig();
  if (t < de - 1 || t > ate) return null;
  return (
    <Sequence from={Math.round(de * fps)} durationInFrames={Math.max(1, Math.round((ate - de) * fps))} premountFor={fps}>
      {/* a parte de baixo da câmera escurece até a emenda */}
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, transparent 760px, rgba(0,0,0,.85) 960px, #000 1100px)'}} />
      <AbsoluteFill style={{WebkitMaskImage: 'linear-gradient(to bottom, transparent 860px, #000 1040px)', maskImage: 'linear-gradient(to bottom, transparent 860px, #000 1040px)'}}>
        <div style={{position: 'absolute', left: 0, top: desloc, width: W, height: H * escala, overflow: 'hidden'}}>
          <OffthreadVideo muted src={staticFile(`${PROJETO}/hf/${arquivo}`)} style={{width: W * escala, height: H * escala, objectFit: 'cover', marginLeft: (W - W * escala) / 2}} />
        </div>
      </AbsoluteFill>
    </Sequence>
  );
};

// ---------- Split-painel (câmera à esquerda, painéis de cor sólida à direita) ----------

export const PaineisCor: React.FC<{de: number; ate: number; itens: {texto: string; t: number; fundo: string; cor: string}[]}> = ({de, ate, itens}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  const visiveis = itens.filter((i) => t >= i.t);
  return (
    <div style={{position: 'absolute', left: W / 2, top: 0, width: W / 2, height: H, display: 'flex', flexDirection: 'column'}}>
      {visiveis.map((i) => {
        const p = Math.min(1, (t - i.t) / (4 * QUADRO));
        return (
          <div
            key={i.texto}
            style={{
              flex: 1, background: i.fundo, display: 'flex', alignItems: 'center', justifyContent: 'center',
              transform: `translateX(${(1 - p) * 100}%)`, fontFamily: MONTSERRAT, fontWeight: 800, fontSize: 64, color: i.cor, letterSpacing: -1,
            }}
          >
            {i.texto}
          </div>
        );
      })}
    </div>
  );
};

// ---------- Flash branco com rampa de desfoque (assinatura das viradas) ----------

export const FlashBranco: React.FC<{t0: number; quente?: boolean}> = ({t0, quente}) => {
  const t = useT();
  const q = (t - t0) / QUADRO; // em quadros, 0 = quadro da troca
  if (q < -2 || q > 5) return null;
  // q -2..0: desfoque e brilho subindo no plano que sai; q 0..1: branco puro; q 1..5: branco decai sobre o plano novo
  const branco = q < 0 ? 0.35 * (q + 2) : q < 1.5 ? 1 : Math.max(0, 0.85 * (1 - (q - 1.5) / 3.5));
  const desfoque = q < 0 ? 10 * (q + 2) : 0;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {desfoque > 0 ? <AbsoluteFill style={{backdropFilter: `blur(${desfoque}px) brightness(${1 + desfoque / 10})`}} /> : null}
      <AbsoluteFill style={{background: '#FFFFFF', opacity: branco}} />
      {quente && q >= 1 ? <AbsoluteFill style={{background: '#FFD27A', opacity: Math.max(0, 0.4 * (1 - (q - 1) / 4)), mixBlendMode: 'screen'}} /> : null}
    </AbsoluteFill>
  );
};

// ---------- Logo Beeno (uma vez, grande, abaixo do queixo) ----------

export const LogoEntrada: React.FC<{de: number; ate: number; y: number; variante: 'zoom' | 'whip'}> = ({de, ate, y, variante}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  const largura = 680;
  const altura = (largura * 1105) / 2937;
  const k = Math.min(1, (t - de) / (8 * QUADRO));
  const ease = 1 - Math.pow(1 - k, 4);
  const img = (estilo: React.CSSProperties, key?: number) => (
    <Img key={key} src={staticFile(`${PROJETO}/hf/logo_beeno_lockup_escuro.png`)} style={{position: 'absolute', left: (W - largura) / 2, top: y - altura / 2, width: largura, height: altura, ...estilo}} />
  );
  if (variante === 'zoom') {
    const s = 3 - 2 * ease;
    return <AbsoluteFill>{img({transform: `scale(${s})`, filter: `blur(${(1 - ease) * 14}px)`, opacity: Math.min(1, k * 3)})}</AbsoluteFill>;
  }
  // whip horizontal com borrão direcional (cópias com opacidade decrescente)
  const x = -1.2 * W * (1 - ease);
  const rastro = (1 - ease) * 140;
  return (
    <AbsoluteFill>
      {k < 1 ? [1, 2, 3, 4, 5].map((i) => img({transform: `translateX(${x - (rastro * i) / 5}px)`, opacity: 0.18 * (1 - i / 6)}, i)) : null}
      {img({transform: `translateX(${x}px)`})}
    </AbsoluteFill>
  );
};

// ---------- Tipografias especiais (sobre o palco, abaixo do queixo) ----------

export type PalavraEspecial = {w: string; t: number; cor?: string; grande?: boolean; quebra?: boolean};

// Linha-chave grande: Montserrat ExtraBold ~100 px; a palavra-chave em caixa alta ~125 px colorida. Acumula palavra a palavra.
export const LinhaChave: React.FC<{de: number; ate: number; y: number; contexto?: {texto: string; t: number}; palavras: PalavraEspecial[]}> = ({
  de, ate, y, contexto, palavras,
}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: y, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
      {contexto && t >= contexto.t ? (
        <div style={{fontFamily: MONTSERRAT, fontWeight: 700, fontSize: 60, color: '#FFFFFF', textShadow: '3px 4px 6px rgba(0,0,0,.45)'}}>{contexto.texto}</div>
      ) : null}
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'baseline', columnGap: 24, rowGap: 0}}>
        {palavras.map((p, i) => (
          <React.Fragment key={i}>
            {p.quebra ? <div style={{flexBasis: '100%', height: 0}} /> : null}
            <span
              style={{
                fontFamily: MONTSERRAT, fontWeight: 800, fontSize: p.grande ? 128 : 100, lineHeight: 1.1, letterSpacing: -2,
                color: p.cor ?? '#FFFFFF', textTransform: p.grande ? 'uppercase' : undefined, opacity: t >= p.t ? 1 : 0,
                textShadow: '3px 5px 10px rgba(0,0,0,.45)',
              }}
            >
              {p.w}
            </span>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

// Lista de dores: ✗ vermelho em disco + texto branco, um item por palavra falada (com pop).
export const ListaX: React.FC<{de: number; ate: number; y: number; titulo?: {texto: string; t: number}; itens: {texto: string; t: number}[]}> = ({
  de, ate, y, titulo, itens,
}) => {
  const t = useT();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (t < de || t >= ate) return null;
  return (
    <div style={{position: 'absolute', left: 230, top: y, display: 'flex', flexDirection: 'column', gap: 26}}>
      {titulo && t >= titulo.t ? (
        <div style={{fontFamily: MONTSERRAT, fontWeight: 700, fontSize: 58, color: '#FFFFFF', textShadow: '3px 4px 6px rgba(0,0,0,.45)', marginBottom: 6}}>{titulo.texto}</div>
      ) : null}
      {itens.map((it) => {
        if (t < it.t) return null;
        const m = spring({frame: frame - it.t * fps, fps, config: {damping: 12, stiffness: 260}});
        return (
          <div key={it.texto} style={{display: 'flex', alignItems: 'center', gap: 28, transform: `scale(${0.7 + 0.3 * m})`, transformOrigin: 'left center'}}>
            <div style={{width: 84, height: 84, borderRadius: 42, background: BEENO.vermelhoG, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONTSERRAT, fontWeight: 900, fontSize: 52, boxShadow: '0 8px 20px rgba(0,0,0,.35)'}}>
              ✕
            </div>
            <div style={{fontFamily: MONTSERRAT, fontWeight: 800, fontSize: 78, color: '#FFFFFF', letterSpacing: -1, textShadow: '3px 5px 10px rgba(0,0,0,.45)'}}>{it.texto}</div>
          </div>
        );
      })}
    </div>
  );
};

// X desenhado em dois traços sobre uma frase em caixa alta (som de rabisco no mesmo tempo).
export const XDesenhado: React.FC<{de: number; ate: number; y: number; linhas: {texto: string; t: number}[]; tX: number}> = ({de, ate, y, linhas, tX}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  const a = Math.min(1, Math.max(0, (t - tX) / 0.2));
  const b = Math.min(1, Math.max(0, (t - tX - 0.2) / 0.15));
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center'}}>
      <div style={{position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '10px 30px'}}>
        {linhas.map((l) => (
          <div key={l.texto} style={{fontFamily: MONTSERRAT, fontWeight: 900, fontSize: 104, lineHeight: 1.05, color: '#FFFFFF', letterSpacing: -2, textShadow: '3px 5px 10px rgba(0,0,0,.45)', opacity: t >= l.t ? 1 : 0}}>
            {l.texto}
          </div>
        ))}
        {/* o X passa da altura do texto para não ficar achatado sobre uma frase larga */}
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={{position: 'absolute', left: '8%', width: '84%', top: '-45%', height: '190%', overflow: 'visible'}}>
          <line x1="4" y1="8" x2={4 + 92 * a} y2={8 + 84 * a} stroke={BEENO.xVermelho} strokeWidth="7" strokeLinecap="round" vectorEffect="non-scaling-stroke" style={{strokeWidth: 22}} opacity={a > 0 ? 1 : 0} />
          <line x1="96" y1="8" x2={96 - 92 * b} y2={8 + 84 * b} stroke={BEENO.xVermelho} strokeWidth="7" strokeLinecap="round" vectorEffect="non-scaling-stroke" style={{strokeWidth: 22}} opacity={b > 0 ? 1 : 0} />
        </svg>
      </div>
    </div>
  );
};

// ---------- Beeno dark (motion de produto) ----------

export const FundoDark: React.FC<{brilho?: 'verde' | 'blip'}> = ({brilho = 'verde'}) => {
  const cor = brilho === 'blip' ? BEENO.brilhoBlip : BEENO.brilho;
  return (
    <AbsoluteFill style={{background: BEENO.fundo}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse 80% 55% at 50% 40%, ${cor} 0%, transparent 70%)`}} />
      <AbsoluteFill
        style={{
          backgroundImage: 'linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />
      <div style={{position: 'absolute', left: -160, top: 80, width: 520, height: 520, borderRadius: '50%', background: cor, filter: 'blur(120px)', opacity: 0.7}} />
      <div style={{position: 'absolute', right: -200, bottom: 160, width: 600, height: 600, borderRadius: '50%', background: cor, filter: 'blur(140px)', opacity: 0.6}} />
    </AbsoluteFill>
  );
};

// Bloco dark: fundo + cena; cada cena começa com ~6 quadros de fundo vazio (o conteúdo usa t0 = de + 0.2).
export const BlocoDark: React.FC<{de: number; ate: number; brilho?: 'verde' | 'blip'; children: React.ReactNode}> = ({de, ate, brilho, children}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  return (
    <AbsoluteFill>
      <FundoDark brilho={brilho} />
      {children}
    </AbsoluteFill>
  );
};

// Entrada padrão do motion: fade + subida de 24 px em 8 quadros.
export const useEntradaDark = (t0: number) => {
  const t = useT();
  const p = Math.min(1, Math.max(0, (t - t0) / (8 * QUADRO)));
  const e = 1 - Math.pow(1 - p, 3);
  return {opacity: e, transform: `translateY(${(1 - e) * 24}px)`, visivel: t >= t0};
};

export const CardVidro: React.FC<{t0: number; x: number; y: number; w: number; h: number; children: React.ReactNode}> = ({t0, x, y, w, h, children}) => {
  const e = useEntradaDark(t0);
  if (!e.visivel) return null;
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 16, overflow: 'hidden', background: BEENO.card,
        border: '1px solid rgba(0,203,136,.45)', boxShadow: '0 0 40px rgba(0,203,136,.12), 0 30px 60px rgba(0,0,0,.45)',
        opacity: e.opacity, transform: e.transform,
      }}
    >
      {children}
    </div>
  );
};

export type TrechoTitulo = {w: string; t: number; cor?: string};

// Texto do motion em 3 níveis (Poppins): contexto cinza-verde 44 px + título branco Bold 84 px com a palavra de destaque colorida.
// O título pode trocar: cada item de `titulos` substitui o anterior a partir do seu primeiro trecho.
export const TituloDark: React.FC<{y: number; contexto?: {texto: string; t: number; destaque?: {w: string; cor: string}}; titulos: TrechoTitulo[][]}> = ({
  y, contexto, titulos,
}) => {
  const t = useT();
  const atual = [...titulos].reverse().find((linha) => t >= linha[0].t);
  const ctx = useEntradaDark(contexto?.t ?? 1e9);
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: y, fontFamily: FONTE}}>
      {contexto && ctx.visivel ? (
        <div style={{fontWeight: 500, fontSize: 44, color: BEENO.contexto, opacity: ctx.opacity, transform: ctx.transform, marginBottom: 10}}>
          {contexto.destaque ? contexto.texto.split(contexto.destaque.w).flatMap((parte, i, arr) => (i < arr.length - 1 ? [parte, <span key={i} style={{color: contexto.destaque!.cor}}>{contexto.destaque!.w}</span>] : [parte])) : contexto.texto}
        </div>
      ) : null}
      {atual ? (
        <div style={{fontWeight: 700, fontSize: 84, lineHeight: 1.12, color: BEENO.titulo, letterSpacing: -1.5}}>
          {atual.map((p, i) => (
            <TrechoAnimado key={`${atual[0].t}-${i}`} trecho={p} />
          ))}
        </div>
      ) : null}
    </div>
  );
};

const TrechoAnimado: React.FC<{trecho: TrechoTitulo}> = ({trecho}) => {
  const e = useEntradaDark(trecho.t);
  return <span style={{color: trecho.cor ?? BEENO.titulo, opacity: e.opacity, display: 'inline-block', transform: e.transform, marginRight: 22}}>{trecho.w}</span>;
};

export const ListaCheck: React.FC<{x: number; y: number; itens: {texto: string; t: number; ok?: boolean}[]}> = ({x, y, itens}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', flexDirection: 'column', gap: 18}}>
    {itens.map((it) => (
      <ItemCheck key={it.texto} {...it} />
    ))}
  </div>
);

const ItemCheck: React.FC<{texto: string; t: number; ok?: boolean}> = ({texto, t, ok = true}) => {
  const e = useEntradaDark(t);
  if (!e.visivel) return null;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 20, opacity: e.opacity, transform: e.transform, fontFamily: FONTE, fontWeight: 600, fontSize: 48, color: BEENO.titulo}}>
      <span style={{width: 52, height: 52, borderRadius: 26, background: ok ? BEENO.check : BEENO.vermelhoG, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 30, fontWeight: 800}}>
        {ok ? '✓' : '✕'}
      </span>
      {texto}
    </div>
  );
};

// ---------- Legenda base (seção 5.1) ----------

type PaginaLegenda = {palavras: Palavra[]; de: number; ate: number};

export type ConfigLegenda = {
  palavras: Palavra[];
  // Palavras coloridas: início exato da palavra (do palavras.json) → cor.
  cores: {t: number; cor: string}[];
  // Palavras em CAIXA ALTA 1,3× (ênfase dentro da legenda).
  caixaAlta?: number[];
  // Trocas de plano: a página zera em cada uma.
  quebras: number[];
  // Posição do bloco por tipo de cena: y do topo (centralizado na tela) ou {y, x, largura}; null = some.
  yPorCena: (t: number) => number | {y: number; x: number; largura: number} | null;
  // Cenas em P&B: legenda inteira amarela.
  amarelaEm?: (t: number) => boolean;
};

const NOMES_PROPRIOS = new Set(['beeno', 'blip', 'crm', 'whatsapp']);
const MAX_CARACTERES_PAGINA = 54; // ~3 linhas de ~18–22 caracteres

const montarPaginas = (palavras: Palavra[], quebras: number[]): PaginaLegenda[] => {
  const juntas: Palavra[] = [];
  for (const p of palavras) {
    const w = p.w.trim();
    if (/^[-–]/.test(w) && juntas.length) {
      const ult = juntas[juntas.length - 1];
      juntas[juntas.length - 1] = {...ult, w: ult.w + w, e: p.e};
    } else juntas.push({...p, w});
  }
  const paginas: Palavra[][] = [];
  let atual: Palavra[] = [];
  const fecha = () => {
    if (atual.length) paginas.push(atual);
    atual = [];
  };
  for (const p of juntas) {
    const tamanho = atual.reduce((n, x) => n + x.w.length + 1, 0) + p.w.length;
    const corte = atual.length > 0 && quebras.some((q) => q > atual[atual.length - 1].s + 0.01 && q <= p.s + 0.06);
    if (atual.length && (tamanho > MAX_CARACTERES_PAGINA || corte)) fecha();
    atual.push(p);
    if (/[.,?!]$/.test(p.w)) fecha();
  }
  fecha();
  return paginas.map((pg, i) => ({palavras: pg, de: pg[0].s, ate: Math.min(paginas[i + 1]?.[0].s ?? Infinity, pg[pg.length - 1].e + 0.5)}));
};

export const LegendaBeeno: React.FC<{config: ConfigLegenda}> = ({config}) => {
  const t = useT();
  const paginas = React.useMemo(() => montarPaginas(config.palavras, config.quebras), [config.palavras, config.quebras]);
  const pg = paginas.find((p) => t >= p.de - 1 * QUADRO && t < p.ate);
  const pos = config.yPorCena(t);
  if (!pg || pos === null) return null;
  const area = typeof pos === 'number' ? {y: pos, x: (W - 860) / 2, largura: 860} : pos;
  const amarela = config.amarelaEm?.(t) ?? false;
  const primeira = config.palavras[0].s;
  return (
    <div style={{position: 'absolute', left: area.x, width: area.largura, top: area.y, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'baseline', columnGap: 18}}>
      {pg.palavras.map((p) => {
        const base = p.w.replace(/\.$/, '');
        const n = normalizar(base);
        const caixa = config.caixaAlta?.some((c) => Math.abs(c - p.s) < 0.01);
        let texto = NOMES_PROPRIOS.has(n) ? base.replace(/^\p{L}/u, (c) => c.toUpperCase()) : base.toLowerCase();
        if (n === 'crm') texto = base.replace(/crm/i, 'CRM');
        if (n === 'whatsapp') texto = base.replace(/whatsapp/i, 'WhatsApp');
        if (Math.abs(p.s - primeira) < 0.01) texto = texto.replace(/^\p{L}/u, (c) => c.toUpperCase());
        if (caixa) texto = texto.toUpperCase();
        const cor = config.cores.find((c) => Math.abs(c.t - p.s) < 0.01)?.cor ?? (amarela ? BEENO.amarelo : '#FFFFFF');
        return (
          <span
            key={p.s}
            style={{
              fontFamily: MONTSERRAT, fontWeight: 700, fontSize: caixa ? 94 : 72, lineHeight: 1.3, color: cor,
              textShadow: '3px 4px 6px rgba(0,0,0,.45)', opacity: t >= p.s - 1 * QUADRO ? 1 : 0,
            }}
          >
            {texto}
          </span>
        );
      })}
    </div>
  );
};

