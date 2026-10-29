/* p43 · 过于尊重就是没底线
 * 图：../scene-library/p43-过于尊重-就是没有底线.png（处境图库，图不复制）
 * 屏上字：过于尊重（只做标签）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p43-过于尊重-就是没有底线.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("过于尊重", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
