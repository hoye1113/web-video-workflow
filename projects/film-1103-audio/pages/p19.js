/* p19 · 离婚，还是继续过下去
 * 图：../scene-library/p19-到底该离婚-还是继续过下去.png（处境图库，图不复制）
 * 屏上字：怎么选（只做标签）
 */
ENGINE.visual('p19', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p19-到底该离婚-还是继续过下去.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("怎么选", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
