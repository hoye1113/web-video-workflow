/* p47 · 别停在两边都想要的状态里反复拉扯
 * 图：../scene-library/p47-别停在两边都想要的状态里反复.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：别两边都要（只做标签）
 */
ENGINE.visual('p47', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p47-别停在两边都想要的状态里反复.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(1500, 400, 520, { at: 0.5, kind: 'window', k: (lt) => PV.clamp((lt - 0.5) / 1.6) });
  P.text("别两边都要", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
