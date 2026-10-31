/* p44 · 得对方想和你在一起
 * 图：../scene-library/p44-只有对方想和你在一起-婚姻才.png（处境图库，图不复制）
 * 屏上字：想在一起（只做标签）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p44-只有对方想和你在一起-婚姻才.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("想在一起", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
