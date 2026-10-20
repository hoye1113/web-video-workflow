/* p25 · 第三种怎么办：先停一停
 * 图：../scene-library/p26-smooth-refold.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：先停一停（只做标签）
 */
ENGINE.visual('p25', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p26-smooth-refold.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1020, 420, 700, { at: 0.5, kind: 'window', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("先停一停", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
