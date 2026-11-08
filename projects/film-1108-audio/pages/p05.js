/* p05 · 父母离婚对孩子的影响到底有多大
 * 图：../scene-library/f1108-p05-43.png（处境图库，图不复制）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1108-p05-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
