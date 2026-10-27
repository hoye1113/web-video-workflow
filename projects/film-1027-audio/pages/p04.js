/* p04 · 一会儿想继续，一会儿想离婚
 * 图：../scene-library/p04-情绪来回拉扯-一会儿想继续一.png（处境图库，图不复制）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p04-情绪来回拉扯-一会儿想继续一.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
