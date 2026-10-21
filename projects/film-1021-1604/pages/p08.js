/* p08 · 你越坚强，别人越放心把事丢给你
 * 图：../scene-library/p08-你越坚强-别人越放心把事丢给.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：都先想到你（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p08-你越坚强-别人越放心把事丢给.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(560, 420, 560, { at: 0.6, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.6) / 1.5) });
  P.text("都先想到你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
