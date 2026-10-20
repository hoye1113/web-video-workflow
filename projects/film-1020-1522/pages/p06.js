/* p06 · 他要的不是复合，是你心里还有他
 * 图：../scene-library/p25-ruler.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：你的分量（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p25-ruler.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(860, 420, 520, { at: 0.6, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("你的分量", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
