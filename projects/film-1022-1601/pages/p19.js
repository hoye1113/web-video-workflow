/* p19 · 辜负了，是对方的问题
 * 图：../scene-library/p19-辜负了是对方的问题.png（处境图库，图不复制）
 */
ENGINE.visual('p19', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p19-辜负了是对方的问题.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
