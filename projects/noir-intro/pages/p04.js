/* p04 · identity card: a waveform and a line-art microphone. */
ENGINE.visual('p04', (P) => {
  const H = P.hud;
  H.noirHeader(4, 4, 'THE VOICE', { at: 0.05 });

  P.noirGhost('声', { x: 1470, y: 170, size: 270, opacity: 0.06 });

  P.noirReveal('听过我的声音', {
    x: 148, y: 210, size: 84, color: 'ink',
    at: 0.28, dur: 0.65, stagger: 0.045,
  });
  P.text('你不一定认识我', {
    x: 152, y: 326, size: 36, font: 'serif', color: 'soft',
    at: 0.8, mode: 'fade', dur: 0.5,
  });
  const en = P.text('the voice you already know', {
    x: 152, y: 382, size: 24, font: 'latin', color: 'muted',
    at: 1.0, mode: 'fade', dur: 0.5,
  });
  en.el.style.letterSpacing = '0.06em';

  P.noirWave(1080, 300, 560, 105, { bars: 40, gap: 5, color: 'blue', at: 0.9, dur: 0.7 });
  P.noirLabel('VOICE / 01', 1080, 272, { size: 12, color: 'muted', at: 1.0 });

  P.path('M1364 470 Q1364 448 1390 448 Q1416 448 1416 470 L1416 548 Q1416 574 1390 574 Q1364 574 1364 548 Z', {
    color: 'orange', sw: 1.6, at: 1.2, dur: 0.7,
  });
  P.line(1374, 486, 1406, 486, { color: 'orange', sw: 1, at: 1.45, dur: 0.3, pen: false });
  P.line(1374, 504, 1406, 504, { color: 'orange', sw: 1, at: 1.52, dur: 0.3, pen: false });
  P.line(1374, 522, 1406, 522, { color: 'orange', sw: 1, at: 1.59, dur: 0.3, pen: false });
  P.line(1390, 574, 1390, 620, { color: 'orange', sw: 1.4, at: 1.65, dur: 0.3, pen: false });
  P.line(1350, 620, 1430, 620, { color: 'orange', sw: 1.4, at: 1.75, dur: 0.3, pen: false });
  P.line(1360, 646, 1420, 646, { color: 'orange', sw: 1.4, at: 1.82, dur: 0.3, pen: false });
  P.noirNode(1390, 432, 4, { at: 1.3, dur: 0.4, color: 'orange' });

  H.noirLabel('04.01', 150, 690, { size: 12, color: 'muted', at: 1.2 });
  H.noirLabel('HEARD / BEFORE', 1650, 820, { size: 12, color: 'faint', at: 1.1 });
  H.noirLabel('04.02', 1700, 140, { size: 11, color: 'faint', at: 0.75 });
  H.noirLabel('04.03', 1700, 720, { size: 11, color: 'faint', at: 1.25 });

  H.noirNarration('你不一定认识我，但你一定听过我的声音。', {
    at: P.c(0) + 0.05, kicker: '04 — NARRATION',
  });
});
