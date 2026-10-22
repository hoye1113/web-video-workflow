/* p03 · 你说一句，他这辈子再不敢怠慢你
 * 图：../scene-library/p03-不是颜值-是敢说这三句话.png（处境图库，图不复制）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-不是颜值-是敢说这三句话.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
