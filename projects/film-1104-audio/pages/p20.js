/* p20 · 信任已经碎得捡不回来了
 * 图：../scene-library/f1104-p20.png（处境图库，图不复制）
 * 屏上字：第五种（只做标签）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1104-p20.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("第五种", { x: 250, y: 230, size: 44, align: 'l', color: '#E8DCCB', at: 1.2 });
});
