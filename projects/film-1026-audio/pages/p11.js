/* p11 · 真心悔改，还是只想过关
 * 图：../scene-library/p11-犯错者要分清真心悔改还是只想.png（处境图库，图不复制）
 * 屏上字：真心还是过关（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p11-犯错者要分清真心悔改还是只想.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("真心还是过关", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
