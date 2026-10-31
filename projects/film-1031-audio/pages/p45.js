/* p45 · 一个慌乱局促
 * 图：../scene-library/f1031-p45.png（处境图库，图不复制）
 */
ENGINE.visual('p45', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p45.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.2 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
