/* p24 · 想离开人，还是想逃开痛
 * 图：../scene-library/p24-想清楚-是真想离开这个人-还.png（处境图库，图不复制）
 * 屏上字：想逃还是想走（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p24-想清楚-是真想离开这个人-还.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("想逃还是想走", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
