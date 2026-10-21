/* p17 · 第三件：允许自己被照顾
 * 图：../scene-library/p17-第三件-允许自己被照顾.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：允许被照顾（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p17-第三件-允许自己被照顾.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 380, 640, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("允许被照顾", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
