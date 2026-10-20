/* p05 · 你真不找，他反而开始怀疑自己
 * 图：../scene-library/male-02-phone-glow.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：他先慌了（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/male-02-phone-glow.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1000, 430, 420, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.4) });
  P.text("他先慌了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
