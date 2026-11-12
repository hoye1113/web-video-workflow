/* p02 · three questions converge on one card; dashed connectors are the diagram. */
ENGINE.visual('p02', (P) => {
  const H = P.hud;
  H.noirHeader(2, 4, 'ALL ANSWERED HERE', { at: 0.05 });

  P.noirGhost('答', { x: 1330, y: 170, size: 300, opacity: 0.07 });

  P.noirReveal('三个问题', {
    x: 148, y: 210, size: 84, color: 'ink',
    at: 0.28, dur: 0.6, stagger: 0.05,
  });
  P.text('但感情里，没有标准答案。', {
    x: 152, y: 322, size: 34, font: 'serif', color: 'soft',
    at: 0.8, mode: 'fade', dur: 0.5,
  });
  P.noirHairline(150, 760, 370, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.75 });

  const rows = [
    ['01', '他还回来吗？', 402],
    ['02', '他还会爱吗？', 482],
    ['03', '你还能信吗？', 562],
  ];
  rows.forEach(([no, q, y], i) => {
    H.noirLabel(no, 150, y, { size: 14, color: 'orange', at: 0.65 + i * 0.18, track: '0.1em' });
    P.text(q, {
      x: 214, y: y - 12, size: 32, font: 'serif', color: 'ink',
      at: 0.75 + i * 0.18, mode: 'fade', dur: 0.45,
    });
    P.noirHairline(150, 760, y + 32, {
      color: 'faint', sw: 1, at: 0.8 + i * 0.18, dur: 0.6, opacity: 0.65,
    });
  });

  P.noirCard(1120, 438, 420, 166, {
    fill: '#0A1214', color: 'soft', sw: 1.1, at: 1.35, dur: 0.7,
  });
  P.line(1120, 438, 1164, 438, { color: 'orange', sw: 1.2, at: 1.55, dur: 0.3, pen: false });
  P.line(1120, 438, 1120, 482, { color: 'orange', sw: 1.2, at: 1.6, dur: 0.3, pen: false });
  P.check(1150, 470, 34, {
    color: 'green', sw: 2, rough: 0, single: true,
    at: 1.65, dur: 0.35, pen: false,
  });
  P.text('标准答案', {
    x: 1200, y: 458, size: 30, font: 'serif', color: 'ink',
    at: 1.55, mode: 'fade', dur: 0.45,
  });
  P.text('ALL ANSWERED HERE', {
    x: 1330, y: 540, w: 300, align: 'c', size: 12, font: 'mono', color: 'muted',
    at: 1.8, mode: 'fade', dur: 0.4,
  });

  rows.forEach(([, , y], i) => {
    P.noirConnector(760, y + 10, 1120, 500, {
      color: 'soft', sw: 1, dashed: true, dash: '3 7',
      at: 1.5 + i * 0.12, dur: 0.7, opacity: 0.42,
    });
  });

  H.noirLabel('02.01', 150, 690, { size: 12, color: 'muted', at: 1.2 });
  H.noirLabel('THREE / ONE', 1650, 820, { size: 12, color: 'faint', at: 1.15 });
  H.noirLabel('02.02', 1700, 140, { size: 11, color: 'faint', at: 0.75 });
  H.noirLabel('02.03', 1700, 720, { size: 11, color: 'faint', at: 1.25 });

  H.noirNarration('而是这段关系，还值不值得你继续。', {
    at: P.c(0) + 0.05, kicker: '02 — NARRATION',
  });
});
