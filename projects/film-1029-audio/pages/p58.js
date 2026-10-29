/* p58 · 心理学上叫沉没成本
 * 图：../scene-library/p58-心理学上-这叫沉没成本.png（处境图库，图不复制）
 * 屏上字：沉没成本（只做标签）
 */
ENGINE.visual('p58', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p58-心理学上-这叫沉没成本.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("沉没成本", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
