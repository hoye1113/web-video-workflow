/* p55 · 不是两个完美的人相遇
 * 图：../scene-library/f1111-p55-43.png（处境图库，图不复制）
 * 屏上字：两个普通人（只做标签）
 */
ENGINE.visual('p55', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1111-p55-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [1.96, 1], [2.51, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("两个普通人", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
