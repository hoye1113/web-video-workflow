/* p18 · 一边要家庭，一边要刺激
 * 图：../scene-library/p18-two-doors.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：家里、外面（只做标签）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p18-two-doors.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(300, 640, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.light(1620, 640, 560, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.5) });
  P.text("家里", { x: 260, y: 230, size: 40, align: 'l', color: 'orange', at: 1.6 });
  P.text("外面", { x: 1500, y: 230, size: 40, align: 'l', color: 'blue', at: 2.4 });
});
