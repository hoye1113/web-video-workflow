/* p20 · 我想说的是
 * 图：../scene-library/f1110-p20-43.png（处境图库，图不复制）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p20-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
