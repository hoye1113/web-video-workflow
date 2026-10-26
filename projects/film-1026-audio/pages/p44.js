/* p44 · 反复和怀疑都是正常的
 * 图：../scene-library/p44-过程中会有反复-怀疑-甚至想.png（处境图库，图不复制）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p44-过程中会有反复-怀疑-甚至想.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
