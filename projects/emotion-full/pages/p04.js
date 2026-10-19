/* p04 · 暴露往往始于一次意外，他的第一反应是恐惧
 * 图：../scene-library/male-02-phone-glow.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：三年的关系（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/male-02-phone-glow.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.92, saturate: 0.94 },
  });

  P.light(1010, 600, 360, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.2) });
  P.text("三年的关系", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
