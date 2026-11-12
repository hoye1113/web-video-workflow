/* p01 · opening question: one hook, one vertical rule, one ghost character. */
ENGINE.visual('p01', (P) => {
  const H = P.hud;
  H.noirHeader(1, 4, 'THE QUESTION', { at: 0.05 });

  P.noirGhost('问', { x: 1270, y: 210, size: 300, opacity: 0.07 });

  P.noirReveal('你真正想知道的', {
    x: 148, y: 226, size: 92, color: 'orange',
    at: 0.3, dur: 0.7, stagger: 0.042,
  });
  P.noirHairline(150, 760, 384, { color: 'faint', sw: 1, at: 0.72, dur: 0.8, opacity: 0.8 });

  const en = P.text('the question behind the question', {
    x: 152, y: 400, size: 26, font: 'latin', color: 'soft',
    at: 1.0, mode: 'fade', dur: 0.6,
  });
  en.el.style.letterSpacing = '0.06em';

  P.text('不是他爱不爱你', {
    x: 152, y: 444, size: 40, font: 'serif', color: 'ink',
    at: 1.18, mode: 'fade', dur: 0.5,
  });

  P.line(1300, 170, 1300, 650, {
    color: 'faint', sw: 1, rough: 0, single: true,
    at: 0.55, dur: 0.8, pen: false,
  });
  P.noirNode(1300, 170, 8, { at: 0.95, dur: 0.5 });
  H.noirLabel('01.01', 1300, 690, { size: 12, color: 'muted', at: 1.15 });
  H.noirLabel('SIGNAL / 01', 1650, 820, { size: 12, color: 'faint', at: 1.0 });
  H.noirLabel('01.02', 1700, 140, { size: 11, color: 'faint', at: 0.75 });
  H.noirLabel('01.03', 1700, 720, { size: 11, color: 'faint', at: 1.25 });

  H.noirNarration('你真正想知道的，不是他爱不爱你。', {
    at: P.c(0) + 0.05, kicker: '01 — NARRATION',
  });
});
