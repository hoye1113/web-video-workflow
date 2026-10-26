/* p47 · 什么样的相处能长久
 * 图：../scene-library/p47-更清楚什么样的相处能让关系长.png（处境图库，图不复制）
 */
ENGINE.visual('p47', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p47-更清楚什么样的相处能让关系长.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
