/* p34 · 重新建立连接的机会
 * 图：../scene-library/f1110-p34-43.png（处境图库，图不复制）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p34-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

});
