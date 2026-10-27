/* p28 · 承认这对他不公平
 * 图：../scene-library/p28-承认这对他不公平-信任要修好.png（处境图库，图不复制）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p28-承认这对他不公平-信任要修好.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
