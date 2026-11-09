/* p40 · 她现在和对方联系到什么程度
 * 图：../scene-library/f1109-p40-43.png（处境图库，图不复制）
 * 屏上字：先看清处境（只做标签）
 */
ENGINE.visual('p40', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p40-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("先看清处境", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
