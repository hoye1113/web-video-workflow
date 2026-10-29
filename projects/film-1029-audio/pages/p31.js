/* p31 · 从聊天走到自然相处
 * 图：../scene-library/p31-不再排斥沟通-就自然走近.png（处境图库，图不复制）
 * 屏上字：自然而然（只做标签）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p31-不再排斥沟通-就自然走近.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("自然而然", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
