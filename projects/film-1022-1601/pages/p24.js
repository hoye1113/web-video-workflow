/* p24 · 时间精力花出去，得到什么
 * 图：../scene-library/p24-花出去的精力换来什么.png（处境图库，图不复制）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p24-花出去的精力换来什么.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
