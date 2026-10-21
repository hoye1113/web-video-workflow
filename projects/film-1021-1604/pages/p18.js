/* p18 · 先让一个人看见你，就够了
 * 图：../scene-library/p18-先让一个人看见你-就够了.png（处境图库，图不复制）
 * 屏上字：先被看见（只做标签）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p18-先让一个人看见你-就够了.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.9, saturate: 0.88 },
  });

  P.text("先被看见", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
