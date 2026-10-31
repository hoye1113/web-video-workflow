/* p09 · 只要你在婚姻中有一个让对方不舒服的举动
 * 图：../scene-library/f1031-p09.png（处境图库，图不复制）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p09.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

});
