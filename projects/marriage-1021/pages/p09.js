/* p09 · 他怕的是孩子受影响，妻子当晚拿出离婚协议
 * 图：../scene-library/p09-他怕的是孩子受影响-妻子当晚.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：当场崩塌（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-他怕的是孩子受影响-妻子当晚.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 700, { at: 0.5, kind: 'window', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("当场崩塌", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
