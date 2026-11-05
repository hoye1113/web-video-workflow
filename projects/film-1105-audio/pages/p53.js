/* p53 · 管理自己的反应
 * 图：../scene-library/p53-主动权不是控制伴侣-而是管理-43.png（处境图库，图不复制）
 */
ENGINE.visual('p53', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p53-主动权不是控制伴侣-而是管理-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
