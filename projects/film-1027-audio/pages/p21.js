/* p21 · 让他感到在家里仍被需要
 * 图：../scene-library/p21-让他感到在家里仍有地位-被需.png（处境图库，图不复制）
 */
ENGINE.visual('p21', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p21-让他感到在家里仍有地位-被需.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
