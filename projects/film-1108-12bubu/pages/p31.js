/* p31 · 这种恐惧会一直伴随着他们成长
 * 图：../scene-library/f1108b-p31.png（处境图库，图不复制）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1108b-p31.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
