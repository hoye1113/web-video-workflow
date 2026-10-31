/* p14 · 不爱了呼吸都是错
 * 图：../scene-library/p14-当对方不爱了-你连呼吸都可能.png（处境图库，图不复制）
 * 屏上字：呼吸都是错（只做标签）
 */
ENGINE.visual('p14', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p14-当对方不爱了-你连呼吸都可能.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("呼吸都是错", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
