/* p38 · 你要对方继续和你留在现有婚姻里
 * 图：../scene-library/f1031-p38.png（处境图库，图不复制）
 */
ENGINE.visual('p38', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p38.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
