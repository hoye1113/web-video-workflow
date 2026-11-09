/* p41 · 给你更有针对性的分析和思路
 * 图：../scene-library/f1109-p41-43.png（处境图库，图不复制）
 */
ENGINE.visual('p41', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p41-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

});
