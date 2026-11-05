/* p54 · 该表达时表达，该倾听时倾听
 * 图：../scene-library/p54-该表达时讲清事实和感受-该倾-43.png（处境图库，图不复制）
 * 屏上字：表达与倾听（只做标签）
 */
ENGINE.visual('p54', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p54-该表达时讲清事实和感受-该倾-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("表达与倾听", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
