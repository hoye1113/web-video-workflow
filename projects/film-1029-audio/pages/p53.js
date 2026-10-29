/* p53 · 情绪价值让人相处舒服
 * 图：../scene-library/p53-情绪价值高-相处就舒服.png（处境图库，图不复制）
 * 屏上字：相处舒服（只做标签）
 */
ENGINE.visual('p53', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p53-情绪价值高-相处就舒服.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("相处舒服", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
