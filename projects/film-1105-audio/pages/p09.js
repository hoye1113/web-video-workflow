/* p09 · 追着蛇跑，自己先倒下
 * 图：../scene-library/p09-举着棍子追蛇-蛇没追到自己先-43.png（处境图库，图不复制）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p09-举着棍子追蛇-蛇没追到自己先-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
