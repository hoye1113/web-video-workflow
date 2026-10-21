/* p38 · 她以为他更爱外面那个女人，真相不是谁更爱谁
 * 图：../scene-library/p38-她以为他更爱外面那个女人-真.png（处境图库，图不复制）
 * 光：lamp、window（光就是情绪）
 * 屏上字：不是谁更爱谁（只做标签）
 */
ENGINE.visual('p38', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p38-她以为他更爱外面那个女人-真.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(700, 500, 480, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.light(1300, 460, 360, { at: 0.9, kind: 'window', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.4) });
  P.text("不是谁更爱谁", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
