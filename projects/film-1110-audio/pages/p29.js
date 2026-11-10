/* p29 · 这个世界上最珍贵
 * 图：../scene-library/f1110-p29-43.png（处境图库，图不复制）
 * 屏上字：最珍贵（只做标签）
 */
ENGINE.visual('p29', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p29-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [2.45, 1], [3, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("最珍贵", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
