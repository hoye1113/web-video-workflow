/* p52 · 有问题，随时来找我
 * 图：../scene-library/p52-有问题随时来找我-我是李安.png（处境图库，图不复制）
 * 屏上字：有问题找我（只做标签）
 */
ENGINE.visual('p52', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p52-有问题随时来找我-我是李安.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("有问题找我", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
