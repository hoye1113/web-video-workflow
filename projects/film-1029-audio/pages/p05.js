/* p05 · 嘘寒问暖和故作高冷
 * 图：../scene-library/p05-嘘寒问暖或故作高冷-能追到吗.png（处境图库，图不复制）
 * 屏上字：很难追到（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p05-嘘寒问暖或故作高冷-能追到吗.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("很难追到", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
