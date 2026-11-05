/* p41 · 重新分配，也重新成长
 * 图：../scene-library/p41-发展兴趣-也重新分配家务和责-43.png（处境图库，图不复制）
 * 屏上字：重新分配（只做标签）
 */
ENGINE.visual('p41', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p41-发展兴趣-也重新分配家务和责-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("重新分配", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
