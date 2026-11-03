/* p33 · 第一次真正听见对方
 * 图：../scene-library/p33-真正倾听对方-重新认识彼此.png（处境图库，图不复制）
 * 屏上字：听见对方（只做标签）
 */
ENGINE.visual('p33', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p33-真正倾听对方-重新认识彼此.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("听见对方", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
