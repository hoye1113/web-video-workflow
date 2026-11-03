/* p23 · 一张证带不走那些记忆
 * 图：../scene-library/p23-离婚只结束法律关系-记忆和习.png（处境图库，图不复制）
 */
ENGINE.visual('p23', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p23-离婚只结束法律关系-记忆和习.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
