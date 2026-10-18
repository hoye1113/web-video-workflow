/* p15 · 白天正常、晚上装没事。
 * 图本身就是夜景，所以只补一盏门口的光；机位慢慢推近门口。 */
ENGINE.visual('p15', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('assets/p15-night-door.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [{ t: 0, z: 1.02 }, { t: T * 0.4, z: 1.02 }, { t: T * 0.4 + 0.8, z: 1.08 }, { t: T, z: 1.08 }],
  });

  // 门里那束暖光（夜间唯一的光源）
  P.light(760, 520, 520, { at: 0.3, kind: 'lamp', k: (lt) => PV.clamp(lt / 1.8) });
});
