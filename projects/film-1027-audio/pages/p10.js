/* p10 · 情绪反复，是伤口在说话
 * 图：../scene-library/p10-情绪阴晴不定-是心里的伤口在.png（处境图库，图不复制）
 * 屏上字：伤口在说话（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p10-情绪阴晴不定-是心里的伤口在.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("伤口在说话", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
