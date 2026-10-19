/* p03 · 三个真实案例，比任何道理都更能改变理解
 * 图：../scene-library/p03-cases.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：挑出三个（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-cases.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 820, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("挑出三个", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
