/* p22 · 第一种怎么办：稳住，别追
 * 图：../scene-library/p24-clench.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：先稳住（只做标签）
 */
ENGINE.visual('p22', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p24-clench.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 430, 540, { at: 0.6, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("先稳住", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
