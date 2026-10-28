/* p05 · 狠心绝情是撑出来的
 * 图：../scene-library/p05-她表现得狠心绝情-是因为牵扯.png（处境图库，图不复制）
 * 屏上字：狠心背后（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-她表现得狠心绝情-是因为牵扯.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("狠心背后", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
