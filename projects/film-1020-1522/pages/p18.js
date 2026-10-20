/* p18 · 回避心里有三个软肋：敏感、脆弱、不甘
 * 图：../scene-library/p13-two-lights.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：三个软肋（只做标签）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p13-two-lights.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(420, 620, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.light(1520, 620, 560, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.5) });
  P.text("三个软肋", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
