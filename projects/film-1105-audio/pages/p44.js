/* p44 · 为自己的生活负责
 * 图：../scene-library/p44-我可以为自己的生活负责-也愿-43.png（处境图库，图不复制）
 * 屏上字：为自己负责（只做标签）
 */
ENGINE.visual('p44', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p44-我可以为自己的生活负责-也愿-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("为自己负责", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
