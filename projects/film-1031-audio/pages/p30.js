/* p30 · 放开手双方都自由
 * 图：../scene-library/p30-解除婚姻关系-双方都自由了.png（处境图库，图不复制）
 * 屏上字：都自由了（只做标签）
 */
ENGINE.visual('p30', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p30-解除婚姻关系-双方都自由了.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("都自由了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
