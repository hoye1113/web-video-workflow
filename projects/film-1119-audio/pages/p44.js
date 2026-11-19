/* p44 · 则会让你一直活在焦虑和痛苦中
 * 图：../scene-library/f1119-p44.png（处境图库，图不复制）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1119-p44.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
