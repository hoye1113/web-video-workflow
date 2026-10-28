/* p42 · 会比危机前更亲密
 * 图：../scene-library/p42-关系会比危机前更健康-更亲密.png（处境图库，图不复制）
 * 屏上字：比从前近（只做标签）
 */
ENGINE.visual('p42', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p42-关系会比危机前更健康-更亲密.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.24, dur: 1.52 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("比从前近", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
