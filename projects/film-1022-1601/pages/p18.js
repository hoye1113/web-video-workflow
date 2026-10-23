/* p18 · 放手，是相信自己的选择
 * 图：../scene-library/p18-放手是相信自己的选择.png（处境图库，图不复制）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p18-放手是相信自己的选择.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
