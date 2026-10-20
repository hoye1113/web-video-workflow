/* p11 · 下次吵架，先别急着说对不起
 * 图：../scene-library/p11-下次吵架-先别急着说对不起.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：先别道歉（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p11-下次吵架-先别急着说对不起.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 400, 520, { at: 0.4, kind: 'window', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("先别道歉", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
