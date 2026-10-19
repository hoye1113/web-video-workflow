/* p09 · 婚姻在出事之前，早已无波无澜
 * 图：../scene-library/male-03-long-table.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：无波无澜（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/male-03-long-table.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(620, 640, 560, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("无波无澜", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
