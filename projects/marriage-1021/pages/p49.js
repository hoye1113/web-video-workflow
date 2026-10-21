/* p49 · 妻子这端最危险的，是失去判断只剩情绪
 * 图：../scene-library/p49-妻子这端最危险的-是失去判断.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：只剩情绪（只做标签）
 */
ENGINE.visual('p49', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p49-妻子这端最危险的-是失去判断.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(560, 420, 560, { at: 0.6, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("只剩情绪", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
