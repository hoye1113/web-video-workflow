/* p40 · 她在暗处看着
 * 图：../scene-library/p40-她在暗处看着-你只管用事实改.png（处境图库，图不复制）
 * 屏上字：她在暗处（只做标签）
 */
ENGINE.visual('p40', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p40-她在暗处看着-你只管用事实改.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.24, dur: 1.52 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("她在暗处", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
