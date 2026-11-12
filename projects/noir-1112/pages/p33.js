/* p33 · 没有信任 · generated */
ENGINE.visual("p33", (P) => {
  const H = P.hud;
  H.noirHeader(6, 7, "NO TRUST", { at: 0.04, right: 'NOIR / 06' });
  H.noirLabel('06.02', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("信", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("没有信任", { x: 148, y: 220, size: 88, color: 'orange', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("和睦的亲密关系，也就无从谈起", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.box(1120, 220, 560, 460, { r: 0, fill: null, color: 'faint', sw: 1, rough: 0, single: true, at: 0.6, dur: 0.9, pen: false });
  P.line(1120, 220, 1200, 220, { color: 'orange', sw: 1.2, at: 0.9, dur: 0.35, pen: false });
  P.line(1120, 220, 1120, 300, { color: 'orange', sw: 1.2, at: 0.95, dur: 0.35, pen: false });
  P.noirLabel('SPECIMEN / 06.02', 1120, 700, { size: 11, color: 'muted', at: 1.25 });
  P.noirLabel('STATEMENT / 06.02', 150, 820, { size: 12, color: 'muted', at: 1.0 });
});
