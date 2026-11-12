/* p39 · 劝和不劝离 · generated */
ENGINE.visual("p39", (P) => {
  const H = P.hud;
  H.noirHeader(7, 7, "STAY / TOGETHER", { at: 0.04, right: 'NOIR / 07' });
  H.noirLabel('07.04', 1700, 140, { size: 11, color: 'faint', at: 0.7 });

  P.noirGhost("聊", { x: 1280, y: 180, size: 300, opacity: 0.07 });
  P.noirReveal("劝和不劝离", { x: 960, y: 240, w: 1300, align: 'c', size: 74, color: 'orange', at: 0.3, dur: 0.7, stagger: 0.05 });
  P.text("无论遇上什么困惑，都可以来找李安聊聊", { x: 960, y: 360, w: 1100, align: 'c', size: 32, font: 'serif', color: 'soft', at: 0.9, mode: 'fade', dur: 0.55, lh: 1.4 });
  P.noirWave(680, 500, 560, 105, { bars: 36, gap: 5, color: 'blue', at: 1.0, dur: 0.7 });
  P.path('M928 660 Q928 640 952 640 Q976 640 976 660 L976 724 Q976 748 952 748 Q928 748 928 724 Z', { color: 'orange', sw: 1.5, at: 1.3, dur: 0.6 });
  P.line(938, 674, 966, 674, { color: 'orange', sw: 1, at: 1.5, dur: 0.3, pen: false });
  P.line(938, 690, 966, 690, { color: 'orange', sw: 1, at: 1.56, dur: 0.3, pen: false });
  P.line(938, 706, 966, 706, { color: 'orange', sw: 1, at: 1.62, dur: 0.3, pen: false });
  P.line(952, 748, 952, 790, { color: 'orange', sw: 1.2, at: 1.7, dur: 0.3, pen: false });
  P.line(920, 790, 984, 790, { color: 'orange', sw: 1.2, at: 1.8, dur: 0.3, pen: false });
  P.noirLabel('李安 · 情感修复', 960, 830, { size: 13, color: 'muted', at: 1.6, track: '0.2em' });
  P.noirLabel('STAY / TOGETHER', 1650, 140, { size: 11, color: 'faint', at: 0.8 });
});
