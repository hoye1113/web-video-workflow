/* p26 · 脓血排干净，伤口才会愈合
 * 图：../scene-library/p26-脓血排干净-伤口才有可能愈合.png（处境图库，图不复制）
 */
ENGINE.visual('p26', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p26-脓血排干净-伤口才有可能愈合.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
