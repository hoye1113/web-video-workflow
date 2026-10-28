/* p06 · 旧账堆成了没救
 * 图：../scene-library/p06-旧经历和旧认知堆在一起-她只.png（处境图库，图不复制）
 * 屏上字：旧账太多（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-旧经历和旧认知堆在一起-她只.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("旧账太多", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
