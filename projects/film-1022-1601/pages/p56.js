/* p56 · 体谅和信任，是有分量的
 * 图：../scene-library/p56-体谅和信任是有分量的.png（处境图库，图不复制）
 */
ENGINE.visual('p56', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p56-体谅和信任是有分量的.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
