/* p03 · 回不到以前，是一辈子的痛
 * 图：../scene-library/p03-可一旦有了第三者-就回不到以.png（处境图库，图不复制）
 * 屏上字：一辈子的痛（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-可一旦有了第三者-就回不到以.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("一辈子的痛", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
