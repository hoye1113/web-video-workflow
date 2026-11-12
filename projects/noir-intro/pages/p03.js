/* p03 · true/false split: two curves, one eye, one cross. */
ENGINE.visual('p03', (P) => {
  const H = P.hud;
  H.noirHeader(3, 4, 'TRUE / FALSE', { at: 0.05 });

  P.noirGhost('真', { x: 900, y: 220, size: 290, opacity: 0.08 });
  P.noirGhost('假', { x: 1340, y: 300, size: 290, opacity: 0.08 });

  P.noirReveal('判断力', {
    x: 148, y: 210, size: 96, color: 'orange',
    at: 0.28, dur: 0.65, stagger: 0.07,
  });
  P.text('真真假假，难以分辨', {
    x: 152, y: 326, size: 34, font: 'serif', color: 'blue',
    at: 0.8, mode: 'fade', dur: 0.5,
  });

  P.noirEye(1298, 250, 96, { color: 'blue', at: 0.95 });
  H.noirLabel('SIGNAL / NOISE', 150, 470, { size: 12, color: 'muted', at: 1.0 });

  P.noirHairline(980, 1700, 570, { color: 'faint', sw: 1, at: 0.9, dur: 0.8, opacity: 0.65 });
  P.noirNode(980, 570, 6, { at: 1.15, dur: 0.45 });

  P.noirCurve('M980 570 C1200 570 1420 430 1700 300', {
    color: 'blue', sw: 2.2, glow: 7, at: 1.05, dur: 1.1,
  });
  P.noirCurve('M980 570 C1200 570 1420 700 1700 780', {
    color: 'red', sw: 2.2, glow: 6, at: 1.2, dur: 1.1,
  });

  P.noirLabel('TRUE', 1688, 268, { size: 18, color: 'blue', at: 2.15, track: '0.18em' });
  P.noirLabel('FALSE', 1688, 748, { size: 18, color: 'red', at: 2.25, track: '0.18em' });

  P.line(1582, 672, 1624, 714, {
    color: 'red', sw: 2, rough: 0, single: true,
    at: 2.35, dur: 0.2, pen: false,
  });
  P.line(1624, 672, 1582, 714, {
    color: 'red', sw: 2, rough: 0, single: true,
    at: 2.42, dur: 0.2, pen: false,
  });

  H.noirLabel('03.01', 150, 690, { size: 12, color: 'muted', at: 1.2 });
  H.noirLabel('TRUE / FALSE', 1650, 820, { size: 12, color: 'faint', at: 1.1 });
  H.noirLabel('03.02', 1700, 140, { size: 11, color: 'faint', at: 0.75 });
  H.noirLabel('03.03', 1700, 720, { size: 11, color: 'faint', at: 1.25 });

  H.noirNarration('别急着找答案，先找回你的判断力。', {
    at: P.c(0) + 0.05, kicker: '03 — NARRATION',
  });
});
