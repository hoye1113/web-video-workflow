/* p40 · 不隐瞒，也不单独相处
 * 图：../scene-library/p40-不单独相处-也不隐瞒重要社交.png（处境图库，图不复制）
 */
ENGINE.visual('p40', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p40-不单独相处-也不隐瞒重要社交.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
