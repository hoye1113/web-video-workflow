/* p31 · 想怎么过就怎么过
 * 图：../scene-library/p31-想怎么过就怎么过-不用再迁就.png（处境图库，图不复制）
 * 屏上字：想怎么过（只做标签）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p31-想怎么过就怎么过-不用再迁就.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("想怎么过", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
