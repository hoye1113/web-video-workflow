/* p07 · 那就是伴侣会患上背叛后遗症
 * 图：../scene-library/f1110-p07-43.png（处境图库，图不复制）
 * 屏上字：背叛后遗症（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1110-p07-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [1.52, 1], [2.07, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("背叛后遗症", { x: 250, y: 230, size: 50, align: 'l', color: '#F7F3EA', at: 1.2 });
});
