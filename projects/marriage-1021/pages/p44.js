/* p44 · 不是向外寻求补偿，而是先看清两个点
 * 图：../scene-library/p44-不是向外寻求补偿-而是先看清.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：解决问题还是逃避（只做标签）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p44-不是向外寻求补偿-而是先看清.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 780, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("解决问题还是逃避", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
