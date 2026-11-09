// Faixa de público para anúncios da Beeno (qualifica quem deve assistir, ex.: "EMPRESAS QUE ATENDEM PELO WHATSAPP").
// Padrão: uma linha fina no topo, pílula sólida cor de tinta com borda verde, que nunca cobre rosto, placa ou motions.
// No gancho entra junto uma segunda pílula, verde cheia, com a chamada ("ESSE VÍDEO É PRA VOCÊ"); depois do gancho
// ela se recolhe e fica só a pílula do público até o fim. Nos trechos em que o topo está ocupado, a pílula sobe e some.
// Copy sempre na 3ª pessoa ("empresas que…"), nunca "se você…" (atributo pessoal, barrado pela política da Meta).
// Sem transparência no texto nem no fundo da pílula (ajuste da v5 dos reels).
import {loadFont} from '@remotion/google-fonts/Poppins';
import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

const {fontFamily: POPPINS} = loadFont('normal', {weights: ['800'], subsets: ['latin', 'latin-ext']});
const VERDE = '#00CD8A';
const TINTA = '#0A1C15';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SAIDA = Easing.out(Easing.cubic);

export type FaixaPublicoProps = {
  linha1: string; // público (números como "+R$ 100 MIL/MÊS" ou "50 VENDEDORES" ficam verdes)
  linha2: string; // chamada, só no gancho
  chamadaAte?: number | null; // fim da chamada em s (null = sem chamada, ex.: o gancho já tem a sua)
  desde?: number; // quando a faixa aparece (padrão: 1º quadro)
  y?: number; // topo da pílula
  ocultar?: [number, number][]; // trechos (s do vídeo inteiro) em que o topo está ocupado
};

// Pinta de verde o número do público ("+R$ 100 MIL/MÊS", "R$ 1 MI/ANO", "10 VENDEDORES"...).
const comValor = (texto: string) => {
  const m = texto.match(/\+?R\$\s?[\d.,]+\s?(MIL|MI)?(\/(MÊS|ANO))?|\+?\d+\s?[A-ZÇÃÕÉ]+/);
  if (!m || m.index === undefined) return texto;
  return (
    <>
      {texto.slice(0, m.index)}
      <span style={{color: VERDE}}>{m[0]}</span>
      {texto.slice(m.index + m[0].length)}
    </>
  );
};

const caber = (texto: string, max: number) => Math.min(max, Math.floor(1000 / (texto.length * 0.66)));

export const FaixaPublico: React.FC<FaixaPublicoProps> = ({linha1, linha2, chamadaAte = 3.5, desde = 0, y = 46, ocultar = []}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  // Pílula do público: visível desde o 1º quadro (ou de `desde`); nos trechos ocupados sobe e sai (movimento, não transparência parcial).
  let visivel = desde > 0 ? interpolate(t, [desde, desde + 0.3], [0, 1], {...clamp, easing: SAIDA}) : 1;
  for (const [a, b] of ocultar) visivel *= 1 - Math.min(interpolate(t, [a - 0.18, a], [0, 1], clamp), interpolate(t, [b, b + 0.22], [1, 0], clamp));
  const pop = desde > 0 ? 1 : interpolate(t, [0, 0.22], [0.94, 1], {...clamp, easing: Easing.out(Easing.back(2))});

  // Chamada (só no gancho): entra logo abaixo e se recolhe para cima no fim do gancho.
  const temChamada = chamadaAte != null && t < chamadaAte + 0.4;
  const entra = interpolate(t, [0.15, 0.4], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.8))});
  const recolhe = chamadaAte != null ? interpolate(t, [chamadaAte, chamadaAte + 0.3], [0, 1], {...clamp, easing: SAIDA}) : 1;
  const tam1 = caber(linha1, 32);

  const pilula: React.CSSProperties = {
    borderRadius: 999,
    fontFamily: POPPINS,
    fontWeight: 800,
    letterSpacing: -0.2,
    textTransform: 'uppercase',
    whiteSpace: 'nowrap',
    boxShadow: '0 10px 26px rgba(0,0,0,.35)',
  };

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {temChamada ? (
        <div style={{position: 'absolute', left: 0, width: 1080, top: y + tam1 + 34, display: 'flex', justifyContent: 'center'}}>
          <div
            style={{
              ...pilula,
              padding: '8px 24px 9px',
              background: VERDE,
              color: TINTA,
              fontSize: caber(linha2, 30),
              opacity: entra > 0.5 && recolhe < 0.5 ? 1 : 0,
              transform: `translateY(${(1 - entra) * -16 - recolhe * 40}px) scale(${0.9 + 0.1 * entra - 0.1 * recolhe})`,
            }}
          >
            {linha2}
          </div>
        </div>
      ) : null}
      {visivel > 0.001 ? (
        <div style={{position: 'absolute', left: 0, width: 1080, top: y, display: 'flex', justifyContent: 'center'}}>
          <div
            style={{
              ...pilula,
              padding: '9px 26px 10px',
              background: TINTA,
              border: `2px solid ${VERDE}`,
              fontSize: tam1,
              color: '#fff',
              transform: `translateY(${(1 - visivel) * -120}px) scale(${pop})`,
            }}
          >
            {comValor(linha1.replace(/,\s*$/, ''))}
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
