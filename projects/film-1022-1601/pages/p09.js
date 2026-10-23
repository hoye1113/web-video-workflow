/* p09 · 四件事，让感情变好
 * 图：../scene-library/p09-四件事让感情变好.png（处境图库，图不复制）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-四件事让感情变好.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
