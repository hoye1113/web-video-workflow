/* p56 · 一杯奶茶立刻送到楼下
 * 图：../scene-library/p56-一杯奶茶-立刻送到楼下.png（处境图库，图不复制）
 */
ENGINE.visual('p56', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p56-一杯奶茶-立刻送到楼下.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
