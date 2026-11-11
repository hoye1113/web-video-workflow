/* p48 · 真的去相信他会变好
 * 图：../scene-library/f1111-p48-43.png（处境图库，图不复制）
 * 屏上字：信任是源泉（只做标签）
 */
ENGINE.visual('p48', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1111-p48-43.png', {
    at: 0,
    reveal: { from: 0.4, to: 1, at: 0.1, dur: 1.3 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("信任是源泉", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
