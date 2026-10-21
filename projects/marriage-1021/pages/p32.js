/* p32 · 来回几个小时，他看清这是长期消耗
 * 图：../scene-library/p32-来回几个小时-他看清这是长期.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：来回几小时（只做标签）
 */
ENGINE.visual('p32', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p32-来回几个小时-他看清这是长期.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(980, 300, 420, { at: 0.8, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.8) / 1.4) });
  P.text("来回几小时", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
