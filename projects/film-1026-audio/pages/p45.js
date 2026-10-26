/* p45 · 都没放弃，破碎能重生
 * 图：../scene-library/p45-只要都没放弃-破碎就有可能重.png（处境图库，图不复制）
 * 屏上字：没放弃（只做标签）
 */
ENGINE.visual('p45', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p45-只要都没放弃-破碎就有可能重.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("没放弃", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
