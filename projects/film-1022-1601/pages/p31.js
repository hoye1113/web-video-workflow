/* p31 · 对方的选择，说明对方是谁
 * 图：../scene-library/p31-对方的选择说明对方是谁.png（处境图库，图不复制）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p31-对方的选择说明对方是谁.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
