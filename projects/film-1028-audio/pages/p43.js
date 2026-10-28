/* p43 · 成长后的你会安心
 * 图：../scene-library/p43-成长后的你会安心-她配不上那.png（处境图库，图不复制）
 * 屏上字：你会安心（只做标签）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p43-成长后的你会安心-她配不上那.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("你会安心", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
