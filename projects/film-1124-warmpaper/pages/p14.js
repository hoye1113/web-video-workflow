/* p14 · 从来不是单方面的一厢情愿
 * 图：../scene-library/f1124-p14.png（处境图库，图不复制）
 * 屏上字：依恋人格（只做标签）
 */
ENGINE.visual('p14', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p14.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("依恋人格", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
