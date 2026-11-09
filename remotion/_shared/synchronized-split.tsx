import React from 'react';
import {interpolate} from 'remotion';

const clamp = {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
} as const;

export type SynchronizedSplitConfig = {
  canvasWidth?: number;
  canvasHeight?: number;
  splitCameraLeft?: number;
  splitCameraTop?: number;
  splitCameraWidth?: number;
  splitCameraHeight?: number;
  splitCameraRadius?: number;
  splitVideoX?: number;
  splitVideoY?: number;
  panelGap?: number;
  panelTravel?: number;
};

export type SynchronizedSplitState = {
  progress: number;
  canvasWidth: number;
  canvasHeight: number;
  camera: {
    left: number;
    top: number;
    width: number;
    height: number;
    radius: number;
  };
  video: {
    x: number;
    y: number;
  };
  panel: {
    visibleWidth: number;
    translateX: number;
    gap: number;
  };
};

export const getSynchronizedSplitState = (
  rawProgress: number,
  config: SynchronizedSplitConfig = {},
): SynchronizedSplitState => {
  const progress = Math.max(0, Math.min(1, rawProgress));
  const canvasWidth = config.canvasWidth ?? 1920;
  const canvasHeight = config.canvasHeight ?? 1080;
  const splitCameraLeft = config.splitCameraLeft ?? 1210;
  const panelGap = config.panelGap ?? 32;
  const cameraLeft = interpolate(progress, [0, 1], [0, splitCameraLeft], clamp);

  return {
    progress,
    canvasWidth,
    canvasHeight,
    camera: {
      left: cameraLeft,
      top: interpolate(progress, [0, 1], [0, config.splitCameraTop ?? 70], clamp),
      width: interpolate(progress, [0, 1], [canvasWidth, config.splitCameraWidth ?? 650], clamp),
      height: interpolate(progress, [0, 1], [canvasHeight, config.splitCameraHeight ?? 940], clamp),
      radius: interpolate(progress, [0, 1], [0, config.splitCameraRadius ?? 30], clamp),
    },
    video: {
      x: interpolate(progress, [0, 1], [0, config.splitVideoX ?? -635], clamp),
      y: interpolate(progress, [0, 1], [0, config.splitVideoY ?? -70], clamp),
    },
    panel: {
      visibleWidth: Math.max(0, cameraLeft - panelGap),
      translateX: (1 - progress) * -(config.panelTravel ?? 90),
      gap: panelGap,
    },
  };
};

export const SynchronizedCameraFrame: React.FC<{
  state: SynchronizedSplitState;
  children: React.ReactNode;
  boxShadow?: string;
}> = ({state, children, boxShadow = '0 30px 90px rgba(0,0,0,.5)'}) => (
  <div
    style={{
      position: 'absolute',
      left: state.camera.left,
      top: state.camera.top,
      width: state.camera.width,
      height: state.camera.height,
      overflow: 'hidden',
      borderRadius: state.camera.radius,
      boxShadow: state.progress > 0.01 ? boxShadow : 'none',
    }}
  >
    {children}
  </div>
);

export const SynchronizedSplitPanel: React.FC<{
  state: SynchronizedSplitState;
  children: React.ReactNode;
}> = ({state, children}) => (
  <div
    style={{
      position: 'absolute',
      left: 0,
      top: 0,
      width: state.panel.visibleWidth,
      height: state.canvasHeight,
      overflow: 'hidden',
    }}
  >
    <div
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: state.canvasWidth,
        height: state.canvasHeight,
        transform: `translateX(${state.panel.translateX}px)`,
      }}
    >
      {children}
    </div>
  </div>
);


// Versão vertical (9:16): painel em cima, câmera em card embaixo.
// Câmera e painel usam o mesmo `progress`, então entram e saem juntos.
// Com progress 0 a câmera ocupa a tela inteira com `fullZoom` em torno do ponto focal (o rosto).
export type SynchronizedVerticalSplitConfig = {
  canvasWidth?: number;
  canvasHeight?: number;
  card: {left: number; top: number; width: number; height: number; radius?: number};
  // Escala do vídeo dentro do card e posição do canto do vídeo relativa ao card.
  cardVideoScale: number;
  cardVideoX: number;
  cardVideoY: number;
  fullZoom?: number;
  focalX?: number;
  focalY?: number;
  panelTop?: number;
  panelGap?: number;
  panelTravel?: number;
  // Opcional: área do painel em qualquer lugar (ex.: câmera em cima e painel embaixo). Padrão: acima do card.
  panelArea?: {top: number; height: number};
  // Opcional: enquadramento de partida (progress 0) no lugar da tela cheia, para ir de um card a outro.
  from?: {
    card: {left: number; top: number; width: number; height: number; radius?: number};
    videoScale: number;
    videoX: number;
    videoY: number;
  };
};

export type SynchronizedVerticalSplitState = {
  progress: number;
  canvasWidth: number;
  canvasHeight: number;
  camera: {left: number; top: number; width: number; height: number; radius: number};
  video: {x: number; y: number; scale: number};
  panel: {top: number; visibleHeight: number; fullHeight: number; translateY: number};
};

export const getSynchronizedVerticalSplitState = (
  rawProgress: number,
  config: SynchronizedVerticalSplitConfig,
): SynchronizedVerticalSplitState => {
  const progress = Math.max(0, Math.min(1, rawProgress));
  const canvasWidth = config.canvasWidth ?? 1080;
  const canvasHeight = config.canvasHeight ?? 1920;
  const zoom = Math.max(1, config.fullZoom ?? 1);
  const fx = config.focalX ?? canvasWidth / 2;
  const fy = config.focalY ?? canvasHeight / 2;
  // Zoom em torno do rosto, preso aos limites para nunca mostrar borda preta.
  const fullX = Math.min(0, Math.max(canvasWidth - canvasWidth * zoom, fx - fx * zoom));
  const fullY = Math.min(0, Math.max(canvasHeight - canvasHeight * zoom, fy - fy * zoom));
  const lerp = (a: number, b: number) => interpolate(progress, [0, 1], [a, b], clamp);
  const panelTop = config.panelArea?.top ?? config.panelTop ?? 200;
  const panelGap = config.panelGap ?? 24;
  const cameraTop = lerp(config.from?.card.top ?? 0, config.card.top);
  const fullHeight = config.panelArea?.height ?? config.card.top - panelGap - panelTop;
  const de = config.from;

  return {
    progress,
    canvasWidth,
    canvasHeight,
    camera: {
      left: lerp(de?.card.left ?? 0, config.card.left),
      top: cameraTop,
      width: lerp(de?.card.width ?? canvasWidth, config.card.width),
      height: lerp(de?.card.height ?? canvasHeight, config.card.height),
      radius: lerp(de?.card.radius ?? 0, config.card.radius ?? 36),
    },
    video: {
      x: lerp(de?.videoX ?? fullX, config.cardVideoX),
      y: lerp(de?.videoY ?? fullY, config.cardVideoY),
      scale: lerp(de?.videoScale ?? zoom, config.cardVideoScale),
    },
    panel: {
      top: panelTop,
      visibleHeight: fullHeight,
      fullHeight,
      translateY: (1 - progress) * -(config.panelTravel ?? 60),
    },
  };
};

export const SynchronizedVerticalCamera: React.FC<{
  state: SynchronizedVerticalSplitState;
  children: React.ReactNode;
  boxShadow?: string;
}> = ({state, children, boxShadow = '0 24px 70px rgba(0,0,0,.28)'}) => (
  <div
    style={{
      position: 'absolute',
      left: state.camera.left,
      top: state.camera.top,
      width: state.camera.width,
      height: state.camera.height,
      overflow: 'hidden',
      borderRadius: state.camera.radius,
      boxShadow: state.progress > 0.01 ? boxShadow : 'none',
    }}
  >
    <div
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: state.canvasWidth,
        height: state.canvasHeight,
        transformOrigin: '0 0',
        transform: `translate(${state.video.x}px, ${state.video.y}px) scale(${state.video.scale})`,
      }}
    >
      {children}
    </div>
  </div>
);

// O painel fica atrás da câmera: enquanto o card desce, ele revela o painel.
export const SynchronizedVerticalPanel: React.FC<{
  state: SynchronizedVerticalSplitState;
  children: React.ReactNode;
}> = ({state, children}) => (
  <div
    style={{
      position: 'absolute',
      left: 0,
      top: state.panel.top,
      width: state.canvasWidth,
      height: state.panel.fullHeight,
      opacity: state.progress,
      transform: `translateY(${state.panel.translateY}px)`,
    }}
  >
    {children}
  </div>
);
