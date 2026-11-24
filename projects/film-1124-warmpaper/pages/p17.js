/* p17 · 焦虑与回避最初爱上的
 * 图：../scene-library/f1124-p17.png（处境图库，图不复制）
 * 屏上字：完美爱人（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p17.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("完美爱人", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
