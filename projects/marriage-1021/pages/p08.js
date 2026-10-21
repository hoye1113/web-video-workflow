/* p08 · 三年的关系就这么暴露了
 * 图：../scene-library/p08-三年的关系就这么暴露了.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：不是愧疚，是怕（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p08-三年的关系就这么暴露了.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(980, 560, 460, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.4) });
  P.text("不是愧疚，是怕", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
