/* p28 · 记住对方的安全感缺口
 * 图：../scene-library/p28-被伤害者的安全感缺口需要被记.png（处境图库，图不复制）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p28-被伤害者的安全感缺口需要被记.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
