/* p06 · 方式没有对错，难度有差别
 * 图：../scene-library/p06-方式没有对错-难度和收益有差.png（处境图库，图不复制）
 * 屏上字：难度不同（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-方式没有对错-难度和收益有差.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("难度不同", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
