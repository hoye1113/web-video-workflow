/* p34 · 你的办法比她还差
 * 图：../scene-library/p34-你的办法比她自己试过的还差.png（处境图库，图不复制）
 * 屏上字：比她还差（只做标签）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p34-你的办法比她自己试过的还差.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("比她还差", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
