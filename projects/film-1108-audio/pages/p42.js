/* p42 · 等到后来他们自己有了小孩之后
 * 图：../scene-library/f1108-p42-43.png（处境图库，图不复制）
 */
ENGINE.visual('p42', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1108-p42-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
