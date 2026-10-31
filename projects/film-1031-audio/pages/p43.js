/* p43 · 你连自己都不放过
 * 图：../scene-library/f1031-p43.png（处境图库，图不复制）
 * 屏上字：狠心（只做标签）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p43.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("狠心", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
