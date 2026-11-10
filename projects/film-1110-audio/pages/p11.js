/* p11 · 你要做好准备去接纳伴侣的痛苦
 * 图：../scene-library/f1110-p11-43.png（处境图库，图不复制）
 * 屏上字：接住他的痛苦（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p11-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [1.32, 1], [1.87, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("接住他的痛苦", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
