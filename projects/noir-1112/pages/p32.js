/* p32 · 信任是空气 · generated */
ENGINE.visual("p32", (P) => {
  const H = P.hud;
  H.noirHeader(6, 7, "TRUST IS AIR", { at: 0.04, right: 'NOIR / 06' });
  H.noirLabel('06.01', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost('06', { x: 1230, y: 170, size: 310, opacity: 0.08 });
  P.noirReveal("信任是空气", { x: 148, y: 250, size: 96, color: 'orange', at: 0.3, dur: 0.7, stagger: 0.055 });
  P.text("没有信任，就没有真正的安全感", { x: 152, y: 392, size: 34, font: 'serif', color: 'soft', at: 0.9, mode: 'fade', dur: 0.55, w: 780, lh: 1.4 });
  P.noirHairline(150, 780, 452, { color: 'faint', sw: 1, at: 1.0, dur: 0.8, opacity: 0.72 });
  P.noirLabel('CHAPTER 06 / 07', 150, 820, { size: 12, color: 'muted', at: 0.8 });
  P.box(1120, 170, 560, 500, { r: 0, fill: null, color: 'faint', sw: 1, rough: 0, single: true, at: 0.55, dur: 1.0, pen: false });
  P.line(1120, 170, 1200, 170, { color: 'orange', sw: 1.2, at: 0.8, dur: 0.4, pen: false });
  P.line(1120, 170, 1120, 250, { color: 'orange', sw: 1.2, at: 0.86, dur: 0.4, pen: false });
  P.noirLabel('SPECIMEN / 06', 1120, 700, { size: 11, color: 'muted', at: 1.2 });
});
