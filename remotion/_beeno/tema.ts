import {loadFont} from '@remotion/google-fonts/Poppins';
import {Easing} from 'remotion';

// Identidade tirada dos banners e logos do Beeno (projetos/001. beeno-video/prints e logos).
export const COR = {
  menta: '#EAFBF4',
  menta2: '#D2F4E5',
  verde: '#00CB88',
  verdeEscuro: '#009E6A',
  tinta: '#141414',
  cinza: '#5E6B66',
  branco: '#FFFFFF',
  amarelo: '#FFD43B',
  marca: 'rgba(255, 212, 59, .5)',
  vermelho: '#E5484D',
};

export const {fontFamily: FONTE} = loadFont('normal', {weights: ['500', '600', '700', '800'], subsets: ['latin', 'latin-ext']});

export const PROJETO = '001. beeno-video';
export const FPS = 30;

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const suave = Easing.inOut(Easing.cubic);

export type Palavra = {w: string; s: number; e: number};

export const normalizar = (w: string) =>
  w
    .trim()
    .toLowerCase()
    .replace(/^[-–]/, '')
    .replace(/[.,!?;:"“”]/g, '');

// Gatilhos sempre vêm do palavras.json: T('tickets') = início da 1ª ocorrência; T('perde', 3) = da 3ª.
// Aceita frase ("no outro") para desambiguar palavras curtas: devolve o início da primeira palavra.
export const criarGatilhos = (palavras: Palavra[]) => (texto: string, ocorrencia = 1) => {
  const alvo = texto.split(/\s+/).map(normalizar);
  const norm = palavras.map((p) => normalizar(p.w));
  let n = 0;
  for (let i = 0; i + alvo.length <= norm.length; i++) {
    if (alvo.every((a, k) => norm[i + k] === a) && ++n === ocorrencia) return palavras[i].s;
  }
  throw new Error(`"${texto}" (ocorrência ${ocorrencia}) não está no palavras.json`);
};
