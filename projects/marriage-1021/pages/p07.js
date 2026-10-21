/* p07 · 暴露始于一次意外：孩子用他的手机上网课
 * 图：../scene-library/p07-暴露始于一次意外-孩子用他的.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：3年的关系（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p07-暴露始于一次意外-孩子用他的.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1010, 620, 420, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.2) });
  P.text("3年的关系", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
