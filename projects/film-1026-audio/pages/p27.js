/* p27 · 容易误会的场景提前说
 * 图：../scene-library/p27-容易误会的场景-提前说清楚.png（处境图库，图不复制）
 */
ENGINE.visual('p27', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p27-容易误会的场景-提前说清楚.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
