/* p04 · 三天没说话，最后是他先敲的门
 * 图：../scene-library/p04-三天没说话-最后是他先敲的门.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：他先敲的门（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p04-三天没说话-最后是他先敲的门.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.82, saturate: 0.85 },
  });

  P.light(960, 170, 620, { at: 0.3, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 1.8) });
  P.text("他先敲的门", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
