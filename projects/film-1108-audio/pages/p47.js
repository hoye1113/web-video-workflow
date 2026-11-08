/* p47 · 多花点功夫
 * 图：../scene-library/f1108-p47-43.png（处境图库，图不复制）
 * 屏上字：一起修（只做标签）
 */
ENGINE.visual('p47', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1108-p47-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("一起修", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
