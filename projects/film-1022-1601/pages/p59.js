/* p59 · 人心会变，分寸靠阅历
 * 图：../scene-library/p59-人心会变-分寸靠阅历.png（处境图库，图不复制）
 */
ENGINE.visual('p59', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p59-人心会变-分寸靠阅历.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
