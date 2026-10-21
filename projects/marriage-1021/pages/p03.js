/* p03 · 答案比你想象的更现实
 * 图：../scene-library/p03-答案比你想象的更现实.png（处境图库，图不复制）
 * 光：lamp、window（光就是情绪）
 * 屏上字：更现实（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-答案比你想象的更现实.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(700, 500, 520, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.light(1350, 500, 420, { at: 0.9, kind: 'window', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.4) });
  P.text("更现实", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
