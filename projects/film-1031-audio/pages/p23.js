/* p23 · 只是成长经历不同
 * 图：../scene-library/p23-没有权威的对错标准-只是从小.png（处境图库，图不复制）
 * 屏上字：成长不同（只做标签）
 */
ENGINE.visual('p23', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p23-没有权威的对错标准-只是从小.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("成长不同", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
