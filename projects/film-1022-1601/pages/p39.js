/* p39 · 有一天，会觉得你跟不上
 * 图：../scene-library/p39-有一天会觉得你跟不上.png（处境图库，图不复制）
 */
ENGINE.visual('p39', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p39-有一天会觉得你跟不上.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
