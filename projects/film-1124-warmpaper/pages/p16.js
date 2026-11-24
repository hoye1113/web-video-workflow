/* p16 · 不如稳定关系后
 * 图：../scene-library/f1124-p16.png（处境图库，图不复制）
 * 屏上字：真实本性（只做标签）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p16.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("真实本性", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
