/* p29 · 疑神疑鬼，把日子过别扭
 * 图：../scene-library/p29-疑神疑鬼把日子过别扭.png（处境图库，图不复制）
 */
ENGINE.visual('p29', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p29-疑神疑鬼把日子过别扭.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
