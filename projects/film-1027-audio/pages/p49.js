/* p49 · 日子要往前走，伤口会结痂
 * 图：../scene-library/p49-日子总要往前走-伤口终会结痂.png（处境图库，图不复制）
 * 屏上字：伤口会结痂（只做标签）
 */
ENGINE.visual('p49', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p49-日子总要往前走-伤口终会结痂.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("伤口会结痂", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
