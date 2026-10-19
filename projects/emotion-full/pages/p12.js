/* p12 · 在外面被需要，回家只剩压力，所以他更爱逃
 * 图：../scene-library/male-05-door-crack.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：更容易逃避（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/male-05-door-crack.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1300, 300, 520, { at: 0.7, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.7) / 1.6) });
  P.text("更容易逃避", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
