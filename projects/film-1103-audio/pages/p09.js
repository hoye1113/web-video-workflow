/* p09 · 第三个人一出现，性质就变了
 * 图：../scene-library/p09-家还在-人也还是我的-第三者.png（处境图库，图不复制）
 * 屏上字：性质变了（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-家还在-人也还是我的-第三者.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("性质变了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
