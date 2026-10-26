/* p25 · 把透明变成日常小事
 * 图：../scene-library/p25-靠一天一件小事-把透明变成日.png（处境图库，图不复制）
 * 屏上字：一件小事（只做标签）
 */
ENGINE.visual('p25', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p25-靠一天一件小事-把透明变成日.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("一件小事", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
