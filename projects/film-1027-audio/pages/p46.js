/* p46 · 这点委屈受不住，刺就一直在
 * 图：../scene-library/p46-这点委屈受不住-刺就永远留在.png（处境图库，图不复制）
 */
ENGINE.visual('p46', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p46-这点委屈受不住-刺就永远留在.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
