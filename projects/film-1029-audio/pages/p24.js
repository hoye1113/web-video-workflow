/* p24 · 太累了，只能放手
 * 图：../scene-library/p24-太累了-最后只能放手.png（处境图库，图不复制）
 * 屏上字：太累了（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p24-太累了-最后只能放手.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("太累了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
