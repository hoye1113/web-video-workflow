/* p62 · 怎么去爱一个人了
 * 图：../scene-library/f1118-p62.png（处境图库，图不复制）
 */
ENGINE.visual('p62', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1118-p62.png', {
    at: 0,
    reveal: { from: 0.6, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
