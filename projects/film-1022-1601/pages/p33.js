/* p33 · 第三件：不管未来走向
 * 图：../scene-library/p33-第三件-不管未来走向.png（处境图库，图不复制）
 * 屏上字：人生课题（只做标签）
 */
ENGINE.visual('p33', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p33-第三件-不管未来走向.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("人生课题", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
