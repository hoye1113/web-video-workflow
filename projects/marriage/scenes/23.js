// 垂直切片 · 第 23 镜「床沿 ｜ 凹下去一块，男人的手撑在上面」
// 混合方案：场景与运动由代码画（光、床沿凹陷、呼吸），手是 Flow 生成 + 绿幕抠出来的贴图。
// 代码不画脸、不画有机形状，这一镜正好试「代码 + 生成图」的分工。
// 预览：index.html?film=compare   渲染：render.py --film compare --solo zz_bedside --from 0 --to 5
SCENES['23'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, ss } = U;
  const C = { dark: '#2A2A2A', sheet: '#F1EAE2', fold: '#CFC5B6', ink: '#2A2A2A', warm: '#E9B872' };
  const LW = 5;
  const HAND = 'demos/marriage/assets/hand_v2.png';
  // 手贴图落位（sprite 1129×768 的 RGBA）
  const HW = 620, HH = 620 * 768 / 1129, HX = 640, HY = 350;
  const DIPX = 900, DIPBASE = 706;                 // 床沿被压凹的最低点

  // 床沿：中间一段被手压下去，两边自然回弹
  function bedEdge(sag) {
    const y = DIPBASE + sag;
    const p = new Path2D();
    p.moveTo(0, 638);
    p.bezierCurveTo(320, 644, 560, 676, 706, y - 6);
    p.bezierCurveTo(820, y + 12, 990, y + 12, 1096, y - 6);
    p.bezierCurveTo(1300, 676, 1620, 644, W, 632);
    p.lineTo(W, H); p.lineTo(0, H); p.closePath();
    return p;
  }

  return {
    draw(c, lt, t, IMG) {
      const im = IMG[HAND];
      if (!im) throw new Error('贴图没加载：' + HAND);
      const p = clamp(lt / 5);
      const press = ss(0.2, 0.85, p);                            // 压下去的进度
      const sag = press * 22;                                    // 床沿下沉
      const breath = Math.sin(t * 1.15) * 2.2;                   // 呼吸般的极轻起伏

      // ---- 夜：大面积墨色 ----
      c.fillStyle = C.dark; c.fillRect(0, 0, W, H);

      // ---- 窗光：软边的光束（线性渐变做边缘）----
      const beam = (x0, x1, a) => {
        const g = c.createLinearGradient(x0, 0, x1, 0);
        g.addColorStop(0, 'rgba(233,184,114,0)');
        g.addColorStop(0.5, `rgba(233,184,114,${a})`);
        g.addColorStop(1, 'rgba(233,184,114,0)');
        c.save(); c.fillStyle = g;
        c.beginPath(); c.moveTo(x0, -80); c.lineTo(x1, -80); c.lineTo(x1 + 520, H); c.lineTo(x0 + 380, H); c.closePath(); c.fill();
        c.restore();
      };
      beam(-40, 620, 0.20); beam(760, 1180, 0.13);

      // ---- 床 ----
      const edge = bedEdge(sag + breath * 0.3);
      c.save(); c.fillStyle = C.sheet; c.fill(edge); c.restore();
      c.save(); c.strokeStyle = C.warm; c.lineWidth = 7; c.globalAlpha = 0.5; c.stroke(edge); c.restore();

      // 被压处的放射折痕：从凹陷往外拉，这是「凹下去」的视觉证据
      c.save(); c.strokeStyle = C.fold; c.lineWidth = 4; c.lineCap = 'round'; c.globalAlpha = 0.9;
      const y1 = DIPBASE + sag + 10;
      [[-300, 92], [-186, 140], [190, 132], [312, 86], [-420, 54], [432, 50]].forEach(([dx, len], i) => {
        const sx = DIPX + dx * 0.72, sy = y1 + 6 + Math.abs(dx) * 0.02;
        c.beginPath(); c.moveTo(sx, sy);
        c.quadraticCurveTo(sx + dx * 0.1, sy + len * 0.62, sx + dx * 0.16, sy + len);
        c.stroke();
      });
      c.restore();
      // 床单远处几条长褶皱
      c.save(); c.strokeStyle = C.fold; c.lineWidth = 4; c.lineCap = 'round'; c.globalAlpha = 0.7;
      [[150, 830, 210], [430, 862, 176], [1420, 826, 196], [1700, 856, 160]].forEach(([x, y, len]) => {
        c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + 30, y + len * 0.55, x + 6, y + len); c.stroke();
      });
      c.restore();
      // 凹陷处的一片暗（手压出来的窝）
      c.save(); c.globalAlpha = 0.13; c.fillStyle = C.ink;
      c.beginPath(); c.ellipse(DIPX - 10, DIPBASE + sag + 30, 210, 30, 0, 0, TAU); c.fill(); c.restore();

      // ---- 手：影子 + 压暗融入夜景 ----
      const hy = HY + sag + breath;
      c.save();
      c.globalAlpha = 0.26; c.filter = 'brightness(0) blur(5px)';
      c.drawImage(im, HX + 14, hy + 20, HW, HH);
      c.restore();
      // 只把手压暗一档，不额外打光：扁平线稿不需要在贴图上伪造受光
      c.save();
      c.filter = 'brightness(0.93) sepia(0.06)';
      c.drawImage(im, HX, hy, HW, HH);
      c.restore();
    },
  };
})();
