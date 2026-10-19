/* p24 · 妻子这端最危险的，不是哭，而是只剩情绪
 * 图：../scene-library/p24-clench.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：只剩情绪（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p24-clench.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1500, 500, 620, { at: 0.6, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.6) / 1.6) });
  P.text("只剩情绪", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
