/* p36 · 打游戏刷视频没主见
 * 图：../scene-library/p36-打游戏刷视频-没有主见.png（处境图库，图不复制）
 * 屏上字：没主见（只做标签）
 */
ENGINE.visual('p36', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p36-打游戏刷视频-没有主见.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("没主见", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
