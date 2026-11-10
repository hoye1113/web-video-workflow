/* p12 · 就是你要不断的尝试
 * 图：../scene-library/f1110-p12-43.png（处境图库，图不复制）
 * 屏上字：重建信任（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p12-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.text("重建信任", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
