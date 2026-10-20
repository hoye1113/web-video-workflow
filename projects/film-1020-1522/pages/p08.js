/* p08 · 第一个信号：没删你，也没拉黑你
 * 图：../scene-library/p08-phone-ignored.png（处境图库，图不复制）
 * 光：window、screen（光就是情绪）
 * 屏上字：只是不回（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p08-phone-ignored.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 320, 480, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.light(1310, 620, 260, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.4) });
  P.text("只是不回", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
