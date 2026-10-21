/* p14 · 别人眼里的你，都是你自己演出来的
 * 图：../scene-library/p14-别人眼里的你-都是你自己演出.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：你演出来的（只做标签）
 */
ENGINE.visual('p14', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p14-别人眼里的你-都是你自己演出.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1200, 380, 560, { at: 0.6, kind: 'window', k: (lt) => PV.clamp((lt - 0.6) / 1.5) });
  P.text("你演出来的", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
