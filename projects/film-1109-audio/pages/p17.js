/* p17 · 她拿着你这里的安稳给自己兜底
 * 图：../scene-library/f1109-p17-43.png（处境图库，图不复制）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p17-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
