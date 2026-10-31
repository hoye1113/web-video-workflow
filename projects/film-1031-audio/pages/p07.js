/* p07 · 爱没了就是没了
 * 图：../scene-library/p07-该被原谅也好-被抛弃也好-爱.png（处境图库，图不复制）
 * 屏上字：没了就是没了（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p07-该被原谅也好-被抛弃也好-爱.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("没了就是没了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
