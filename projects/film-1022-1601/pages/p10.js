/* p10 · 第一件：不管社交圈
 * 图：../scene-library/p10-第一件-不管社交圈.png（处境图库，图不复制）
 * 屏上字：社交圈（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p10-第一件-不管社交圈.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("社交圈", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
