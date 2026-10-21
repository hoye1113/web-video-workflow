/* p51 · 婚姻里最怕的不是犯错，是犯错后继续内耗
 * 图：../scene-library/p51-婚姻里最怕的不是犯错-是犯错.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：继续内耗（只做标签）
 */
ENGINE.visual('p51', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p51-婚姻里最怕的不是犯错-是犯错.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1150, 300, 420, { at: 0.7, kind: 'window', k: (lt) => PV.clamp((lt - 0.7) / 1.5) });
  P.text("继续内耗", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
