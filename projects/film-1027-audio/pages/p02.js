/* p02 · 两个人都想过好，却都过不好
 * 图：../scene-library/p02-遭遇不忠后-两个人都想好好过.png（处境图库，图不复制）
 */
ENGINE.visual('p02', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p02-遭遇不忠后-两个人都想好好过.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
