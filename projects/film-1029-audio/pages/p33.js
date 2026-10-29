/* p33 · 暧昧期好感度最高
 * 图：../scene-library/p33-暧昧相处-好感度最高的时候.png（处境图库，图不复制）
 */
ENGINE.visual('p33', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p33-暧昧相处-好感度最高的时候.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
