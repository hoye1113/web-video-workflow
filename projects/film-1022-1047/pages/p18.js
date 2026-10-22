/* p18 · 把精力放回自己身上，你就掌握主动权
 * 图：../scene-library/p18-把精力放回自己身上-就掌握主.png（处境图库，图不复制）
 * 屏上字：主动权（只做标签）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p18-把精力放回自己身上-就掌握主.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("主动权", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
