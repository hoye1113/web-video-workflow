/* p17 · 大多数背叛的男人，不是在享受，而是在撕裂
 * 图：../scene-library/male-01-paper-fold.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：不是在享受（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/male-01-paper-fold.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1900, 180, 700, { at: 0.6, kind: 'window', k: (lt) => PV.clamp((lt - 0.5) / 2) });
  P.text("不是在享受", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
