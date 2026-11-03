/* p07 · 没有第三个人，根基就还在
 * 图：../scene-library/p07-没有第三个人动摇根基-矛盾就.png（处境图库，图不复制）
 * 屏上字：门还关着（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p07-没有第三个人动摇根基-矛盾就.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("门还关着", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
