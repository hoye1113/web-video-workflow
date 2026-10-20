/* p08 · 低头换不来对等，只换来更久的沉默
 * 图：../scene-library/p08-低头换不来对等-只换来更久的.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：不等于对等（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p08-低头换不来对等-只换来更久的.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.86, saturate: 0.85 },
  });

  P.light(480, 420, 540, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.4) / 1.6) });
  P.text("不等于对等", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
