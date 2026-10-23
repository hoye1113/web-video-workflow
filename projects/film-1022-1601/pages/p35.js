/* p35 · 总觉得对方缺人推一把
 * 图：../scene-library/p35-总觉得对方缺人推一把.png（处境图库，图不复制）
 */
ENGINE.visual('p35', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p35-总觉得对方缺人推一把.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
