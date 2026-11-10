/* p15 · 他的身体和心理都产生了排斥反应
 * 图：../scene-library/f1110-p15-43.png（处境图库，图不复制）
 */
ENGINE.visual('p15', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p15-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
