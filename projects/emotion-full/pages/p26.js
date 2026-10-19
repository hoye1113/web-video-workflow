/* p26 · 真正的修复，是重新建立规则和边界
 * 图：../scene-library/p26-smooth-refold.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：重建边界（只做标签）
 */
ENGINE.visual('p26', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p26-smooth-refold.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 300, 780, { at: 0.5, kind: 'window', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("重建边界", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
