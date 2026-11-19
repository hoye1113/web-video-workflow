/* p35 · 心态，陷入无端的受迫害妄想中
 * 图：../scene-library/f1119-p35.png（处境图库，图不复制）
 */
ENGINE.visual('p35', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1119-p35.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
