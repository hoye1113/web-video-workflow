/* p03 · 也依旧要选择频繁与其他异性深入互动
 * 图：../scene-library/f1109-p03-43.png（处境图库，图不复制）
 * 屏上字：不是不懂（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1109-p03-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("不是不懂", { x: 250, y: 230, size: 50, align: 'l', color: '#F7F3EA', at: 1.2 });
});
