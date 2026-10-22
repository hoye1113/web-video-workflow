/* p12 · 冷对冷，用魔法打败魔法
 * 图：../scene-library/p12-第三句-她逃避问题-还把责任.png（处境图库，图不复制）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p12-第三句-她逃避问题-还把责任.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
