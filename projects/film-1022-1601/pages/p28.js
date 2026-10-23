/* p28 · 值得信任，就不用疑神疑鬼
 * 图：../scene-library/p28-值得信任就不用疑神疑鬼.png（处境图库，图不复制）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p28-值得信任就不用疑神疑鬼.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
