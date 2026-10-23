/* p47 · 对方成了你的天气预报
 * 图：../scene-library/p47-对方成了天气预报.png（处境图库，图不复制）
 */
ENGINE.visual('p47', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p47-对方成了天气预报.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
