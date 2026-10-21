/* p05 · 你把选择权让出去，就再也没人替你选
 * 图：../scene-library/p05-你把选择权让出去-就再也没人.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：他们不会再问（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-你把选择权让出去-就再也没人.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 280, 760, { at: 0.5, kind: 'lamp', k: (lt) => PV.clamp(lt / 2) });
  P.text("他们不会再问", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
