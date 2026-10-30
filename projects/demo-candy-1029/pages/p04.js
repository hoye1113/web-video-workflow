/* p04 · 那天，她把糖放进嘴里，笑了
 * 图：../scene-library/p04-candy-smile-close.png（处境图库，图不复制）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-candy-smile-close.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
