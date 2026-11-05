/* p60 · 再说感受，把问题拆小
 * 图：../scene-library/p60-再说自己的感受和希望-把问题-43.png（处境图库，图不复制）
 */
ENGINE.visual('p60', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p60-再说自己的感受和希望-把问题-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
