/* p24 · 这真的不是空穴来风
 * 图：../scene-library/f1110-p24-43.png（处境图库，图不复制）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1110-p24-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
