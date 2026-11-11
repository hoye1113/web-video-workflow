/* p15 · 你正在给伴侣下一个负面预言
 * 图：../scene-library/f1111-p15-43.png（处境图库，图不复制）
 * 屏上字：负面预言（只做标签）
 */
ENGINE.visual('p15', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1111-p15-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("负面预言", { x: 250, y: 230, size: 50, align: 'l', color: '#F7F3EA', at: 1.2 });
});
