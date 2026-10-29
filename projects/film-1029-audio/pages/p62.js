/* p62 · 这不是算计，是平衡
 * 图：../scene-library/p62-这不是算计-是让关系平衡.png（处境图库，图不复制）
 */
ENGINE.visual('p62', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p62-这不是算计-是让关系平衡.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
