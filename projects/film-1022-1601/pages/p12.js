/* p12 · 不管，能行吗
 * 图：../scene-library/p12-不管-能行吗.png（处境图库，图不复制）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p12-不管-能行吗.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
