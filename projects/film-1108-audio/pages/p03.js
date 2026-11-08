/* p03 · 这事就算尘埃落定了
 * 图：../scene-library/f1108-p03-43.png（处境图库，图不复制）
 * 屏上字：家变了（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1108-p03-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("家变了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
