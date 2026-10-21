/* p54 · 让关系重新变得可承受可持续
 * 图：../scene-library/p54-让关系重新变得可承受可持续.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：可承受可持续（只做标签）
 */
ENGINE.visual('p54', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p54-让关系重新变得可承受可持续.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1000, 620, 520, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("可承受可持续", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
