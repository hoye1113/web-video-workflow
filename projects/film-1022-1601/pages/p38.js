/* p38 · 被推着走的人，很少真心感激
 * 图：../scene-library/p38-被推着走的人很少感激.png（处境图库，图不复制）
 */
ENGINE.visual('p38', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p38-被推着走的人很少感激.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
