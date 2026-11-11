/* p05 · 很大概率是你亲手把对方变成了那个样子
 * 图：../scene-library/f1111-p05-43.png（处境图库，图不复制）
 * 屏上字：你亲手塑造成（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1111-p05-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("你亲手塑造成", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
