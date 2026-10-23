/* p01 · 开场：四不管，感情反而更好
 * 图：../scene-library/p01-开场抛出结论.png（处境图库，图不复制）
 * 屏上字：四不管（只做标签）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p01-开场抛出结论.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("四不管", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
