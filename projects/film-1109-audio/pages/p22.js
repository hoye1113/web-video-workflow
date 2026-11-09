/* p22 · 可她明明知道你会难受
 * 图：../scene-library/f1109-p22-43.png（处境图库，图不复制）
 * 屏上字：裂口（只做标签）
 */
ENGINE.visual('p22', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p22-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [3.21, 1], [3.76, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("裂口", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
