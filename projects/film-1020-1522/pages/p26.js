/* p26 · 冷不是拒绝，肯回来才是答案
 * 图：../scene-library/p15-night-door.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：门没关（只做标签）
 */
ENGINE.visual('p26', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p15-night-door.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 320, 460, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.6) });
  P.text("门没关", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
