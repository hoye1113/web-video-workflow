/* p07 · 用非常遗憾的语气讲
 * 图：../scene-library/p07-她才会意识到自己哪里需要提升.png（处境图库，图不复制）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p07-她才会意识到自己哪里需要提升.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
