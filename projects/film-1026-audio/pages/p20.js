/* p20 · 复盘是为了看清关系
 * 图：../scene-library/p20-复盘是为了看清关系哪里出了问.png（处境图库，图不复制）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p20-复盘是为了看清关系哪里出了问.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
