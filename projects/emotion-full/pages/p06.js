/* p06 · 换副卡、删联系人，他用行动证明要回归
 * 图：../scene-library/p06-sim-card.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：断联消息（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-sim-card.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(980, 520, 460, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("断联消息", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
