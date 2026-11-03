/* p08 · 第二天照样一起做饭
 * 图：../scene-library/p08-很多人打完架-第二天照样一起.png（处境图库，图不复制）
 * 屏上字：照样做饭（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p08-很多人打完架-第二天照样一起.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("照样做饭", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
