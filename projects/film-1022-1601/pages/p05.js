/* p05 · 像雷达一样扫描
 * 图：../scene-library/p05-整天像雷达一样扫描.png（处境图库，图不复制）
 * 屏上字：全天候雷达（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-整天像雷达一样扫描.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("全天候雷达", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
