/* p25 · 要不要继续，看对方有没有承担后果
 * 图：../scene-library/p25-ruler.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：看承担后果（只做标签）
 */
ENGINE.visual('p25', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p25-ruler.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(620, 420, 560, { at: 0.6, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("看承担后果", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
