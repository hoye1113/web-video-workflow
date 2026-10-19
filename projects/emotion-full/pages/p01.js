/* p01 · 背叛之后，还会不会爱老婆
 * 图：../scene-library/p01-paper-fold.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：还会爱吗（只做标签）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p01-paper-fold.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(520, 240, 760, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("还会爱吗", { x: 260, y: 240, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
