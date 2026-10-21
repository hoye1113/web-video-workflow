/* p14 · 他怕事情失控：清空账号和支付工具
 * 图：../scene-library/p14-他怕事情失控-清空账号和支付.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：全部清空（只做标签）
 */
ENGINE.visual('p14', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p14-他怕事情失控-清空账号和支付.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.3, dur: 1.4 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.light(1010, 600, 420, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.4) });
  P.text("全部清空", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
