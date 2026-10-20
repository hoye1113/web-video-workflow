/* p01 · 分开之后他不回消息，是想复合还是想断联
 * 图：../scene-library/female-02-phone-glow.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：不回消息（只做标签）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/female-02-phone-glow.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 430, 420, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.4) });
  P.text("不回消息", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
