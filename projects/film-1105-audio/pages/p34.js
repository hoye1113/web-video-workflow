/* p34 · 别把伴侣当成唯一出口
 * 图：../scene-library/p34-别把伴侣变成唯一的情绪出口-43.png（处境图库，图不复制）
 * 屏上字：唯一出口（只做标签）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p34-别把伴侣变成唯一的情绪出口-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("唯一出口", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
