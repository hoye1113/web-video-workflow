/* p57 · 你会把她养成只会接受
 * 图：../scene-library/p57-你会把她养成只会接受的人.png（处境图库，图不复制）
 */
ENGINE.visual('p57', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p57-你会把她养成只会接受的人.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
