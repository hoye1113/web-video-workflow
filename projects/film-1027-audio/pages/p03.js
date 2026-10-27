/* p03 · 人回来了，心里的坎还在
 * 图：../scene-library/p03-人已经回头-可心里的坎还是跨.png（处境图库，图不复制）
 * 屏上字：跨不过去（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p03-人已经回头-可心里的坎还是跨.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("跨不过去", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
