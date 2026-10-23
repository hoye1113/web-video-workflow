/* p54 · 珍惜你的人，会更看重婚姻
 * 图：../scene-library/p54-珍惜你的人会更看重婚姻.png（处境图库，图不复制）
 */
ENGINE.visual('p54', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p54-珍惜你的人会更看重婚姻.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
