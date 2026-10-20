/* p11 · 他不擅长解释，只会用距离说话
 * 图：../scene-library/male-08-empty-living.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：只会躲（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/male-08-empty-living.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(1380, 300, 460, { at: 0.7, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.7) / 1.5) });
  P.text("只会躲", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
