/* p02 · 打过架，也能和好
 * 图：../scene-library/p02-就算打过架-没有第三者也能和.png（处境图库，图不复制）
 * 屏上字：也能和好（只做标签）
 */
ENGINE.visual('p02', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p02-就算打过架-没有第三者也能和.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("也能和好", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
