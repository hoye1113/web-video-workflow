/* p10 · 迎合来自恐惧
 * 图：../scene-library/p10-你的失落和迎合-全来自怕离婚.png（处境图库，图不复制）
 * 屏上字：怕离婚（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p10-你的失落和迎合-全来自怕离婚.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("怕离婚", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
