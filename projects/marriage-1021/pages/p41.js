/* p41 · 撕裂感才是持续消耗他的东西
 * 图：../scene-library/p41-撕裂感才是持续消耗他的东西.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：持续消耗（只做标签）
 */
ENGINE.visual('p41', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p41-撕裂感才是持续消耗他的东西.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 470, 430, { at: 0.8, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.8) / 1.5) });
  P.text("持续消耗", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
