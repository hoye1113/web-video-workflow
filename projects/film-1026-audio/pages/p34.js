/* p34 · 一次失信，可能回到原点
 * 图：../scene-library/p34-一次失信-可能又回到原点.png（处境图库，图不复制）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p34-一次失信-可能又回到原点.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
