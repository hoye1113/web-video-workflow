/* p61 · 她会慢慢把你当自己人
 * 图：../scene-library/p61-慢慢把你当成自己人.png（处境图库，图不复制）
 * 屏上字：当成自己人（只做标签）
 */
ENGINE.visual('p61', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p61-慢慢把你当成自己人.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("当成自己人", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
