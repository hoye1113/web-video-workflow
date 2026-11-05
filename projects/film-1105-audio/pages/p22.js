/* p22 · 一条晚回的消息
 * 图：../scene-library/p22-一条晚回的消息-让人感到被忽-43.png（处境图库，图不复制）
 * 屏上字：晚回的消息（只做标签）
 */
ENGINE.visual('p22', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p22-一条晚回的消息-让人感到被忽-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("晚回的消息", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
