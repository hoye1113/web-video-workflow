// 第18页·真相拆解：两列方格（左红＝家庭／右青＝刺激）一行行交替亮起，中缝一道细颤线——不是选择，是内在冲突。
// 节奏：0.0s 整片方格先以极淡压痕在场、第一格已起头 → 每行约隔 0.15*dur 依次落笔并亮起（偶行红先、奇行青先，各自从外侧往中缝扫）→ 0.60*dur 出字 → 0.63~0.90*dur 中缝颤线自上而下画成 → 末段两列交替明暗收束。镜头停。
SCENES['18'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', red: '#C8402F', teal: '#2F5D62' };
  const DUR = 13;
  const CELL = 200, GAPX = 112, GAPY = 74, ROWS = 4;
  const GW = 2 * CELL + GAPX, GH = ROWS * CELL + (ROWS - 1) * GAPY;    // 512 × 1022
  const L = (W - GW) / 2, T = (H - GH) / 2, CX = W / 2;                // 704 / 29 / 960：主角高占画面 95%
  const cellX = i => L + i * (CELL + GAPX);
  const cellY = j => T + j * (CELL + GAPY);
  const hY = j => j >= ROWS ? T + GH : T + j * (CELL + GAPY);
  const ROWT = [0.02, 0.17, 0.32, 0.47];                              // 每行起亮时刻（× DUR）
  const LAG = 0.65;                                                   // 同一行里第二列晚亮的秒数
  const TXT = '一边…一边…';

  // 同一支笔（与全片同款）：分段描边，线宽自然顿挫，圆头圆角，不换第二套笔触
  const pen = (c, pts, w, seed, taper, a) => {
    if (!pts || pts.length < 2) return;
    const r = rng(seed);
    c.save(); c.globalAlpha = a === undefined ? 1 : a; c.strokeStyle = C.ink;
    c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      const s = i / (pts.length - 1), tp = taper ? clamp((1 - s) / taper) : 1;
      c.lineWidth = w * (0.75 + r() * 0.75) * (0.35 + 0.65 * tp);
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };
  // 手画的直线：垂直方向固定抖动（不随帧变，否则线会逐帧发颤）
  const JIT = (() => { const r = rng(181), o = []; for (let i = 0; i < 512; i++) o.push((r() - 0.5) * 3.0); return o; })();
  const line = (x1, y1, x2, y2, k, n) => {
    const o = [], dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
    const nx = -dy / len, ny = dx / len;
    for (let i = 0; i <= n; i++) {
      const s = i / n, j = JIT[(k * 41 + i * 7) % 512];
      o.push([x1 + dx * s + nx * j, y1 + dy * s + ny * j]);
    }
    return o;
  };
  const cut = (pts, k) => pts.slice(0, Math.max(2, Math.round(k * (pts.length - 1)) + 1));

  // 骨架：每行是两格“缺上边”的方框（上边只由第 0 行画），每条线只落一次笔
  const EDGE = [];
  for (let j = 0; j < ROWS; j++) {
    const e = [], y0 = hY(j), y1 = hY(j + 1);
    for (let i = 0; i < 2; i++) {
      const xa = cellX(i), xb = xa + CELL, k = j * 8 + i * 3;
      if (j === 0) e.push(line(xa, y0, xb, y0, k, 6));
      e.push(line(xa, y1, xb, y1, k + 19, 6));
      e.push(line(xa, y0, xa, y1, k + 37, 6));
      e.push(line(xb, y0, xb, y1, k + 55, 6));
    }
    EDGE.push(e);
  }

  // 亮起：从该格外侧的边往里扫，压平整块；底部一条淡墨＝两档平涂的暗面
  const fillCell = (c, i, j, prog, pa) => {
    if (prog <= 0.002) return;
    const x = cellX(i), y = cellY(j), w = CELL * clamp(prog);
    const px = i === 0 ? x - 4 : x + CELL - w;
    c.save();
    c.beginPath(); c.rect(x - 4, y - 4, CELL + 8, CELL + 8); c.clip();
    c.globalAlpha = pa; c.fillStyle = i === 0 ? C.red : C.teal;
    c.fillRect(px, y - 4, w + 4, CELL + 8);
    c.globalAlpha = pa * 0.14; c.fillStyle = C.ink;
    c.fillRect(px, y + CELL * 0.74, w + 4, CELL * 0.30);
    c.restore();
  };

  // 中缝的细颤线：两股力互相拽着，自方格上沿往下画成，末了两端仍轻轻发抖
  const tension = (c, lt) => {
    const k = ss(8.2, 11.7, lt);
    if (k <= 0.002) return;
    const yA = T + 5, yB = T + GH - 5, yE = lerp(yA, yB, ease.out(k));
    const A = 20 * (0.82 + 0.18 * Math.sin(lt * 1.9)), ph = 0.6 + 0.7 * Math.sin(lt * 1.1);
    const pts = [], n = 40;
    for (let i = 0; i <= n; i++) {
      const y = lerp(yA, yE, i / n);
      pts.push([CX + A * Math.sin((y - yA) / (yB - yA) * TAU * 3 + ph), y]);
    }
    pen(c, pts, 2.6, 77, 0.25, 0.72);
  };

  return {
    draw(c, lt, t, IMG) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                     // 每帧自己画背景

      // ① 载体：两列共 8 张浅纸格，第一帧就在
      c.fillStyle = C.paper;
      for (let j = 0; j < ROWS; j++) for (let i = 0; i < 2; i++) c.fillRect(cellX(i), cellY(j), CELL, CELL);

      // ② 第一帧交代主角与走向：整片方格先以极淡的铅笔压痕在场
      for (let j = 0; j < ROWS; j++) for (const p of EDGE[j]) pen(c, p, 2.4, 300 + j, 0, 0.16);

      // ③ 一行行交替亮起：偶行红先、奇行青先，各自从外侧往中缝扫
      for (let j = 0; j < ROWS; j++) {
        const first = j % 2 === 0 ? 0 : 1;
        const pulse = 1 - 0.18 * ss(11.2, 12.3, lt) * (0.5 + 0.5 * Math.sin(lt * 1.9 + j * 0.9));
        for (let i = 0; i < 2; i++) {
          const t0 = ROWT[j] * DUR + (i === first ? 0 : LAG);
          fillCell(c, i, j, ss(t0 - 0.45, t0 + 0.85, lt), pulse);
        }
        // ④ 该行的格线随后落笔，压住色块边沿
        const rv = ss(ROWT[j] * DUR - 0.5, ROWT[j] * DUR + 0.35, lt);
        if (rv > 0.01) for (const p of EDGE[j]) pen(c, cut(p, rv * 1.35), 3.6, 500 + j * 7, rv < 1 ? 0.25 : 0, 0.88 * Math.min(1, rv * 1.4));
      }

      // ⑤ 0.63*dur 起，中缝颤线自上而下画成
      tension(c, lt);

      // ⑥ 0.60*dur 出字：逐字浮现，落在左下留白，不抢重心
      const pt = ss(7.8, 8.9, lt);
      if (pt > 0.01) {
        c.save(); c.fillStyle = C.ink; c.font = '500 54px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        let tx = 140;
        for (let i = 0; i < TXT.length; i++) {
          const k = clamp(pt * 1.7 - i * 0.09);
          if (k > 0.01) { c.globalAlpha = 0.92 * k; c.fillText(TXT[i], tx, 210 + (1 - k) * 12); }
          tx += c.measureText(TXT[i]).width + 6;
        }
        c.restore();
      }
    }
  };
})();
