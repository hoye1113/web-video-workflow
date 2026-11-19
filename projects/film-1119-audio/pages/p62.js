/* p62 · 更谈不上家庭的幸福美满
 * 图：../scene-library/f1119-p62.png（处境图库，图不复制）
 */
ENGINE.visual('p62', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1119-p62.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.1, dur: 1.0 },
    cam: [[0, 1.03], [T, 1.03]].map(([t, z]) => ({ t, z })),
  });

});
