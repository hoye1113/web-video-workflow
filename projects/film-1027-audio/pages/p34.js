/* p34 · 他状态差就别硬碰，也别催和好
 * 图：../scene-library/p34-他状态差就别招惹-好转也别急.png（处境图库，图不复制）
 * 屏上字：顺着他节奏（只做标签）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p34-他状态差就别招惹-好转也别急.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("顺着他节奏", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
