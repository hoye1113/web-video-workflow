/* p03 · 女生最喜欢的三种追求
 * 图：../scene-library/p03-分享三种追求方式-记得点赞收.png（处境图库，图不复制）
 * 屏上字：三种方式（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p03-分享三种追求方式-记得点赞收.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("三种方式", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
