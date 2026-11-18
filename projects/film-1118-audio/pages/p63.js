/* p63 · 就是你们重建
 * 图：../scene-library/f1118-p63.png（处境图库，图不复制）
 */
ENGINE.visual('p63', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1118-p63.png', {
    at: 0,
    reveal: { from: 0.6, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1.03], [T, 1.03]].map(([t, z]) => ({ t, z })),
  });

});
