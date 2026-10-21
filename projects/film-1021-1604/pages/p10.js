/* p10 · 你越能干，别人越不习惯来找你
 * 图：../scene-library/p10-你越能干-别人越不习惯来找你.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：接住就不用你（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p10-你越能干-别人越不习惯来找你.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 300, 700, { at: 0.5, kind: 'lamp', k: (lt) => PV.clamp(lt / 2) });
  P.text("接住就不用你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
