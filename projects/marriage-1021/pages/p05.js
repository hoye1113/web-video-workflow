/* p05 · 上百个男性咨询案例里，挑出三个最典型的
 * 图：../scene-library/p05-上百个男性咨询案例里-挑出三.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：挑出三个（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-上百个男性咨询案例里-挑出三.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 820, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("挑出三个", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
