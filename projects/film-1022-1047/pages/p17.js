/* p17 · 她冷，你更冷；用魔法打败魔法
 * 图：../scene-library/p17-她冷-你更冷-用魔法打败魔法.png（处境图库，图不复制）
 * 屏上字：冷对冷（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p17-她冷-你更冷-用魔法打败魔法.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("冷对冷", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
