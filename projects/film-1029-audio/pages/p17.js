/* p17 · 她被打动，但恋爱才开始
 * 图：../scene-library/p17-她被打动-可恋爱才刚开始.png（处境图库，图不复制）
 * 屏上字：一时心动（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p17-她被打动-可恋爱才刚开始.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("一时心动", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
