/* p39 · 用从前的好抵现在的伤，是否定他
 * 图：../scene-library/p39-拿从前的好抵现在的伤-就是否.png（处境图库，图不复制）
 */
ENGINE.visual('p39', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p39-拿从前的好抵现在的伤-就是否.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
