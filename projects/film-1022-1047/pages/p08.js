/* p08 · 不带情绪的放弃更让人失控
 * 图：../scene-library/p08-第二句-她明知故犯挑战底线.png（处境图库，图不复制）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p08-第二句-她明知故犯挑战底线.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
