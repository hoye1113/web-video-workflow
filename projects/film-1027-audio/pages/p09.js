/* p09 · 他在提醒自己别受二次伤害
 * 图：../scene-library/p09-他在提醒自己别再受一次伤害.png（处境图库，图不复制）
 * 屏上字：二次伤害（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-他在提醒自己别再受一次伤害.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("二次伤害", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
