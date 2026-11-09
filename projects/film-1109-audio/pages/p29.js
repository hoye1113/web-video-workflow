/* p29 · 她维护的未必只是和外面那个男人的关系
 * 图：../scene-library/f1109-p29-43.png（处境图库，图不复制）
 * 屏上字：不是那个男人（只做标签）
 */
ENGINE.visual('p29', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p29-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("不是那个男人", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
