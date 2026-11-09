/* p15 · 她做的其实是一种平行评估
 * 图：../scene-library/f1109-p15-43.png（处境图库，图不复制）
 * 屏上字：安全网（只做标签）
 */
ENGINE.visual('p15', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p15-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("安全网", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
