/* p31 · 觉得被侵犯隐私，可平衡是你打破的
 * 图：../scene-library/p31--凭什么要我这样--可平衡是.png（处境图库，图不复制）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p31--凭什么要我这样--可平衡是.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
