/* p26 · 继续过，真正的考验才开始
 * 图：../scene-library/p26-选择继续过-就要做好准备-真.png（处境图库，图不复制）
 * 屏上字：考验才开始（只做标签）
 */
ENGINE.visual('p26', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p26-选择继续过-就要做好准备-真.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("考验才开始", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
