/* p12 · 其实回避从来都没有外表
 * 图：../scene-library/f1124-p12.png（处境图库，图不复制）
 * 屏上字：故作冷漠（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p12.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.24, dur: 1.6 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("故作冷漠", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
