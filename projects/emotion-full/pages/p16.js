/* p16 · 一次回家送钥匙，让他看清这是长期消耗
 * 图：../scene-library/p16-keys.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：来回几小时（只做标签）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p16-keys.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 180, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.3) / 1.6) });
  P.text("来回几小时", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
