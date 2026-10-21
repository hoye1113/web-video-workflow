/* p06 · 「都可以」不是客气，是被默认了
 * 图：../scene-library/p06--都可以-不是客气-是被默认.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：被默认了（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06--都可以-不是客气-是被默认.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(820, 520, 520, { at: 0.5, kind: 'lamp', k: (lt) => PV.clamp(lt / 2) });
  P.text("被默认了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
