/* p38 · 别总提我以前对你多好
 * 图：../scene-library/p38-也别总提-我以前对你有多好-.png（处境图库，图不复制）
 */
ENGINE.visual('p38', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p38-也别总提-我以前对你有多好-.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
