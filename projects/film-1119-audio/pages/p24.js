/* p24 · 接下来你可能会处处猜疑他
 * 图：../scene-library/f1119-p24.png（处境图库，图不复制）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1119-p24.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1.03], [T, 1.03]].map(([t, z]) => ({ t, z })),
  });

});
