/* p05 · 妻子提离婚的当晚，他跪下来认错
 * 图：../scene-library/p05-kneel.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：当场崩塌（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-kneel.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(500, 250, 720, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("当场崩塌", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
