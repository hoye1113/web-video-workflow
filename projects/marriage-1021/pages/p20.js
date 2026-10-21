/* p20 · 他觉得自己好像重新活了一次
 * 图：../scene-library/p20-他觉得自己好像重新活了一次.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：重新活了一次（只做标签）
 */
ENGINE.visual('p20', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p20-他觉得自己好像重新活了一次.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 470, 400, { at: 0.8, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.8) / 1.5) });
  P.text("重新活了一次", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
