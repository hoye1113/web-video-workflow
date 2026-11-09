/* p21 · 一个真正对亲密关系感到满足的女人
 * 图：../scene-library/f1109-p21-43.png（处境图库，图不复制）
 */
ENGINE.visual('p21', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p21-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
