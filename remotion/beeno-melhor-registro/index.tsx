import React from 'react';
import {AbsoluteFill, Audio, staticFile} from 'remotion';
import palavrasJson from '../transcricao/15-56-43-cortado/palavras.json';
import {Cursor, EventoSom, PrintZoom, Sons, progresso, useT} from '../_beeno/componentes';
import {
  BEENO, BlocoDark, CameraBeeno, CardVidro, CenaBeeno, ConfigCamera, ConfigLegenda, FlashBranco, LegendaBeeno, LinhaChave, ListaCheck,
  LogoEntrada, SplitBroll, TituloDark, XDesenhado, cenaEm,
} from '../_beeno/estilo';
import {COR, FONTE, PROJETO, Palavra, criarGatilhos} from '../_beeno/tema';

// Vídeo B, "O melhor registro", no estilo Beeno (guia-edicao/1-estilo-beeno.md), família B (selfie) com blocos Beeno dark.
// Master: cópia sem as pausas longas (pedido da pessoa); original intocado.
export const VIDEO_B = 'Teleprompter-2026-06-10_15-56-43_cortado.mp4';
export const DURACAO_B = 1152; // quadros a 30 fps = duração do master

const palavras = palavrasJson as Palavra[];
const T = criarGatilhos(palavras);
const ANTES = 0.05; // o corte cai ~1,5 quadro antes da 1ª palavra da frase

// Rosto medido nos quadros (frames/rosto.json): x ≈ 555, cabelo y ≈ 630, queixo y ≈ 1290 (mais baixo que no vídeo A).
// O punch-in ancora no queixo para nunca cortar o rosto nem invadir a legenda.
const CAMERA: ConfigCamera = {
  rosto: {x: 555, y: 1290},
  split: {s: 1.15, x: -98, y: -684.5}, // cabelo em y ≈ 40, queixo em y ≈ 800
  palco: {s: 1.5, x: -292, y: -935}, // queixo em y ≈ 1000; texto e logo abaixo dele
  painelX: -285,
};

const ABERTO = 1;
const MEDIO = 1.15;
const FECHADO = 1.3;

// O logo entra quando termina "…com uma tag" e aterrissa ~0,3 s antes de "Beeno" (manual, seção 6.2; escolha da pessoa).
const LOGO_DE = 17.62;
const KANBAN_DE = 18.6;

const CENAS: CenaBeeno[] = [
  {de: 0, tipo: 'camera', escala: ABERTO},
  {de: T('ninguém', 1) - ANTES, tipo: 'camera', escala: MEDIO},
  {de: T('Pare') - ANTES, tipo: 'impacto', escala: FECHADO, pb: true},
  {de: T('Parece') - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('Mas') - ANTES, tipo: 'split'},
  {de: T('vai') - ANTES, tipo: 'impacto', escala: FECHADO},
  {de: T('O caminho'), tipo: 'palco'},
  {de: T('Na operação') - ANTES, tipo: 'dark'},
  {de: LOGO_DE, tipo: 'palco'},
  {de: KANBAN_DE, tipo: 'dark'},
  {de: T('Quando') - ANTES, tipo: 'camera', escala: MEDIO},
  {de: T('o dado') - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('o gestor') - ANTES, tipo: 'split'},
  {de: T('fiscal') - ANTES, tipo: 'palco'},
  {de: T('O registro bom') - ANTES, tipo: 'camera', escala: FECHADO},
  {de: T('ninguém', 2) - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('Clique') - ANTES, tipo: 'camera', escala: MEDIO},
  {de: T('agende') - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('para conhecer') - ANTES, tipo: 'camera', escala: MEDIO},
];

const LEGENDA: ConfigLegenda = {
  palavras,
  cores: [
    {t: T('falhar'), cor: BEENO.vermelho},
    {t: T('consequência'), cor: BEENO.verde},
    {t: T('tarefa'), cor: BEENO.vermelho},
    {t: T('a mais'), cor: BEENO.vermelho},
    {t: T('mais', 2), cor: BEENO.vermelho},
    {t: T('completo'), cor: BEENO.verde},
    {t: T('demo'), cor: BEENO.verde},
  ],
  caixaAlta: [T('ninguém', 1)],
  quebras: CENAS.map((c) => c.de),
  yPorCena: (t) => {
    const c = cenaEm(t, CENAS);
    if (c.tipo === 'palco' || c.tipo === 'dark') return null;
    if (c.tipo === 'split') return 880;
    return 1420;
  },
  amarelaEm: (t) => !!cenaEm(t, CENAS).pb,
};

const BLIP = 'tela_extensao-blip-desk.png';
const KANBAN = 'WhatsApp Image 2026-09-01 at 20.32.08.jpeg';
const FICHA = 'WhatsApp Image 2026-09-01 at 20.36.42.jpeg';
// Dados reais nos prints (e-mail e telefone) ficam desfocados.
const OCULTAR_BLIP = [{x: 1410, y: 268, w: 112, h: 24}, {x: 1626, y: 296, w: 192, h: 24}];
const OCULTAR_FICHA = [{x: 866, y: 210, w: 180, h: 21}];

// Tag em coordenadas do print (o chip acompanha o zoom do print).
const TagNoPrint: React.FC<{t0: number; x: number; y: number}> = ({t0, x, y}) => {
  const t = useT();
  const p = progresso(t, t0, 0.2);
  if (p <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, transform: `translateY(${(1 - p) * -30}px) scale(${0.6 + 0.4 * p})`, opacity: p,
        transformOrigin: 'left center', background: COR.verde, color: COR.branco, fontFamily: FONTE, fontWeight: 700, fontSize: 20,
        padding: '5px 14px', borderRadius: 999, boxShadow: '0 6px 16px rgba(0,120,80,.35)', whiteSpace: 'nowrap',
      }}
    >
      # Proposta enviada
    </div>
  );
};

// Kanban (1600×720): card "Têxtil Andorinha" em Diagnóstico realizado vai para Proposta enviada.
const CARD_ORIGEM = {x: 818, y: 288, w: 222, h: 200};
const CARD_DESTINO_X = 1068;

const Kanban: React.FC = () => {
  const t = useT();
  const anda = progresso(t, T('move'), 0.8);
  const ativo = t >= T('move');
  return (
    <PrintZoom arquivo={KANBAN} iw={1600} ih={720} largura={1000} altura={600} vistas={[{t: 0, x: 790, y: 236, w: 530, h: 318}]}>
      {(escala) => (
        <>
          {ativo ? (
            <div
              style={{
                position: 'absolute', left: CARD_ORIGEM.x, top: CARD_ORIGEM.y, width: CARD_ORIGEM.w, height: CARD_ORIGEM.h,
                background: '#F4F6F5', border: `${2 / escala}px dashed #C9D3CF`, borderRadius: 8, opacity: anda,
              }}
            />
          ) : null}
          {/* Recorte do próprio print: o card real é o que se move. */}
          <div
            style={{
              position: 'absolute', left: CARD_ORIGEM.x + (CARD_DESTINO_X - CARD_ORIGEM.x) * anda, top: CARD_ORIGEM.y - 10 * Math.sin(anda * Math.PI),
              width: CARD_ORIGEM.w, height: CARD_ORIGEM.h, borderRadius: 8, opacity: ativo ? 1 : 0,
              backgroundImage: `url(${staticFile(`${PROJETO}/prints/${KANBAN}`)})`, backgroundSize: '1600px 720px',
              backgroundPosition: `-${CARD_ORIGEM.x}px -${CARD_ORIGEM.y}px`,
              boxShadow: `0 ${12 / escala}px ${30 / escala}px rgba(0,0,0,.25), 0 0 0 ${3 / escala}px ${COR.verde}`,
            }}
          />
          <TagNoPrint t0={T('tag', 2)} x={CARD_ORIGEM.x + 8 + (CARD_DESTINO_X - CARD_ORIGEM.x) * anda} y={CARD_ORIGEM.y + 52} />
          {/* O cursor agarra o card e arrasta para a próxima etapa. */}
          <Cursor
            de={T('move') - 0.5} clique={T('move') - 0.02} ate={T('move') + 1.1} escala={escala}
            x0={1180} y0={500} x1={CARD_ORIGEM.x + 120} y1={CARD_ORIGEM.y + 130}
            arrastar={{x: CARD_DESTINO_X + 120, y: CARD_ORIGEM.y + 130, ate: T('move') + 0.8}}
          />
        </>
      )}
    </PrintZoom>
  );
};

const SONS: EventoSom[] = [
  {t: T('Pare') - 0.1, som: 'impacto', volume: 0.35},
  {t: T('falhar') - 0.05, som: 'erro', volume: 0.28},
  {t: T('O caminho') - 1.4, som: 'riser', volume: 0.22},
  {t: T('O caminho') - 0.08, som: 'whoosh_curto', volume: 0.44},
  {t: T('capturar') - 0.05, som: 'impacto', volume: 0.45},
  {t: T('Na operação') - 0.13, som: 'whoosh_curto', volume: 0.4},
  {t: T('Na operação') + 0.15, som: 'clique', volume: 0.2},
  {t: T('classifica') - 0.1, som: 'clique', volume: 0.22},
  {t: T('tag', 1) - 0.05, som: 'pop', volume: 0.28},
  {t: LOGO_DE - 0.03, som: 'whoosh', volume: 0.44},
  {t: LOGO_DE + 0.24, som: 'impacto', volume: 0.55},
  {t: T('tag', 2) - 0.05, som: 'pop', volume: 0.28},
  {t: T('move') - 0.07, som: 'clique', volume: 0.22},
  {t: T('move') + 0.05, som: 'deslizar', volume: 0.3},
  {t: T('move') + 0.8, som: 'notificacao', volume: 0.26},
  {t: T('conversa', 2) - 0.05, som: 'pop', volume: 0.28},
  {t: T('histórico') - 0.05, som: 'pop', volume: 0.28},
  {t: T('chegar') - 0.05, som: 'pop', volume: 0.3},
  {t: T('Quando') - 0.13, som: 'whoosh_curto', volume: 0.4},
  {t: T('fiscal') - 0.1, som: 'impacto', volume: 0.45},
  {t: T('preenchimento') + 0.12, som: 'erro', volume: 0.3},
  {t: T('Clique') - 0.13, som: 'whoosh_curto', volume: 0.4},
];

const BlocoProduto: React.FC = () => (
  <>
    {/* Blip: o atendente classifica a conversa com uma tag (brilho azul-petróleo, cor da Blip). */}
    <BlocoDark de={T('Na operação') - ANTES} ate={LOGO_DE} brilho="blip">
      <CardVidro t0={T('Na operação') + 0.15} x={40} y={230} w={1000} h={760}>
        <PrintZoom
          arquivo={BLIP} iw={1920} ih={1080} largura={1000} altura={760} ocultar={OCULTAR_BLIP}
          vistas={[
            {t: 0, x: 577, y: 168, w: 1263, h: 852},
            {t: T('classifica') - 0.4, x: 580, y: 180, w: 600, h: 456},
          ]}
          marcas={[{t: T('classifica'), x: 590, y: 282, w: 130, h: 26}]}
        >
          {(escala) => (
            <>
              <Cursor de={T('classifica') - 0.6} clique={T('classifica') - 0.05} ate={T('tag', 1) + 0.3} x0={1000} y0={560} x1={650} y1={296} escala={escala} />
              <TagNoPrint t0={T('tag', 1)} x={735} y={280} />
            </>
          )}
        </PrintZoom>
      </CardVidro>
      <TituloDark
        y={1180}
        contexto={{texto: 'na operação com a Blip', t: T('Na operação') + 0.15, destaque: {w: 'Blip', cor: BEENO.azul}}}
        titulos={[[{w: 'o atendente', t: T('atendente')}, {w: 'classifica', t: T('classifica'), cor: BEENO.menta}, {w: 'com uma tag.', t: T('com uma')}]]}
      />
    </BlocoDark>

    {/* Beeno: a tag move o negócio no funil. */}
    <BlocoDark de={KANBAN_DE} ate={T('A conversa já') - ANTES}>
      <CardVidro t0={KANBAN_DE} x={40} y={300} w={1000} h={600}>
        <Kanban />
      </CardVidro>
      <TituloDark
        y={1100}
        contexto={{texto: 'no Beeno,', t: KANBAN_DE}}
        titulos={[[{w: 'a tag', t: T('tag', 2)}, {w: 'move o negócio', t: T('move'), cor: BEENO.menta}, {w: 'no funil.', t: T('no funil')}]]}
      />
    </BlocoDark>

    {/* O que já existe só precisa chegar no CRM. */}
    <BlocoDark de={T('A conversa já') - ANTES} ate={T('Quando') - ANTES}>
      <CardVidro t0={T('A conversa já') + 0.15} x={40} y={230} w={1000} h={640}>
        <PrintZoom arquivo={FICHA} iw={1600} ih={774} largura={1000} altura={640} ocultar={OCULTAR_FICHA} vistas={[{t: 0, x: 352, y: 170, w: 935, h: 598}]} />
      </CardVidro>
      <ListaCheck
        x={110} y={960}
        itens={[{texto: 'a conversa já existe', t: T('conversa', 2)}, {texto: 'o histórico já existe', t: T('histórico')}]}
      />
      <TituloDark y={1180} titulos={[[{w: 'só precisa', t: T('só precisa')}, {w: 'chegar no CRM.', t: T('chegar'), cor: BEENO.menta}]]} />
    </BlocoDark>
  </>
);

export const BeenoMelhorRegistro: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <CameraBeeno video={VIDEO_B} cenas={CENAS} config={CAMERA} />

    <SplitBroll arquivo="B1_postits.mp4" de={T('Mas') - ANTES} ate={T('vai') - ANTES} desloc={600} />
    <SplitBroll arquivo="B2_prancheta.mp4" de={T('o gestor') - ANTES} ate={T('fiscal') - ANTES} desloc={-40} escala={1.32} />

    {/* Virada: "CAPTURAR o que já acontece" no palco */}
    <LinhaChave
      de={T('O caminho')} ate={T('Na operação') - ANTES} y={1060}
      contexto={{texto: 'o caminho é', t: T('O caminho')}}
      palavras={[{w: 'capturar', t: T('capturar'), grande: true, cor: BEENO.verde}, {w: 'o que já', t: T('o que já'), quebra: true}, {w: 'acontece', t: T('acontece')}]}
    />

    <BlocoProduto />

    {/* Logo Beeno uma vez, no palco, abaixo do queixo */}
    <LogoEntrada de={LOGO_DE} ate={KANBAN_DE} y={1230} variante="whip" />

    {/* "fiscal de preenchimento" com X desenhado */}
    <XDesenhado
      de={T('fiscal') - ANTES} ate={T('O registro bom') - ANTES} y={1080}
      linhas={[{texto: 'FISCAL DE', t: T('fiscal')}, {texto: 'PREENCHIMENTO', t: T('preenchimento')}]}
      tX={T('preenchimento') + 0.15}
    />

    <FlashBranco t0={T('O caminho')} quente />
    <FlashBranco t0={T('Na operação') - ANTES} />
    <FlashBranco t0={T('Quando') - ANTES} />
    <FlashBranco t0={T('Clique') - ANTES} />

    {/* Trilha entra na virada (musica/compor_trilha.py), ~15 dB abaixo da voz. */}
    <Audio src={staticFile(`${PROJETO}/musica/trilha_B_melhor-registro.wav`)} volume={0.11} />
    <Sons eventos={SONS} />

    <LegendaBeeno config={LEGENDA} />
  </AbsoluteFill>
);
