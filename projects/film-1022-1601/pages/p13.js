/* p13 · 管得住的其实很少
 * 图：../scene-library/p13-管得住的其实很少.png（处境图库，图不复制）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p13-管得住的其实很少.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
