/* p03 · 很多时候只是表层借口
 * 图：../scene-library/f1031-p03.png（处境图库，图不复制）
 * 屏上字：表层借口（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1031-p03.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("表层借口", { x: 250, y: 230, size: 44, align: 'l', color: '#E8DCCB', at: 1.2 });
});
