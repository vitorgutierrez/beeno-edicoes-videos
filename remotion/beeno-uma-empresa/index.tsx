import React from 'react';
import {AbsoluteFill, Audio, staticFile} from 'remotion';
import palavrasJson from '../transcricao/15-50-07-cortado/palavras.json';
import {Cursor, EventoSom, PrintZoom, Sons} from '../_beeno/componentes';
import {
  BEENO, BlocoDark, CameraBeeno, CardVidro, CenaBeeno, ConfigCamera, ConfigLegenda, FlashBranco, LegendaBeeno, LinhaChave, ListaX,
  LogoEntrada, PaineisCor, SplitBroll, TituloDark, cenaEm,
} from '../_beeno/estilo';
import {PROJETO, Palavra, criarGatilhos} from '../_beeno/tema';

// Vídeo A, "Uma empresa só", no estilo Beeno (guia-edicao/1-estilo-beeno.md), família A (estúdio) com bloco Beeno dark.
// Master: cópia sem as pausas longas (pedido da pessoa); original intocado.
export const VIDEO_A = 'Teleprompter-2026-06-10_15-50-07_cortado.mp4';
export const DURACAO_A = 1239; // quadros a 30 fps = duração do master

const palavras = palavrasJson as Palavra[];
const T = criarGatilhos(palavras);
const ANTES = 0.05; // o corte cai ~1,5 quadro antes da 1ª palavra da frase

// Rosto medido nos quadros (frames/rosto.json): centro (550, 760), cabelo y ≈ 440, queixo y ≈ 1075.
const CAMERA: ConfigCamera = {
  rosto: {x: 550, y: 760},
  split: {s: 1.2, x: -120, y: -488}, // cabelo em y ≈ 40, queixo em y ≈ 800
  palco: {s: 1.25, x: -147.5, y: -444}, // queixo em y ≈ 900; texto e logo abaixo dele
  painelX: -280, // rosto no centro da metade esquerda
};

const ABERTO = 1;
const MEDIO = 1.3;
const FECHADO = 1.6;

const TERMINA_DARK = T('O seu') - ANTES;
const CENAS: CenaBeeno[] = [
  {de: 0, tipo: 'camera', escala: ABERTO},
  {de: T('já') - ANTES, tipo: 'camera', escala: MEDIO},
  {de: T('É') - ANTES, tipo: 'split'},
  {de: T('No outro') - ANTES, tipo: 'split'},
  {de: T('Nenhum') - ANTES, tipo: 'impacto', escala: FECHADO, pb: true},
  {de: T('Para', 1) - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('dois', 2) - ANTES, tipo: 'painel'},
  {de: T('Para', 2) - ANTES, tipo: 'palco'},
  {de: T('E ela') - ANTES, tipo: 'impacto', escala: FECHADO},
  {de: T('Quando') - ANTES, tipo: 'camera', escala: MEDIO},
  {de: T('o mesmo') - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('a empresa perde') - ANTES, tipo: 'palco'},
  {de: T('Com'), tipo: 'palco'},
  {de: T('os tickets') - 0.2, tipo: 'dark'},
  {de: TERMINA_DARK, tipo: 'camera', escala: ABERTO},
  {de: T('e a sua') - ANTES, tipo: 'camera', escala: FECHADO},
  {de: T('Quer') - ANTES, tipo: 'camera', escala: ABERTO},
  {de: T('conheça') - ANTES, tipo: 'camera', escala: MEDIO},
];

const LEGENDA: ConfigLegenda = {
  palavras,
  cores: [
    {t: T('comercial', 1), cor: BEENO.azul},
    {t: T('atendimento', 1), cor: BEENO.amarelo},
    {t: T('desorganizada'), cor: BEENO.vermelho},
    {t: T('também'), cor: BEENO.verde},
    {t: T('deveria'), cor: BEENO.verde},
    {t: T('plataforma'), cor: BEENO.verde},
  ],
  caixaAlta: [T('só', 2)],
  quebras: CENAS.map((c) => c.de),
  yPorCena: (t) => {
    const c = cenaEm(t, CENAS);
    if (c.tipo === 'palco' || c.tipo === 'dark') return null;
    if (c.tipo === 'split') return 880;
    if (c.tipo === 'painel') return {y: 1390, x: 8, largura: 524}; // só na metade da câmera
    return 1390;
  },
  amarelaEm: (t) => !!cenaEm(t, CENAS).pb,
};

const FICHA = 'WhatsApp Image 2026-09-01 at 20.36.42.jpeg';
const BLIP = 'tela_extensao-blip-desk.png';
// Dados reais nos prints (e-mail e telefone) ficam desfocados.
const OCULTAR_FICHA = [{x: 866, y: 210, w: 180, h: 21}];
const OCULTAR_BLIP = [{x: 1410, y: 268, w: 112, h: 24}, {x: 1626, y: 296, w: 192, h: 24}];

const SONS: EventoSom[] = [
  {t: T('chamado') - 0.05, som: 'notificacao', volume: 0.3},
  {t: T('proposta') - 0.05, som: 'clique', volume: 0.22},
  {t: T('Nenhum') - 0.1, som: 'impacto', volume: 0.35},
  {t: T('dois', 2) - 0.1, som: 'impacto', volume: 0.45},
  {t: T('departamentos') - 0.05, som: 'pop', volume: 0.28},
  {t: T('só', 1) - 0.05, som: 'impacto', volume: 0.45},
  {t: T('timing') - 0.05, som: 'pop', volume: 0.28},
  {t: T('argumento') - 0.05, som: 'pop', volume: 0.28},
  {t: T('cliente', 4) - 0.05, som: 'pop', volume: 0.3},
  {t: T('Com') - 1.4, som: 'riser', volume: 0.22},
  {t: T('Com') - 0.08, som: 'whoosh_curto', volume: 0.44},
  {t: T('Com') + 0.15, som: 'impacto', volume: 0.55},
  {t: T('os tickets') - 0.05, som: 'clique', volume: 0.22},
  {t: T('tickets') - 0.1, som: 'clique', volume: 0.22},
  {t: T('negócios') - 0.1, som: 'clique', volume: 0.22},
  {t: T('mesmo', 2) - 0.05, som: 'pop', volume: 0.28},
  {t: T('Quem') - 0.05, som: 'clique', volume: 0.22},
  {t: T('dois', 3) - 0.05, som: 'pop', volume: 0.28},
  {t: T('lados') + 0.1, som: 'pop', volume: 0.28},
  {t: TERMINA_DARK - 0.08, som: 'whoosh_curto', volume: 0.4},
  {t: T('Quer') - 0.13, som: 'whoosh_curto', volume: 0.4},
];

const BlocoProduto: React.FC = () => (
  <>
    {/* Ficha do contato: tickets do atendimento e negócios do comercial no mesmo lugar. */}
    <BlocoDark de={T('os tickets') - 0.2} ate={T('Quem') - ANTES}>
      <CardVidro t0={T('os tickets')} x={40} y={230} w={1000} h={780}>
        <PrintZoom
          arquivo={FICHA} iw={1600} ih={774} largura={1000} altura={780} ocultar={OCULTAR_FICHA}
          vistas={[
            {t: 0, x: 0, y: 40, w: 1600, h: 734},
            {t: T('tickets') - 0.35, x: 362, y: 60, w: 600, h: 320},
            {t: T('negócios') - 0.35, x: 362, y: 280, w: 600, h: 320},
            {t: T('mesmo', 2), x: 0, y: 40, w: 1600, h: 734},
          ]}
          marcas={[
            {t: T('tickets'), x: 368, y: 209, w: 356, h: 21},
            {t: T('negócios'), x: 368, y: 426, w: 542, h: 21},
          ]}
          contornos={[
            {t: T('mesmo', 2), x: 1302, y: 88, w: 280, h: 162, rotulo: 'Negócio'},
            {t: T('mesmo', 2) + 0.1, x: 1302, y: 286, w: 280, h: 128, rotulo: 'Ticket'},
          ]}
        >
          {(escala) => (
            <>
              <Cursor de={T('tickets') - 0.7} clique={T('tickets') - 0.05} ate={T('negócios') - 0.6} x0={880} y0={340} x1={520} y1={216} escala={escala} />
              <Cursor de={T('negócios') - 0.6} clique={T('negócios') - 0.05} ate={T('mesmo', 2)} x0={520} y0={216} x1={600} y1={434} escala={escala} />
            </>
          )}
        </PrintZoom>
      </CardVidro>
      <TituloDark
        y={1180}
        contexto={{texto: 'com o CRM integrado', t: T('os tickets')}}
        titulos={[
          [{w: 'tickets', t: T('tickets'), cor: BEENO.amarelo}, {w: '+ negócios', t: T('negócios'), cor: BEENO.azul}],
          [{w: 'no', t: T('no mesmo')}, {w: 'mesmo contato.', t: T('mesmo', 2), cor: BEENO.menta}],
        ]}
      />
    </BlocoDark>

    {/* Extensão no Blip Desk: quem atende vê a conversa e o CRM lado a lado. */}
    <BlocoDark de={T('Quem') - ANTES} ate={TERMINA_DARK} brilho="blip">
      <CardVidro t0={T('Quem') + 0.15} x={40} y={230} w={1000} h={700}>
        <PrintZoom
          arquivo={BLIP} iw={1920} ih={1080} largura={1000} altura={700} ocultar={OCULTAR_BLIP}
          vistas={[{t: 0, x: 577, y: 168, w: 1263, h: 852}]}
          contornos={[
            {t: T('dois', 3), x: 584, y: 178, w: 800, h: 834, rotulo: 'Conversa'},
            {t: T('lados'), x: 1394, y: 178, w: 440, h: 834, rotulo: 'CRM'},
          ]}
        />
      </CardVidro>
      <TituloDark
        y={1110}
        contexto={{texto: 'quem vai falar com o cliente', t: T('Quem') + 0.15}}
        titulos={[[{w: 'vê os', t: T('vê')}, {w: 'dois lados', t: T('dois', 3), cor: BEENO.menta}, {w: 'antes.', t: T('antes')}]]}
      />
    </BlocoDark>
  </>
);

export const BeenoUmaEmpresa: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <CameraBeeno video={VIDEO_A} cenas={CENAS} config={CAMERA} />

    {/* Segunda e terça: tela dividida com B-roll */}
    <SplitBroll arquivo="A1_segunda_celular.mp4" de={T('É') - ANTES} ate={T('No outro') - ANTES} desloc={250} />
    <SplitBroll arquivo="A2_terca_notebook.mp4" de={T('No outro') - ANTES} ate={T('Nenhum') - ANTES} desloc={525} />

    {/* "dois departamentos": painéis de cor (amarelo = atendimento, azul = comercial em todo o vídeo) */}
    <PaineisCor
      de={T('dois', 2) - ANTES} ate={T('Para', 2) - ANTES}
      itens={[
        {texto: 'Atendimento', t: T('dois', 2) - ANTES, fundo: BEENO.painelAmarelo, cor: '#141414'},
        {texto: 'Comercial', t: T('departamentos') - ANTES, fundo: BEENO.painelAzul, cor: '#FFFFFF'},
      ]}
    />

    {/* Palco: "uma empresa SÓ" */}
    <LinhaChave
      de={T('Para', 2) - ANTES} ate={T('E ela') - ANTES} y={1000}
      contexto={{texto: 'para o cliente,', t: T('Para', 2)}}
      palavras={[{w: 'uma', t: T('uma', 1), quebra: true}, {w: 'empresa', t: T('empresa', 2)}, {w: 'só', t: T('só', 1), grande: true, cor: BEENO.verde}]}
    />

    {/* Palco: o que a empresa perde */}
    <ListaX
      de={T('a empresa perde') - ANTES} ate={T('Com')} y={960}
      titulo={{texto: 'a empresa perde', t: T('a empresa perde')}}
      itens={[{texto: 'timing', t: T('timing')}, {texto: 'argumento', t: T('argumento')}, {texto: 'o cliente', t: T('cliente', 4)}]}
    />

    {/* Virada: logo Beeno no palco */}
    <LogoEntrada de={T('Com') + 0.03} ate={T('os tickets') - 0.2} y={1150} variante="zoom" />

    <BlocoProduto />

    <FlashBranco t0={T('Com')} quente />
    <FlashBranco t0={TERMINA_DARK} />
    <FlashBranco t0={T('Quer') - ANTES} />

    {/* Trilha entra na virada (musica/compor_trilha.py), ~15 dB abaixo da voz. */}
    <Audio src={staticFile(`${PROJETO}/musica/trilha_A_uma-empresa.wav`)} volume={0.17} />
    <Sons eventos={SONS} />

    <LegendaBeeno config={LEGENDA} />
  </AbsoluteFill>
);
