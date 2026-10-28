/* p24 · 凭什么都要遂你意
 * 图：../scene-library/p24-你觉得她自私-凭什么都要遂你.png（处境图库，图不复制）
 * 屏上字：凭什么（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p24-你觉得她自私-凭什么都要遂你.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.24, dur: 1.52 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("凭什么", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
