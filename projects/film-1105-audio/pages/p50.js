/* p50 · 暂停不是消失
 * 图：../scene-library/p50-暂停不是消失-更不是用不回应-43.png（处境图库，图不复制）
 * 屏上字：暂停不是消失（只做标签）
 */
ENGINE.visual('p50', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p50-暂停不是消失-更不是用不回应-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("暂停不是消失", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
