/* p24 · 在彼此的动物性爱恋消失后
 * 图：../scene-library/f1031-p24.png（处境图库，图不复制）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p24.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.2 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

});
