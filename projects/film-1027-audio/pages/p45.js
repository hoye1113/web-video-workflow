/* p45 · 过程难熬，你会怀疑值不值得
 * 图：../scene-library/p45-过程难熬-你会怀疑值不值得.png（处境图库，图不复制）
 */
ENGINE.visual('p45', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p45-过程难熬-你会怀疑值不值得.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
