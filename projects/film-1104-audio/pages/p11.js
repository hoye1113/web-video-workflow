/* p11 · 心凉是婚姻死亡最大的信号
 * 图：../scene-library/f1104-p11.png（处境图库，图不复制）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1104-p11.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
