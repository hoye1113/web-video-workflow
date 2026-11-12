/* p28 · 警觉与多疑 · generated */
ENGINE.visual("p28", (P) => {
  const H = P.hud;
  H.noirHeader(5, 7, "VIGILANCE / PARANOIA", { at: 0.04, right: 'NOIR / 05' });
  H.noirLabel('05.01', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost('05', { x: 1230, y: 170, size: 310, opacity: 0.08 });
  P.noirReveal("警觉与多疑", { x: 148, y: 250, size: 96, color: 'orange', at: 0.3, dur: 0.7, stagger: 0.055 });
  P.text("理性的警觉，和草木皆兵的多疑，完全是两回事", { x: 152, y: 392, size: 34, font: 'serif', color: 'soft', at: 0.9, mode: 'fade', dur: 0.55, w: 780, lh: 1.4 });
  P.noirHairline(150, 780, 452, { color: 'faint', sw: 1, at: 1.0, dur: 0.8, opacity: 0.72 });
  P.noirLabel('CHAPTER 05 / 07', 150, 820, { size: 12, color: 'muted', at: 0.8 });
  P.box(1120, 170, 560, 500, { r: 0, fill: null, color: 'faint', sw: 1, rough: 0, single: true, at: 0.55, dur: 1.0, pen: false });
  P.line(1120, 170, 1200, 170, { color: 'orange', sw: 1.2, at: 0.8, dur: 0.4, pen: false });
  P.line(1120, 170, 1120, 250, { color: 'orange', sw: 1.2, at: 0.86, dur: 0.4, pen: false });
  P.noirLabel('SPECIMEN / 05', 1120, 700, { size: 11, color: 'muted', at: 1.2 });
});
