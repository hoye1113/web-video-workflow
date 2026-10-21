/* p11 · 不是他们忽略你，是你教他们忽略你
 * 图：../scene-library/p11-不是他们忽略你-是你教他们忽.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：你教他们忽略你（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p11-不是他们忽略你-是你教他们忽.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(520, 520, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.light(1420, 520, 560, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.5) });
  P.text("你教他们忽略你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
