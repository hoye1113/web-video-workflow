/* p44 · 打持久战，拔刺会连着撕肉
 * 图：../scene-library/p44-拔刺会连着撕下一块肉-要有打.png（处境图库，图不复制）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p44-拔刺会连着撕下一块肉-要有打.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
