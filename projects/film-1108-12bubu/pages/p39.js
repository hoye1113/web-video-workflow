/* p39 · 是真心实意地接纳你和原配的孩子
 * 图：../scene-library/f1108b-p39.png（处境图库，图不复制）
 */
ENGINE.visual('p39', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1108b-p39.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
