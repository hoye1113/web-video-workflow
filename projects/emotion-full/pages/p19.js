/* p19 · 不是谁更爱谁，而是他在需求之间失控
 * 图：../scene-library/p18-two-doors.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：不是谁更爱谁（只做标签）
 */
ENGINE.visual('p19', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p18-two-doors.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(300, 640, 560, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("不是谁更爱谁", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
