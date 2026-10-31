/* p11 · 认错哀求都是无用功
 * 图：../scene-library/p11-别再把精力放在认错-道歉-哀.png（处境图库，图不复制）
 * 屏上字：别求了（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p11-别再把精力放在认错-道歉-哀.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("别求了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
