/* p16 · 他开始怀疑这段婚姻还能不能继续
 * 图：../scene-library/p16-他开始怀疑这段婚姻还能不能继.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：还能继续吗（只做标签）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p16-他开始怀疑这段婚姻还能不能继.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(620, 640, 560, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("还能继续吗", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
