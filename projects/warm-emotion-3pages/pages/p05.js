/* p05 · 妻子提离婚当晚，他跪下来认错。
 * 一次有重量的动作 = 镜头推向那页离婚协议；其余都停着。 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('assets/p05-kneel.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    // 停 — 推 — 停：40% 处推近一次，落在协议上
    cam: [{ t: 0, z: 1 }, { t: T * 0.38, z: 1 }, { t: T * 0.38 + 0.7, z: 1.09 }, { t: T, z: 1.09 }],
  });

  // 一束窗光（左上方）
  P.light(500, 250, 720, { at: 0.4, kind: 'window', k: (lt) => PV.clamp(lt / 2) });

  // 标签（屏上字只做标签，≤8 字）
  P.text('离婚协议', { x: 300, y: 250, size: 40, align: 'l', color: 'ink', at: 1.4 });
});
