/* p09 · 背着你单独见面
 * 图：../scene-library/f1109-p09-43.png（处境图库，图不复制）
 * 屏上字：越界（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/f1109-p09-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1], [3.21, 1], [3.76, 1.12], [T, 1.12]].map(([t, z]) => ({ t, z })),
  });

  P.text("越界", { x: 250, y: 230, size: 50, align: 'l', color: '#F7F3EA', at: 1.2 });
});
