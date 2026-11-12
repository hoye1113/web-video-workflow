/* p17 · 第一步 · generated */
ENGINE.visual("p17", (P) => {
  const H = P.hud;
  H.noirHeader(3, 7, "THE FIRST STEP", { at: 0.04, right: 'NOIR / 03' });
  H.noirLabel('03.04', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("改", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("第一步", { x: 148, y: 220, size: 82, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("这是修复信任、重建亲密关系最关键的一步", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirConnector(360, 580, 900, 580, { color: 'soft', sw: 1, dashed: true, dash: '4 8', at: 1.0, dur: 0.7, opacity: 0.4 });
  P.noirConnector(1020, 580, 1560, 580, { color: 'soft', sw: 1, dashed: true, dash: '4 8', at: 1.2, dur: 0.7, opacity: 0.4 });
  P.noirNode(300, 580, 12, { color: 'orange', at: 1.1, dur: 0.45 });
  H.noirLabel('01', 288, 528, { size: 13, color: 'muted', at: 1.2 });
  P.text("坦荡认错", { x: 300, y: 620, w: 360, align: 'c', size: 30, font: 'serif', color: 'ink', at: 1.3, mode: 'fade', dur: 0.45 });
  P.noirNode(960, 580, 12, { color: 'orange', at: 1.25, dur: 0.45 });
  H.noirLabel('02', 948, 528, { size: 13, color: 'muted', at: 1.3499999999999999 });
  P.text("踏实改正", { x: 960, y: 620, w: 360, align: 'c', size: 30, font: 'serif', color: 'ink', at: 1.45, mode: 'fade', dur: 0.45 });
  P.noirNode(1620, 580, 12, { color: 'orange', at: 1.4000000000000001, dur: 0.45 });
  H.noirLabel('03', 1608, 528, { size: 13, color: 'muted', at: 1.5 });
  P.text("重建信任", { x: 1620, y: 620, w: 360, align: 'c', size: 30, font: 'serif', color: 'ink', at: 1.6, mode: 'fade', dur: 0.45 });
  P.noirLabel('STEPS / 03.04', 150, 820, { size: 12, color: 'muted', at: 1.2 });
});
