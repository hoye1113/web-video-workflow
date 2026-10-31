/* p13 · 对方会替你找理由
 * 图：../scene-library/p13-对方甚至会在情感滤镜下替你找.png（处境图库，图不复制）
 * 屏上字：替你开脱（只做标签）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p13-对方甚至会在情感滤镜下替你找.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("替你开脱", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
