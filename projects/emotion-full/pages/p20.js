/* p20 · 婚外关系更像一种短期的情绪麻醉
 * 图：../scene-library/p20-anesthesia.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：短期麻醉（只做标签）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p20-anesthesia.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.3, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 700, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("短期麻醉", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
