/* p35 · 那些希望被接住的时刻
 * 图：../scene-library/p35-希望对方立刻安慰-希望对方主-43.png（处境图库，图不复制）
 */
ENGINE.visual('p35', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p35-希望对方立刻安慰-希望对方主-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
