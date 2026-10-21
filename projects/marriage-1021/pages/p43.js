/* p43 · 真进了婚姻危机，先看清什么
 * 图：../scene-library/p43-真进了婚姻危机-先看清什么.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：先看清两点（只做标签）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p43-真进了婚姻危机-先看清什么.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.3, dur: 1.4 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.light(980, 520, 460, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("先看清两点", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
