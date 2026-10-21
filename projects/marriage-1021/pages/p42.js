/* p42 · 他可能最想回归，但回归不等于修复
 * 图：../scene-library/p42-他可能最想回归-但回归不等于.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：回归≠修复（只做标签）
 */
ENGINE.visual('p42', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p42-他可能最想回归-但回归不等于.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1000, 620, 520, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("回归≠修复", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
