/* p23 · 早晚又站回老位置
 * 图：../scene-library/p23-旧人旧事还在-你早晚又站回老.png（处境图库，图不复制）
 * 屏上字：又站回去（只做标签）
 */
ENGINE.visual('p23', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p23-旧人旧事还在-你早晚又站回老.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("又站回去", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
