/* p36 · 对方的逻辑站得住
 * 图：../scene-library/p36-以男女之情为根基-对方坚决要.png（处境图库，图不复制）
 * 屏上字：站得住脚（只做标签）
 */
ENGINE.visual('p36', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p36-以男女之情为根基-对方坚决要.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("站得住脚", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
