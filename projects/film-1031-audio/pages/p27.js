/* p27 · 合乎社会标准的
 * 图：../scene-library/f1031-p27.png（处境图库，图不复制）
 * 屏上字：满大街（只做标签）
 */
ENGINE.visual('p27', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1031-p27.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("满大街", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
