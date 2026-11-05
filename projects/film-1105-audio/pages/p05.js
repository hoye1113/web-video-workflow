/* p05 · 你们可能困在追蛇效应
 * 图：../scene-library/p05-两个人不知不觉困在追蛇效应里-43.png（处境图库，图不复制）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-两个人不知不觉困在追蛇效应里-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
