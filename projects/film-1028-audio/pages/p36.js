/* p36 · 心软一次，只是暂缓
 * 图：../scene-library/p36-她一心软-你只是暂时不难受了.png（处境图库，图不复制）
 */
ENGINE.visual('p36', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p36-她一心软-你只是暂时不难受了.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
