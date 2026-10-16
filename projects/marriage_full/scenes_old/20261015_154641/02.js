Now I have the full picture (page 02 → `projects/marriage_full/scenes/02.js`, junction-linked into the engine's demos). Writing the scene:Trimming to fit the 160-line budget and nudging the main-subject weight:// 页02 · 钩子：一道纸裂缝从纸的下边缘起头，一路向上爬满整张纸 —— 屏上字「窗户纸」
SCENES['02'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss, ease, rng } = U;
  const DUR = 11;
  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F' };

  // ============ 全片只有这一支笔：逐段变粗细、变浓淡，圆头、轻微抖动 ============
  function pen(c, pts, seed, jit, baseW, col) {
    const n = pts.length;
    if (n < 2) return;
    const r = rng(seed), jx = new Float64Array(n), jy = new Float64Array(n);
    for (let i = 0; i < n; i++) { jx[i] = (r() * 2 - 1) * jit; jy[i] = (r() * 2 - 1) * jit; }
    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = col || C.ink;
    for (let i = 0; i < n - 1; i++) {
      const A = pts[i], B = pts[i + 1], al = (A.a + B.a) * 0.5;
      if (al < 0.02) continue;
      c.globalAlpha = clamp(al, 0, 1);
      c.lineWidth = Math.max(0.8, baseW * (A.w + B.w) * 0.5);
      c.beginPath(); c.moveTo(A.x + jx[i], A.y + jy[i]); c.lineTo(B.x + jx[i + 1], B.y + jy[i + 1]); c.stroke();
    }
    c.globalAlpha = 1;
  }

  // ============ 载体：一张竖着的纸，四周留白 ============
  const SX0 = 706, SY0 = 112, SX1 = 1414, SY1 = 968;
  const CW = SX1 - SX0, CH = SY1 - SY0, CX = (SX0 + SX1) / 2;
  const EDGE = (() => {
    const pts = [], add = (xa, ya, xb, yb) => {
      const n = Math.max(2, Math.round(Math.hypot(xb - xa, yb - ya) / 92));
      for (let i = 0; i < n; i++) { const u = i / n; pts.push({ x: lerp(xa, xb, u), y: lerp(ya, yb, u), a: 0.42, w: 1 }); }
    };
    add(SX0, SY0, SX1, SY0); add(SX1, SY0, SX1, SY1); add(SX1, SY1, SX0, SY1); add(SX0, SY1, SX0, SY0);
    return pts;
  })();

  // ============ 主角：裂缝的中心线（形态唯一，整页只沿自己往上长） ============
  // 下边缘上方 4px 起、上边缘下方 4px 止：长 848px ≈ 画面高的 78%
  const BY = SY1 - 4, TY = SY0 + 4, N = 64;
  const curl = (u) => CX + Math.sin(u * 5.9 + 0.5) * 26 + Math.sin(u * 13.4 + 2.1) * 9 + Math.sin(u * 27.7 + 4.3) * 3.2;
  const CL = [], CUM = [0];
  for (let i = 0; i < N; i++) {
    const s = i / (N - 1);
    CL.push({ s, x: curl(s), y: lerp(BY, TY, Math.pow(s, 0.98)) });
    if (i) CUM.push(CUM[i - 1] + Math.hypot(CL[i].x - CL[i - 1].x, CL[i].y - CL[i - 1].y));
  }
  const TOTAL = CUM[N - 1] || 1;
  const at = (u) => {
    const s = clamp(u) * TOTAL;
    let i = 1; while (i < N - 1 && CUM[i] < s) i++;
    const seg = (CUM[i] - CUM[i - 1]) || 1, f = clamp((s - CUM[i - 1]) / seg);
    return { x: lerp(CL[i - 1].x, CL[i].x, f), y: lerp(CL[i - 1].y, CL[i].y, f) };
  };

  // 分叉：两端都落在主线上，只长高，不在画面中间留断头
  const BR = [{ a: 0.13, b: 0.27, dir: -1, h: 25 }, { a: 0.37, b: 0.51, dir: 1, h: 29 },
              { a: 0.60, b: 0.71, dir: -1, h: 17 }, { a: 0.79, b: 0.88, dir: 1, h: 12 }];
  const BRP = BR.map((b) => {
    const n = 26, out = [];
    for (let i = 0; i < n; i++) {
      const q = i / (n - 1), u = lerp(b.a, b.b, q), P = at(u);
      out.push({ u, q, x: P.x, y: P.y, ox: b.dir * b.h * Math.pow(Math.sin(Math.PI * q), 0.7) });
    }
    return out;
  });

  // 12fps 手绘抖：整条缝一起抖（种子固定，逐帧可复现）
  const BOIL = (() => {
    const fr = [];
    for (let k = 0; k < 8; k++) {
      const r = rng(4100 + k * 37), bx = [], by = [];
      for (let i = 0; i < N; i++) { bx.push((r() * 2 - 1) * 1.5); by.push((r() * 2 - 1) * 1.2); }
      fr.push({ x: bx, y: by });
    }
    return fr;
  })();

  // ============ 节奏：这一页的五拍（秒） ============
  const KEY = [[0, 0, 1], [1.10, 0.09, 1.6], [2.80, 0.26, 1.2], [5.60, 0.58, 1], [8.40, 0.86, 1], [10.20, 1, 1.4]];
  const front = (x) => {
    if (x <= 0) return 0;
    for (let i = 0; i < KEY.length - 1; i++) {
      const A = KEY[i], B = KEY[i + 1];
      if (x <= B[0]) return lerp(A[1], B[1], Math.pow(clamp((x - A[0]) / (B[0] - A[0])), B[2]));
    }
    return 1;
  };

  // ============ 屏上字：竖排，落在左侧留白 ============
  const TXT = (() => {
    const r = rng(731);
    return ['窗', '户', '纸'].map((ch, i) => ({ ch, x: 342 + (r() * 2 - 1) * 4, y: 384 + i * 148 + (r() * 2 - 1) * 5, rot: (r() * 2 - 1) * 0.05 }));
  })();

  return {
    draw(c, lt, t) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                      // 每帧自己画底
      const settle = ease.out(clamp(lt / 0.9));                        // 拍1：纸落位
      const F = front(lt);                                             // 拍2/3：裂缝爬到哪儿
      const push = 1 + 0.16 * ss(9.9, 10.7, lt);                       // 拍5：贯通后加重
      const boil = BOIL[Math.floor(U.stepTime(lt, 12) * 12) % 8];
      c.save(); c.translate(0, (1 - settle) * 26);

      // —— 纸（载体）
      c.globalAlpha = 0.10 * (0.35 + 0.65 * settle);
      c.fillStyle = C.gray; c.fillRect(SX0 + 16, SY0 + 20, CW, CH);
      c.globalAlpha = 1;
      c.fillStyle = C.paper; c.fillRect(SX0, SY0, CW, CH);
      pen(c, EDGE, 611, 1.0, 2.6, C.gray);

      // —— 主角：裂缝。第一帧先是一道极淡的压痕 + 底边的线头，之后沿它往上长
      const band = [];
      for (let i = 0; i < N; i++) {
        const g = CL[i];
        const rev = ss(0, 1, (F - g.s) / 0.035);                       // 前沿扫过，墨才上来
        const age = ss(0, 1, (F - g.s) / 0.13);                        // 裂开越久，口子越重
        const op = Math.max(rev, ss(0, 1, (0.018 - g.s) / 0.018));     // 底边的线头
        band.push({ x: g.x + boil.x[i], y: g.y + boil.y[i], a: 0.17 + 0.76 * op,
                    w: (0.50 + 0.62 * Math.max(op, 0.55 * age)) * push });
      }
      pen(c, band, 13, 0.85, 5.4, C.ink);

      // —— 分叉：前沿爬到哪儿，哪根就从主线里张开来（两端始终连在主线上）
      for (let k = 0; k < BR.length; k++) {
        const b = BR[k], P = BRP[k], pg = clamp((F - b.a) / (b.b - b.a));
        if (pg <= 0.001) continue;
        const out = [];
        for (let i = 0; i < P.length; i++) {
          const g = P[i], j = Math.round(g.u * (N - 1));
          out.push({ x: g.x + g.ox * pg + boil.x[j], y: g.y + boil.y[j],
                     a: 0.78 * pg * (0.45 + 0.55 * Math.sqrt(Math.sin(Math.PI * g.q))), w: 0.42 + 0.34 * pg });
        }
        pen(c, out, 40 + k * 9, 1.0, 4.0, C.ink);
      }
      c.restore();

      // —— 拍4：屏上字（0.6 倍时长出），落在左侧留白，不抢裂缝
      const tp = clamp((lt - 0.60 * DUR) / 1.0);
      if (tp > 0.001) {
        c.textAlign = 'center'; c.textBaseline = 'middle';
        c.font = '500 92px "LXGWWenKai-500"';
        c.fillStyle = C.red;
        for (let i = 0; i < TXT.length; i++) {
          const g = TXT[i], q = clamp((tp - i * 0.16) / 0.6);
          if (q <= 0) continue;
          c.save();
          c.globalAlpha = 0.95 * q;
          c.translate(g.x, g.y - (1 - q) * 16);
          c.rotate(g.rot);
          c.beginPath(); c.rect(-74, -76, 148, 152 * q); c.clip();     // 从上往下“写”出来
          c.fillText(g.ch, 0, 0);
          c.restore();
        }
      }
    },
  };
})();
