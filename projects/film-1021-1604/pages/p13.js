/* p13 · 委屈没有说出口，就等于没发生
 * 图：../scene-library/p13-委屈没有说出口-就等于没发生.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：它就不算数了（只做标签）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p13-委屈没有说出口-就等于没发生.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(700, 500, 480, { at: 0.5, kind: 'window', color: 'blue', k: (lt) => PV.clamp(lt / 2) });
  P.text("它就不算数了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
