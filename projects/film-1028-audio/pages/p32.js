/* p32 · 她确认过留不下幸福
 * 图：../scene-library/p32-她已经反复确认-留下也得不到.png（处境图库，图不复制）
 * 屏上字：她确认过（只做标签）
 */
ENGINE.visual('p32', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p32-她已经反复确认-留下也得不到.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("她确认过", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
