/* p16 · 他会反复追问那半小时
 * 图：../scene-library/p16-他会突然追问那半小时去了哪.png（处境图库，图不复制）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p16-他会突然追问那半小时去了哪.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
