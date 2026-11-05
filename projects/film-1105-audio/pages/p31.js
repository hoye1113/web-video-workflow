/* p31 · 让表达从攻击变成沟通
 * 图：../scene-library/p31-让表达从攻击变成沟通-等情绪-43.png（处境图库，图不复制）
 * 屏上字：攻击变沟通（只做标签）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p31-让表达从攻击变成沟通-等情绪-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("攻击变沟通", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
