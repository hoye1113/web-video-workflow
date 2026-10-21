/* p12 · 他以为结束了，第二天妻子开始追问细节
 * 图：../scene-library/p12-他以为结束了-第二天妻子开始.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：断联消息（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p12-他以为结束了-第二天妻子开始.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1010, 620, 420, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.2) });
  P.text("断联消息", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
