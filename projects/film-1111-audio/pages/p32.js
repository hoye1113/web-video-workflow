/* p32 · 很多人在感情里犯的最大的错误
 * 图：../scene-library/f1111-p32-43.png（处境图库，图不复制）
 * 屏上字：只盯缺点（只做标签）
 */
ENGINE.visual('p32', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1111-p32-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("只盯缺点", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
