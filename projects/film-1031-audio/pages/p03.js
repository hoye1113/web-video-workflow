/* p03 · 说出口的多是借口
 * 图：../scene-library/p03-对方说出口的理由-多半只是表.png（处境图库，图不复制）
 * 屏上字：只是借口（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-对方说出口的理由-多半只是表.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("只是借口", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
