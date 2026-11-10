/* p32 · 我们最后做个总结
 * 图：../scene-library/f1110-p32-43.png（处境图库，图不复制）
 * 屏上字：危机是重建（只做标签）
 */
ENGINE.visual('p32', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p32-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("危机是重建", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
