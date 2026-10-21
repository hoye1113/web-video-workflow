/* p48 · 毁掉婚姻的是长期的逃避和不负责任
 * 图：../scene-library/p48-毁掉婚姻的是长期的逃避和不负.png（处境图库，图不复制）
 * 光：lamp、window（光就是情绪）
 * 屏上字：毁在长期逃避（只做标签）
 */
ENGINE.visual('p48', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p48-毁掉婚姻的是长期的逃避和不负.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(700, 500, 500, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.light(1320, 480, 380, { at: 0.9, kind: 'window', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.4) });
  P.text("毁在长期逃避", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
