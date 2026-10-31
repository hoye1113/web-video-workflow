/* p04 · 核心是吸引消失
 * 图：../scene-library/p04-最核心的原因-是动物性爱恋消.png（处境图库，图不复制）
 * 屏上字：吸引没了（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-最核心的原因-是动物性爱恋消.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("吸引没了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
