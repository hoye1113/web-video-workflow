/* p17 · 被伤到再也不敢相信人
 * 图：../scene-library/p17-被伤到觉得自己像个笑话-再难.png（处境图库，图不复制）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p17-被伤到觉得自己像个笑话-再难.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
