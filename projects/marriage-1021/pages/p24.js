/* p24 · 在外面被需要，在家里只有压力和责任
 * 图：../scene-library/p24-在外面被需要-在家里只有压力.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：被需要（只做标签）
 */
ENGINE.visual('p24', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p24-在外面被需要-在家里只有压力.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 780, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("被需要", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
