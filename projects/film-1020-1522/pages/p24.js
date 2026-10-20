/* p24 · 第三种最难：删除拉黑，态度决绝
 * 图：../scene-library/p16-keys.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：态度决绝（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p16-keys.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(770, 260, 480, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.4) / 1.6) });
  P.text("态度决绝", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
