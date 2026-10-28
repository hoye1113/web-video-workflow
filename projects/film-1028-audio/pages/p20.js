/* p20 · 愧疚她不接
 * 图：../scene-library/p20-你说-都是我自己想改--那份.png（处境图库，图不复制）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p20-你说-都是我自己想改--那份.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
