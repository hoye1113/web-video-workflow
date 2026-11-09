/* p27 · 这其实是一种自我开脱
 * 图：../scene-library/f1109-p27-43.png（处境图库，图不复制）
 * 屏上字：自我开脱（只做标签）
 */
ENGINE.visual('p27', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1109-p27-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("自我开脱", { x: 250, y: 230, size: 50, align: 'l', color: '#F7F3EA', at: 1.2 });
});
