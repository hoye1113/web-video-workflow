/* p22 · 找到根源，才能避开旧坑
 * 图：../scene-library/p22-找到根源-才能避开曾经的坑.png（处境图库，图不复制）
 */
ENGINE.visual('p22', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p22-找到根源-才能避开曾经的坑.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
