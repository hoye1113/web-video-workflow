/* p35 · 像照顾受伤的人，别逼他立刻好
 * 图：../scene-library/p35-像照顾受伤的病人-别逼他立刻.png（处境图库，图不复制）
 */
ENGINE.visual('p35', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p35-像照顾受伤的病人-别逼他立刻.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
