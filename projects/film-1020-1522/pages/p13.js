/* p13 · 他嘴上说放下了，手机却一直没离手
 * 图：../scene-library/p13-phone-in-hand.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：谁先低头（只做标签）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p13-phone-in-hand.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 420, 400, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.4) });
  P.text("谁先低头", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
