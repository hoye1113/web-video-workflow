/* p01 · 犯了错的一方
 * 图：../scene-library/f1110-p01-43.png（处境图库，图不复制）
 * 屏上字：光道歉没用（只做标签）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p01-43.png', {
    at: 0,
    reveal: { from: 0.78, to: 1, at: 0, dur: 0.7 },
    cam: [[0, 1], [0.9, 1.035], [T * 0.55, 1.035], [T * 0.55 + 1.0, 1.085], [T, 1.085]].map(([t, z]) => ({ t, z })),
  });

  P.text("光道歉没用", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 0.25 });
});
