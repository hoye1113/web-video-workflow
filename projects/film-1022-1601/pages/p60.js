/* p60 · 理解了吗？再见
 * 图：../scene-library/p60-理解了吗-再见.png（处境图库，图不复制）
 */
ENGINE.visual('p60', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p60-理解了吗-再见.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
