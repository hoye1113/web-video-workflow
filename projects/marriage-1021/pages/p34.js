/* p34 · 三个故事讲完了：有一个很反直觉的结论
 * 图：../scene-library/p34-三个故事讲完了-有一个很反直.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：反直觉的结论（只做标签）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p34-三个故事讲完了-有一个很反直.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 250, 740, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("反直觉的结论", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
