/* p06 · 从社会认知心理学角度看
 * 图：../scene-library/f1109-p06-43.png（处境图库，图不复制）
 * 屏上字：成本与收益（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1109-p06-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("成本与收益", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
