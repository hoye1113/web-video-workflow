/* p04 · 你一定要跟他去促膝长谈一次
 * 图：../scene-library/f1110-p04-43.png（处境图库，图不复制）
 * 屏上字：促膝长谈（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1110-p04-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("促膝长谈", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
