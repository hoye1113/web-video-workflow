/* p25 · 愧疚没让他停下，反而更想补偿
 * 图：../scene-library/p25-愧疚没让他停下-反而更想补偿.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：补偿心态（只做标签）
 */
ENGINE.visual('p25', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p25-愧疚没让他停下-反而更想补偿.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(560, 420, 560, { at: 0.6, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("补偿心态", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
