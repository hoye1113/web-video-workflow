/* p10 · 「你先道歉」成了一本看不见的账
 * 图：../scene-library/p10--你先道歉-成了一本看不见的.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：多付一点（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p10--你先道歉-成了一本看不见的.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(560, 480, 520, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("多付一点", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
