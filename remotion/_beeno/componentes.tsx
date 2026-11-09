import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  SynchronizedVerticalCamera,
  SynchronizedVerticalPanel,
  SynchronizedVerticalSplitConfig,
  getSynchronizedVerticalSplitState,
} from '../../_shared/synchronized-split';
import {COR, FONTE, Palavra, PROJETO, clamp, normalizar, suave} from './tema';

// Tempo absoluto em segundos. Nada aqui fica dentro de <Sequence>, então o quadro é o da composição.
export const useT = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return frame / fps;
};

export const progresso = (t: number, inicio: number, duracao = 0.5) =>
  interpolate(t, [inicio, inicio + duracao], [0, 1], {...clamp, easing: suave});

// Opacidade de uma janela [de, ate] com entrada e saída curtas.
export const janela = (t: number, de: number, ate: number, fade = 0.3) =>
  Math.min(progresso(t, de, fade), 1 - progresso(t, ate - fade, fade));

const useMola = (inicio: number) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - inicio * fps, fps, config: {damping: 15, stiffness: 170}});
};

// ---------- Câmera + painel (tela dividida vertical sincronizada) ----------

export type Janela = {de: number; ate: number};
export const TRANSICAO = 0.9;

export const progressoSplit = (t: number, janelas: Janela[]) =>
  Math.max(
    0,
    ...janelas.map((j) => Math.min(progresso(t, j.de, TRANSICAO), 1 - progresso(t, j.ate - TRANSICAO, TRANSICAO))),
  );

// Chaves [segundo, zoom] interpoladas com curva suave.
export const zoomEm = (t: number, chaves: [number, number][]) => {
  if (t <= chaves[0][0]) return chaves[0][1];
  for (let i = 1; i < chaves.length; i++) {
    const [tp, zp] = chaves[i - 1];
    const [ti, zi] = chaves[i];
    if (t < ti) return interpolate(t, [tp, ti], [zp, zi], {...clamp, easing: suave});
  }
  return chaves[chaves.length - 1][1];
};

// Plano da câmera em degraus (corte seco): [segundo, zoom]. Simula a troca entre plano aberto e fechado.
export const planoEm = (t: number, planos: [number, number][]) => {
  let z = 1;
  for (const [ti, zi] of planos) if (t >= ti) z = zi;
  return z;
};

// Tremida curta depois de cada impacto (em px).
export const tremidaEm = (t: number, tremores: number[], forca = 22) => {
  let dx = 0;
  let dy = 0;
  for (const t0 of tremores) {
    const k = t - t0;
    if (k < 0 || k > 0.4) continue;
    const a = forca * (1 - k / 0.4) ** 2;
    dx += Math.sin(k * 95) * a;
    dy += Math.cos(k * 77) * a * 0.7;
  }
  return {dx, dy};
};

export const CameraEPainel: React.FC<{
  video: string;
  config: SynchronizedVerticalSplitConfig;
  splits: Janela[];
  zoom: [number, number][];
  planos?: [number, number][];
  // Trechos em preto e branco (o "problema"); a cor volta na solução.
  pb?: Janela[];
  tremores?: number[];
  painel: React.ReactNode;
}> = ({video, config, splits, zoom, planos = [], pb = [], tremores = [], painel}) => {
  const t = useT();
  const state = getSynchronizedVerticalSplitState(progressoSplit(t, splits), {...config, fullZoom: zoomEm(t, zoom) * planoEm(t, planos)});
  const cinza = Math.max(0, ...pb.map((j) => Math.min(progresso(t, j.de - 0.05, 0.12), 1 - progresso(t, j.ate - 0.05, 0.12))));
  const {dx, dy} = tremidaEm(t, tremores);
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${COR.menta} 0%, ${COR.menta2} 100%)`, transform: `translate(${dx}px, ${dy}px) scale(${dx || dy ? 1.04 : 1})`}}>
      <SynchronizedVerticalPanel state={state}>{painel}</SynchronizedVerticalPanel>
      <SynchronizedVerticalCamera state={state}>
        {/* O áudio do celular é mono; ao virar estéreo o Remotion perde 3 dB. +3 dB devolve o volume original. */}
        <OffthreadVideo
          src={staticFile(`${PROJETO}/video/${video}`)}
          volume={1.4125}
          style={{width: 1080, height: 1920, filter: cinza > 0 ? `grayscale(${cinza}) contrast(${1 + 0.18 * cinza}) brightness(${1 - 0.06 * cinza})` : undefined}}
        />
      </SynchronizedVerticalCamera>
    </AbsoluteFill>
  );
};

// ---------- Legendas palavra por palavra ----------

type Bloco = {palavras: Palavra[]; de: number; ate: number};

const montarBlocos = (palavras: Palavra[]): Bloco[] => {
  // "segunda" + "-feira," viram uma palavra só.
  const juntas: Palavra[] = [];
  for (const p of palavras) {
    const w = p.w.trim();
    if (/^[-–]/.test(w) && juntas.length) {
      const ult = juntas[juntas.length - 1];
      juntas[juntas.length - 1] = {...ult, w: ult.w + w, e: p.e};
    } else juntas.push({...p, w});
  }
  const blocos: Palavra[][] = [];
  let atual: Palavra[] = [];
  for (const p of juntas) {
    const chars = atual.reduce((n, x) => n + x.w.length + 1, 0) + p.w.length;
    const pausa = atual.length > 0 && p.s - atual[atual.length - 1].e > 0.45;
    if (atual.length && (atual.length >= 3 || chars > 17 || pausa)) {
      blocos.push(atual);
      atual = [];
    }
    atual.push(p);
    if (/[.,?!]$/.test(p.w)) {
      blocos.push(atual);
      atual = [];
    }
  }
  if (atual.length) blocos.push(atual);
  return blocos.map((b, i) => ({
    palavras: b,
    de: b[0].s,
    ate: Math.min(blocos[i + 1]?.[0].s ?? Infinity, b[b.length - 1].e + 0.6),
  }));
};

export const Legendas: React.FC<{palavras: Palavra[]; chaves: string[]; top?: number; ocultar?: Janela[]}> = ({
  palavras, chaves, top = 1400, ocultar = [],
}) => {
  const t = useT();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const blocos = React.useMemo(() => montarBlocos(palavras), [palavras]);
  const set = React.useMemo(() => new Set(chaves.map(normalizar)), [chaves]);
  const bloco = blocos.find((b) => t >= b.de && t < b.ate);
  if (!bloco || ocultar.some((j) => t >= j.de && t < j.ate)) return null;
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top, display: 'flex', justifyContent: 'center'}}>
      <div
        style={{
          display: 'flex', flexWrap: 'nowrap', gap: 16, fontFamily: FONTE, fontWeight: 800, fontSize: 64, lineHeight: 1.15,
          textTransform: 'uppercase', letterSpacing: -0.5,
        }}
      >
        {bloco.palavras.map((p) => {
          const pop = spring({frame: frame - p.s * fps, fps, config: {damping: 14, stiffness: 200}});
          const dita = t >= p.s;
          const chave = set.has(normalizar(p.w));
          return (
            <span
              key={p.s}
              style={{
                display: 'inline-block', color: chave ? COR.amarelo : COR.branco,
                opacity: dita ? 1 : 0, transform: `scale(${dita ? 0.75 + 0.25 * pop : 0.75})`,
                WebkitTextStroke: '2px rgba(0,0,0,.85)', paintOrder: 'stroke fill',
                textShadow: '0 6px 18px rgba(0,0,0,.7), 0 2px 3px rgba(0,0,0,.9)',
              }}
            >
              {p.w.replace(/[.,;:]$/, '')}
            </span>
          );
        })}
      </div>
    </div>
  );
};

// ---------- Tipografia no topo, palavra por palavra ----------

export type ItemTopo = {w: string; t: number; destaque?: boolean; riscarEm?: number; quebra?: boolean};

export const TopoPalavras: React.FC<{itens: ItemTopo[]; ate: number; top?: number; tamanho?: number; cor?: string}> = ({
  itens, ate, top = 240, tamanho = 70, cor = COR.branco,
}) => {
  const t = useT();
  const sai = 1 - progresso(t, ate - 0.3, 0.3);
  if (t < itens[0].t || sai <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute', left: 60, right: 60, top, display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
        columnGap: 20, rowGap: 6, fontFamily: FONTE, fontWeight: 800, fontSize: tamanho, lineHeight: 1.12,
        letterSpacing: -1, opacity: sai, padding: '14px 10px', borderRadius: 32,
        background: cor === COR.branco ? 'radial-gradient(ellipse at center, rgba(0,0,0,.38) 0%, rgba(0,0,0,.18) 60%, transparent 85%)' : undefined,
      }}
    >
      {itens.map((it, i) => {
        const p = progresso(t, it.t, 0.35);
        const risco = it.riscarEm !== undefined ? progresso(t, it.riscarEm, 0.35) : 0;
        return (
          <React.Fragment key={i}>
            {it.quebra ? <div style={{flexBasis: '100%', height: 0}} /> : null}
            <span
              style={{
                position: 'relative', display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 26}px)`,
                color: it.destaque ? COR.tinta : cor,
                background: it.destaque ? COR.verde : 'transparent', borderRadius: 14, padding: it.destaque ? '0 14px' : 0,
                textShadow: it.destaque ? 'none' : '0 4px 18px rgba(0,0,0,.55)',
              }}
            >
              {it.w}
              {risco > 0 ? (
                <span
                  style={{
                    position: 'absolute', left: -6, top: '52%', height: 9, width: `calc(${risco * 100}% + 12px)`,
                    background: COR.vermelho, borderRadius: 5, transform: 'rotate(-3deg)',
                  }}
                />
              ) : null}
            </span>
          </React.Fragment>
        );
      })}
    </div>
  );
};

// ---------- Chip ----------

export const Chip: React.FC<{
  t0: number; ate: number; texto: React.ReactNode; top: number; left?: number;
  cor?: string; fundo?: string; tamanho?: number; tremer?: boolean; centro?: boolean;
}> = ({t0, ate, texto, top, left, cor = COR.tinta, fundo = COR.branco, tamanho = 46, tremer, centro}) => {
  const t = useT();
  const mola = useMola(t0);
  const o = janela(t, t0, ate, 0.25);
  if (o <= 0) return null;
  const dx = tremer ? Math.sin((t - t0) * 40) * 7 * Math.max(0, 1 - (t - t0) / 0.7) : 0;
  return (
    <div
      style={{
        position: 'absolute', top, left: centro ? 0 : left, right: centro ? 0 : undefined,
        display: 'flex', justifyContent: 'center', opacity: o,
        transform: `translateX(${dx}px) scale(${0.6 + 0.4 * mola})`, transformOrigin: 'center',
      }}
    >
      <div
        style={{
          background: fundo, color: cor, fontFamily: FONTE, fontWeight: 700, fontSize: tamanho, padding: '14px 30px',
          borderRadius: 999, boxShadow: '0 14px 40px rgba(0,0,0,.25)', whiteSpace: 'nowrap', letterSpacing: -0.5,
        }}
      >
        {texto}
      </div>
    </div>
  );
};

// ---------- B-roll em tela cheia ----------

export const Broll: React.FC<{
  arquivo: string; de: number; ate: number; escala?: number; origem?: string;
}> = ({arquivo, de, ate, escala = 1, origem = '50% 50%'}) => {
  const t = useT();
  const {fps} = useVideoConfig();
  // Entra com cortina de baixo para cima e sai com fade curto.
  const cortina = progresso(t, de, 0.45);
  const sai = 1 - progresso(t, ate - 0.35, 0.35);
  const durFrames = Math.round((ate - de) * fps);
  return (
    <Sequence from={Math.round(de * fps)} durationInFrames={durFrames} premountFor={fps}>
      <AbsoluteFill style={{clipPath: `inset(${(1 - cortina) * 100}% 0 0 0)`, opacity: sai, background: '#000'}}>
        <AbsoluteFill style={{transform: `scale(${escala})`, transformOrigin: origem}}>
          <OffthreadVideo muted src={staticFile(`${PROJETO}/hf/${arquivo}`)} style={{width: 1080, height: 1920, objectFit: 'cover'}} />
        </AbsoluteFill>
        <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.25) 0%, transparent 25%, transparent 65%, rgba(0,0,0,.35) 100%)'}} />
      </AbsoluteFill>
    </Sequence>
  );
};

// ---------- Print com zoom guiado, marca-texto e contornos ----------

export type Regiao = {x: number; y: number; w: number; h: number};
export type Vista = Regiao & {t: number};

export const PrintZoom: React.FC<{
  arquivo: string; iw: number; ih: number; largura: number; altura: number;
  vistas: Vista[]; marcas?: (Regiao & {t: number})[]; contornos?: (Regiao & {t: number; ate?: number; rotulo?: string})[];
  // Áreas com dados reais (telefone, e-mail) que ficam desfocadas.
  ocultar?: Regiao[];
  children?: (escala: number) => React.ReactNode;
}> = ({arquivo, iw, ih, largura, altura, vistas, marcas = [], contornos = [], ocultar = [], children}) => {
  const t = useT();
  let v: Regiao = vistas[0];
  for (const k of vistas.slice(1)) {
    const p = progresso(t, k.t, 0.8);
    v = {x: v.x + (k.x - v.x) * p, y: v.y + (k.y - v.y) * p, w: v.w + (k.w - v.w) * p, h: v.h + (k.h - v.h) * p};
  }
  const escala = Math.min(largura / v.w, altura / v.h);
  const tx = largura / 2 - (v.x + v.w / 2) * escala;
  const ty = altura / 2 - (v.y + v.h / 2) * escala;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: largura, height: altura, overflow: 'hidden', background: COR.branco}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: iw, height: ih, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${escala})`}}>
        <Img src={staticFile(`${PROJETO}/prints/${arquivo}`)} style={{width: iw, height: ih, display: 'block'}} />
        {ocultar.map((o, i) => (
          <div key={`o${i}`} style={{position: 'absolute', left: o.x, top: o.y, width: o.w, height: o.h, backdropFilter: 'blur(7px)', background: 'rgba(235,238,236,.55)', borderRadius: 4}} />
        ))}
        {marcas.map((m, i) => {
          const p = progresso(t, m.t, 0.5);
          return p > 0 ? (
            <div key={i} style={{position: 'absolute', left: m.x, top: m.y, width: m.w * p, height: m.h, background: COR.marca, mixBlendMode: 'multiply', borderRadius: 3}} />
          ) : null;
        })}
        {contornos.map((c, i) => {
          const o = janela(t, c.t, c.ate ?? 1e9, 0.3);
          return o > 0 ? (
            <div
              key={i}
              style={{
                position: 'absolute', left: c.x, top: c.y, width: c.w, height: c.h, opacity: o,
                border: `${5 / escala}px solid ${COR.verde}`, borderRadius: 10 / escala,
                boxShadow: `0 0 0 ${7 / escala}px rgba(0,203,136,.18)`,
              }}
            >
              {c.rotulo ? (
                <div
                  style={{
                    position: 'absolute', left: -5 / escala, top: -46 / escala, background: COR.verde, color: COR.branco,
                    fontFamily: FONTE, fontWeight: 700, fontSize: 26 / escala, padding: `${4 / escala}px ${14 / escala}px`,
                    borderRadius: 8 / escala, whiteSpace: 'nowrap',
                  }}
                >
                  {c.rotulo}
                </div>
              ) : null}
            </div>
          ) : null;
        })}
        {children?.(escala)}
      </div>
    </div>
  );
};

// Moldura do painel: card branco com sombra, ocupando a largura com margem.
export const Moldura: React.FC<{altura: number; entrada?: number; opacidade?: number; children: (largura: number, altura: number) => React.ReactNode}> = ({
  altura, entrada, opacidade = 1, children,
}) => {
  const t = useT();
  const largura = 1080 - 2 * 36;
  const h = altura - 20;
  // Entra inclinado em 3D e assenta (acompanha um whoosh).
  const p = entrada === undefined ? 1 : progresso(t, entrada, 0.45);
  return (
    <div
      style={{
        position: 'absolute', left: 36, top: 10, width: largura, height: h, borderRadius: 28, overflow: 'hidden',
        boxShadow: '0 30px 70px rgba(0,60,40,.28)', opacity: opacidade * Math.min(1, p * 2), background: COR.branco,
        transform: `perspective(1400px) translateY(${(1 - p) * 160}px) rotateX(${(1 - p) * 28}deg) scale(${0.9 + 0.1 * p})`,
      }}
    >
      {children(largura, h)}
    </div>
  );
};

// ---------- Blocos de diagrama ----------

export const Caixa: React.FC<{
  t0: number; x: number; y: number; w: number; h: number; children: React.ReactNode;
  cor?: string; fundo?: string; borda?: string; tamanho?: number; girar?: number; style?: React.CSSProperties;
}> = ({t0, x, y, w, h, children, cor = COR.tinta, fundo = COR.branco, borda, tamanho = 44, girar = 0, style}) => {
  const mola = useMola(t0);
  const t = useT();
  if (t < t0) return null;
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 26, background: fundo, color: cor,
        border: borda ? `4px solid ${borda}` : undefined, boxShadow: '0 16px 44px rgba(0,60,40,.16)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: FONTE,
        fontWeight: 700, fontSize: tamanho, lineHeight: 1.15, letterSpacing: -0.5, padding: 16, boxSizing: 'border-box',
        opacity: Math.min(1, mola * 1.4), transform: `translateY(${(1 - mola) * 40}px) rotate(${girar}deg) scale(${0.85 + 0.15 * mola})`, ...style,
      }}
    >
      {children}
    </div>
  );
};

export const Seta: React.FC<{t0: number; x1: number; y1: number; x2: number; y2: number; cor?: string; tracejada?: boolean}> = ({
  t0, x1, y1, x2, y2, cor = COR.verde, tracejada,
}) => {
  const t = useT();
  const p = progresso(t, t0, 0.5);
  if (p <= 0) return null;
  const len = Math.hypot(x2 - x1, y2 - y1);
  const ang = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  return (
    <div style={{position: 'absolute', left: x1, top: y1, width: len, height: 0, transform: `rotate(${ang}deg)`, transformOrigin: '0 0'}}>
      <div
        style={{
          position: 'absolute', left: 0, top: -4, height: 8, width: (len - 18) * p, borderRadius: 4,
          background: tracejada ? `repeating-linear-gradient(90deg, ${cor} 0 18px, transparent 18px 30px)` : cor,
        }}
      />
      {p > 0.95 ? (
        <div style={{position: 'absolute', left: len - 30, top: -16, width: 0, height: 0, borderTop: '16px solid transparent', borderBottom: '16px solid transparent', borderLeft: `30px solid ${cor}`}} />
      ) : null}
    </div>
  );
};

export const Logo: React.FC<{versao?: 'verde' | 'preto'; largura: number; style?: React.CSSProperties}> = ({versao = 'preto', largura, style}) => (
  // Versões com fundo transparente geradas a partir de logos/logo_beeno-2.png (verde) e -3.png (preto).
  <Img src={staticFile(`${PROJETO}/hf/logo_beeno_${versao}_alpha.png`)} style={{width: largura, height: (largura * 1105) / 2937, ...style}} />
);

// ---------- Cartela final (painel) ----------

export const CartelaFinal: React.FC<{t0: number; altura: number; botao: string; tBotao: number; tClique?: number; extra?: {texto: string; t: number}}> = ({
  t0, altura, botao, tBotao, tClique, extra,
}) => {
  const t = useT();
  const logo = useMola(t0);
  const b = useMola(tBotao);
  const apertado = tClique !== undefined && t >= tClique && t < tClique + 0.15 ? 0.92 : 1;
  const pulso = apertado * (1 + 0.035 * Math.sin(Math.max(0, t - tBotao - 0.6) * 5));
  const pe = extra ? progresso(t, extra.t, 0.4) : 0;
  return (
    <AbsoluteFill style={{height: altura, alignItems: 'center', justifyContent: 'center', fontFamily: FONTE}}>
      <div style={{opacity: logo, transform: `translateY(${(1 - logo) * 30}px)`}}>
        <Logo largura={560} />
      </div>
      <div style={{width: 90, height: 8, borderRadius: 4, background: COR.verde, marginTop: 26, opacity: logo}} />
      <div style={{marginTop: 26, fontSize: 40, fontWeight: 600, color: COR.cinza, opacity: progresso(t, t0 + 0.3, 0.4)}}>
        O CRM feito para a sua operação na Blip
      </div>
      <div
        style={{
          marginTop: 46, background: COR.verde, color: COR.branco, fontWeight: 800, fontSize: 48, padding: '24px 54px',
          borderRadius: 999, boxShadow: '0 18px 44px rgba(0,160,106,.35)', opacity: Math.min(1, b * 1.5),
          transform: `scale(${(0.7 + 0.3 * b) * pulso})`,
        }}
      >
        {botao}
      </div>
      {tClique !== undefined ? (
        <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: altura}}>
          <Cursor de={tClique - 0.6} clique={tClique} ate={999} x0={900} y0={altura - 40} x1={640} y1={altura / 2 + 150} />
        </div>
      ) : null}
      {extra ? (
        <div style={{marginTop: 26, fontSize: 40, fontWeight: 700, color: COR.tinta, opacity: pe, transform: `translateY(${(1 - pe) * 16}px)`}}>
          {extra.texto}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Painel que só existe dentro de uma janela de tempo, com fade cruzado.
export const Cena: React.FC<{de: number; ate: number; children: React.ReactNode}> = ({de, ate, children}) => {
  const t = useT();
  const o = janela(t, de, ate, 0.3);
  if (o <= 0) return null;
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

// ---------- Efeitos sonoros ----------

export type EventoSom = {t: number; som: string; volume?: number};

// Cada som entra no segundo exato do evento. Os .wav vêm de ferramentas/gerar_sfx.py.
// GANHO_SONS deixa os efeitos sob a voz; o limitador final (masterizar.sh) segura os picos.
const GANHO_SONS = 1;
export const Sons: React.FC<{eventos: EventoSom[]}> = ({eventos}) => {
  const {fps} = useVideoConfig();
  return (
    <>
      {eventos.map((e, i) => (
        <Sequence key={i} from={Math.max(0, Math.round(e.t * fps))} durationInFrames={Math.round(3 * fps)} premountFor={fps}>
          <Audio src={staticFile(`${PROJETO}/sfx/${e.som}.wav`)} volume={(e.volume ?? 0.5) * GANHO_SONS} />
        </Sequence>
      ))}
    </>
  );
};

// ---------- Tela de impacto (fundo branco, palavras batendo) ----------

export type LinhaImpacto = {texto: string; t: number; cor?: string; riscarEm?: number; tamanho?: number};

export const ImpactoTela: React.FC<{de: number; ate: number; linhas: LinhaImpacto[]; fundo?: string; tinta?: string}> = ({
  de, ate, linhas, fundo = COR.branco, tinta = COR.tinta,
}) => {
  const t = useT();
  if (t < de || t >= ate) return null;
  const {dx, dy} = tremidaEm(t, linhas.map((l) => l.t), 16);
  // estouro de luz nos primeiros quadros
  const estouro = 1 - progresso(t, de, 0.12);
  return (
    <AbsoluteFill style={{background: fundo, alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, rgba(0,203,136,.10), transparent 60%)'}} />
      <div style={{transform: `translate(${dx}px, ${dy}px)`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, padding: '0 50px'}}>
        {linhas.map((l, i) => {
          const k = t - l.t;
          if (k < 0) return null;
          const p = Math.min(1, k / 0.16);
          const escala = 1 + 1.3 * (1 - p) ** 3;
          const risco = l.riscarEm !== undefined ? progresso(t, l.riscarEm, 0.25) : 0;
          return (
            <div
              key={i}
              style={{
                position: 'relative', fontFamily: FONTE, fontWeight: 800, fontSize: l.tamanho ?? 128, lineHeight: 1.0,
                letterSpacing: -4, textTransform: 'uppercase', color: l.cor ?? tinta, textAlign: 'center',
                transform: `scale(${escala})`, filter: `blur(${(1 - p) * 10}px)`, opacity: Math.min(1, p * 2),
              }}
            >
              {l.texto}
              {risco > 0 ? (
                <div style={{position: 'absolute', left: -10, top: '50%', height: 16, width: `calc(${risco * 100}% + 20px)`, background: COR.vermelho, borderRadius: 8, transform: 'rotate(-4deg)'}} />
              ) : null}
            </div>
          );
        })}
      </div>
      <AbsoluteFill style={{background: COR.branco, opacity: estouro}} />
    </AbsoluteFill>
  );
};

// ---------- Flash branco e luz vazada ----------

export const Flash: React.FC<{t0: number; dur?: number; forca?: number}> = ({t0, dur = 0.3, forca = 1}) => {
  const t = useT();
  const k = t - t0;
  if (k < 0 || k > dur) return null;
  return <AbsoluteFill style={{background: COR.branco, opacity: forca * (1 - k / dur) ** 1.5, pointerEvents: 'none'}} />;
};

// Luz quente varrendo a tela (como o "light leak" das transições da referência).
export const LuzVazada: React.FC<{t0: number; dur?: number}> = ({t0, dur = 0.8}) => {
  const t = useT();
  const k = (t - t0) / dur;
  if (k < 0 || k > 1) return null;
  const o = Math.sin(Math.PI * k);
  const x = -30 + 160 * k;
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', opacity: o, pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse 70% 60% at ${x}% 40%, rgba(255,170,90,.95), rgba(255,110,60,.55) 40%, transparent 75%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse 45% 35% at ${x + 20}% 70%, rgba(255,240,200,.9), transparent 70%)`}} />
    </AbsoluteFill>
  );
};

// ---------- Texto que bate na tela (sobre a câmera) ----------

export const Slam: React.FC<{
  t0: number; ate: number; texto: React.ReactNode; top: number; tamanho?: number; cor?: string; fundo?: string; girar?: number;
}> = ({t0, ate, texto, top, tamanho = 92, cor = COR.branco, fundo, girar = -3}) => {
  const t = useT();
  const k = t - t0;
  if (k < 0) return null;
  const sai = 1 - progresso(t, ate - 0.2, 0.2);
  if (sai <= 0) return null;
  const p = Math.min(1, k / 0.14);
  const escala = 1 + 0.9 * (1 - p) ** 3 + 0.04 * Math.sin(Math.min(k, 0.5) * 30) * Math.max(0, 1 - k / 0.5);
  return (
    <div style={{position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: sai}}>
      <div
        style={{
          fontFamily: FONTE, fontWeight: 800, fontSize: tamanho, lineHeight: 1.02, letterSpacing: -2, textTransform: 'uppercase',
          color: cor, background: fundo, padding: fundo ? '6px 26px' : 0, borderRadius: 16, textAlign: 'center',
          transform: `rotate(${girar}deg) scale(${escala})`, filter: `blur(${(1 - p) * 8}px)`,
          WebkitTextStroke: fundo ? undefined : '3px rgba(0,0,0,.9)', paintOrder: 'stroke fill',
          textShadow: fundo ? undefined : '0 10px 30px rgba(0,0,0,.6)', boxShadow: fundo ? '0 18px 40px rgba(0,0,0,.35)' : undefined,
        }}
      >
        {texto}
      </div>
    </div>
  );
};

// ---------- Etiquetas empilhando acima da cabeça (como os valores da referência) ----------

export const PilhaEtiquetas: React.FC<{itens: {texto: string; t: number; fundo?: string}[]; ate: number; base: number}> = ({itens, ate, base}) => {
  const t = useT();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sai = 1 - progresso(t, ate - 0.15, 0.15);
  if (t < itens[0].t || sai <= 0) return null;
  return (
    <>
      {itens.map((it, i) => {
        if (t < it.t) return null;
        const m = spring({frame: frame - it.t * fps, fps, config: {damping: 9, stiffness: 220}});
        const girar = [-4, 3, -2][i % 3];
        return (
          <div key={i} style={{position: 'absolute', top: base - i * 96, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: sai}}>
            <div
              style={{
                position: 'relative', background: it.fundo ?? '#FF6A2B', color: COR.branco, fontFamily: FONTE, fontWeight: 800, fontSize: 52,
                padding: '8px 30px', borderRadius: 14, transform: `rotate(${girar}deg) scale(${m})`, boxShadow: '0 12px 30px rgba(0,0,0,.35)',
                textTransform: 'uppercase', letterSpacing: -1, whiteSpace: 'nowrap',
              }}
            >
              {it.texto}
              <div style={{position: 'absolute', left: '50%', bottom: -14, marginLeft: -14, width: 0, height: 0, borderLeft: '14px solid transparent', borderRight: '14px solid transparent', borderTop: `16px solid ${it.fundo ?? '#FF6A2B'}`}} />
            </div>
          </div>
        );
      })}
    </>
  );
};

// ---------- Cursor que vai até um ponto e clica ----------

// Coordenadas no mesmo espaço do pai (ex.: pixels do print dentro do PrintZoom). `escala` compensa o zoom do print.
export const Cursor: React.FC<{de: number; clique: number; ate: number; x0: number; y0: number; x1: number; y1: number; escala?: number; arrastar?: {x: number; y: number; ate: number}}> = ({
  de, clique, ate, x0, y0, x1, y1, escala = 1, arrastar,
}) => {
  const t = useT();
  if (t < de || t > ate) return null;
  const p = progresso(t, de, Math.max(0.1, clique - de - 0.05));
  let x = x0 + (x1 - x0) * p;
  let y = y0 + (y1 - y0) * p;
  if (arrastar) {
    const q = progresso(t, clique + 0.05, arrastar.ate - clique - 0.05);
    x += (arrastar.x - x1) * q;
    y += (arrastar.y - y1) * q;
  }
  const k = t - clique;
  const aperta = k >= 0 && (arrastar ? t < arrastar.ate : k < 0.15) ? 0.85 : 1;
  const onda = k >= 0 && k < 0.45 ? k / 0.45 : -1;
  const s = 1 / escala;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 0, height: 0, opacity: 1 - progresso(t, ate - 0.2, 0.2)}}>
      {onda >= 0 ? (
        <div style={{position: 'absolute', left: -40 * s * onda, top: -40 * s * onda, width: 80 * s * onda, height: 80 * s * onda, borderRadius: '50%', border: `${4 * s}px solid ${COR.verde}`, opacity: 1 - onda}} />
      ) : null}
      <svg width={44 * s} height={56 * s} viewBox="0 0 22 28" style={{position: 'absolute', left: -4 * s, top: -2 * s, transform: `scale(${aperta})`, transformOrigin: '10% 5%', filter: `drop-shadow(0 ${3 * s}px ${4 * s}px rgba(0,0,0,.35))`}}>
        <path d="M2 1 L2 22 L7.5 16.8 L11.2 25.5 L15 23.8 L11.4 15.3 L19 15.3 Z" fill="#fff" stroke="#111" strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
    </div>
  );
};
