/* p30 · 和那点必须证明自己没错的自我满足
 * 图：../scene-library/f1109-p30-43.png（处境图库，图不复制）
 */
ENGINE.visual('p30', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p30-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
