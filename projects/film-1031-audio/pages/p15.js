/* p15 · 即便你把自己完善成大众眼中的好人
 * 图：../scene-library/f1031-p15.png（处境图库，图不复制）
 */
ENGINE.visual('p15', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p15.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
