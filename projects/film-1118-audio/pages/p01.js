/* p01 · 彻底失望离开的女生
 * 图：../scene-library/f1118-p01.png（处境图库，图不复制）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1118-p01.png', {
    at: 0,
    reveal: { from: 0.9, to: 1, at: 0, dur: 0.4 },
    cam: [[0, 1], [0.9, 1.035], [T * 0.55, 1.035], [T * 0.55 + 1.0, 1.085], [T, 1.085]].map(([t, z]) => ({ t, z })),
  });

});
