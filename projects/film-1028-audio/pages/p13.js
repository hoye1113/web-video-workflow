/* p13 · 婚龄多长，试过多少次
 * 图：../scene-library/p13-婚龄多长-她就在心里试过多少.png（处境图库，图不复制）
 * 屏上字：试过太多次（只做标签）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p13-婚龄多长-她就在心里试过多少.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("试过太多次", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
