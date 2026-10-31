/* p06 · 对方本人往往也是无能为力的
 * 图：../scene-library/f1031-p06.png（处境图库，图不复制）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1031-p06.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
