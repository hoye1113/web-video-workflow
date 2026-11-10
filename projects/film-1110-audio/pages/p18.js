/* p18 · 去陪他一点点的
 * 图：../scene-library/f1110-p18-43.png（处境图库，图不复制）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p18-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
