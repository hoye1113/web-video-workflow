/* p05 · 更常见的是：他没错，却先认了错
 * 图：../scene-library/p05-更常见的是-他没错-却先认了.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：他没错（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-更常见的是-他没错-却先认了.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(380, 420, 520, { at: 0.4, kind: 'window', color: 'blue', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("他没错", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
