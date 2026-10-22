/* p10 · 以退为进，抢占道德制高点
 * 图：../scene-library/p10-单方面宣布结束-是降维打击.png（处境图库，图不复制）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p10-单方面宣布结束-是降维打击.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
