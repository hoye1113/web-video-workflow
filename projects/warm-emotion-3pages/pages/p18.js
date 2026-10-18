/* p18 · 一边要家庭，一边要刺激 = 内在冲突。
 * 两束光一暖一冷，是他心里的两个方向；人不看任何一边。 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('assets/p18-two-doors.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [{ t: 0, z: 1 }, { t: T * 0.45, z: 1 }, { t: T * 0.45 + 0.7, z: 1.06 }, { t: T, z: 1.06 }],
  });

  // 两束光：左边暖（家里），右边冷（外面）
  P.light(300, 640, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.light(1620, 640, 560, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.5) });

  // 两个标签，依次出现
  P.text('家里', { x: 260, y: 230, size: 40, align: 'l', color: 'orange', at: 1.6 });
  P.text('外面', { x: 1500, y: 230, size: 40, align: 'l', color: 'blue', at: 2.4 });
});
