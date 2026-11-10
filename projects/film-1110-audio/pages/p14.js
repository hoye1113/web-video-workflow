/* p14 · 一抱他他就会不自觉地想起
 * 图：../scene-library/f1110-p14-43.png（处境图库，图不复制）
 */
ENGINE.visual('p14', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1110-p14-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
