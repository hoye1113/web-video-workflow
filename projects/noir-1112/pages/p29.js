/* p29 · 捕风捉影 · generated */
ENGINE.visual("p29", (P) => {
  const H = P.hud;
  H.noirHeader(5, 7, "THE SHADOW", { at: 0.04, right: 'NOIR / 05' });
  H.noirLabel('05.02', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("影", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("捕风捉影", { x: 148, y: 220, size: 82, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("过度多疑，大多源于内心的自卑", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirCard(1140, 440, 400, 190, { fill: '#0A1214', color: 'soft', sw: 1.0, at: 1.25, dur: 0.7 });
  P.line(1140, 440, 1182, 440, { color: 'orange', sw: 1.2, at: 1.45, dur: 0.3, pen: false });
  P.line(1140, 440, 1140, 484, { color: 'orange', sw: 1.2, at: 1.5, dur: 0.3, pen: false });
  P.text("多疑", { x: 1330, y: 492, w: 300, align: 'c', size: 34, font: 'serif', color: 'ink', at: 1.5, mode: 'fade', dur: 0.5 });
  P.noirLabel('THE / LIST', 1340, 570, { size: 12, color: 'muted', at: 1.7 });
  H.noirLabel('01', 150, 480, { size: 13, color: 'orange', at: 0.95, track: '0.1em' });
  P.text("正常相处 → 关系越界", { x: 210, y: 468, size: 31, font: 'serif', color: 'ink', at: 1.0, mode: 'fade', dur: 0.45, w: 760 });
  P.noirHairline(150, 760, 518, { color: 'faint', sw: 1, at: 1.05, dur: 0.55, opacity: 0.6 });
  H.noirLabel('02', 150, 572, { size: 13, color: 'orange', at: 1.2, track: '0.1em' });
  P.text("吃顿饭 → 旧情复燃", { x: 210, y: 560, size: 31, font: 'serif', color: 'ink', at: 1.25, mode: 'fade', dur: 0.45, w: 760 });
  P.noirHairline(150, 760, 610, { color: 'faint', sw: 1, at: 1.3, dur: 0.55, opacity: 0.6 });
  H.noirLabel('03', 150, 664, { size: 13, color: 'orange', at: 1.45, track: '0.1em' });
  P.text("不够认可自己 → 难以信任", { x: 210, y: 652, size: 31, font: 'serif', color: 'ink', at: 1.5, mode: 'fade', dur: 0.45, w: 760 });
  P.noirHairline(150, 760, 702, { color: 'faint', sw: 1, at: 1.55, dur: 0.55, opacity: 0.6 });
  P.noirLabel('INDEX / 05.02', 150, 820, { size: 12, color: 'muted', at: 1.2 });
});
