/* p58 · 值得相伴余生的人
 * 图：../scene-library/p58-值得相伴余生的人.png（处境图库，图不复制）
 * 屏上字：相伴余生（只做标签）
 */
ENGINE.visual('p58', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p58-值得相伴余生的人.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("相伴余生", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
