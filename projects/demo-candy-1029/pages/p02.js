/* p02 · 她说，好东西要留到最后，才不算浪费
 * 图：../scene-library/p02-candy-tin-v2.png（处境图库，图不复制）
 */
ENGINE.visual('p02', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p02-candy-tin-v2.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
