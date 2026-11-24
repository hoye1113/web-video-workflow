/* p21 · 再决定是否继续坚持
 * 图：../scene-library/f1124-p21.png（处境图库，图不复制）
 * 屏上字：再决定（只做标签）
 */
ENGINE.visual('p21', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p21.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.03], [T, 1.03]].map(([t, z]) => ({ t, z })),
  });

  P.text("再决定", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
