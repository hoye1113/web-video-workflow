/* p44 · 对方脸色不对，你心里打鼓
 * 图：../scene-library/p44-对方脸色不对你就打鼓.png（处境图库，图不复制）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p44-对方脸色不对你就打鼓.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
