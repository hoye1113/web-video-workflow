// 页03 · 钩子：一支铅笔沿着纸裂缝，一笔一笔画下三个小圈（上百个案例里挑出的三个故事）
SCENES['03'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ease, rng } = U;
  const DUR = 13;

  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F' };
  const sm = (x) => { const u = clamp(x, 0, 1); return u * u * (3 - 2 * u); };

  // ---------- 全片唯一一支笔：逐段变粗细、变浓淡、圆头、轻微路径抖动 ----------
  function pen(c, pts, seed, jit, baseW) {
    const n = pts.length;
    if (n < 2) return;
    const r = rng(seed);
    const jx = new Float64Array(n), jy = new Float64Array(n);
    for (let i = 0; i < n; i++) { jx[i] = (r() * 2 - 1) * jit; jy[i] = (r() * 2 - 1) * jit; }
    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = C.ink;
    for (let i = 0; i < n - 1; i++) {
      const A = pts[i], B = pts[i + 1];
      const al = (A.a + B.a) * 0.5;
      if (al < 0.02) continue;
      c.globalAlpha = clamp(al, 0, 1);
      c.lineWidth = Math.max(0.8, baseW * (A.w + B.w) * 0.5);
      c.beginPath();
      c.moveTo(A.x + jx[i], A.y + jy[i]);
      c.lineTo(B.x + jx[i + 1], B.y + jy[i + 1]);
      c.stroke();
    }
    c.globalAlpha = 1;
  }

  // ============ 载体：一张横铺的纸 ============
  const PX0 = 140, PY0 = 150, PX1 = 1780, PY1 = 930;
  const PW = PX1 - PX0, PH = PY1 - PY0;

  const EDGE = (() => {
    const pts = [];
    const add = (xa, ya, xb, yb) => {
      const n = Math.max(2, Math.round(Math.hypot(xb - xa, yb - ya) / 92));
      for (let i = 0; i < n; i++) { const u = i / n; pts.push({ x: lerp(xa, xb, u), y: lerp(ya, yb, u), a: 0.42, w: 1 }); }
    };
    add(PX0, PY0, PX1, PY0); add(PX1, PY0, PX1, PY1);
    add(PX1, PY1, PX0, PY1); add(PX0, PY1, PX0, PY0);
    return pts;
  })();

  // ============ 背景上的那道纸裂缝（页01/02 同一道，这里是旁边的东西，不抢主角） ============
  const CX0 = PX0 + 26, CX1 = PX1 - 26, CY = 330;    // 两端各离纸边 26px
  const crkY = (s) => CY
    + Math.sin(s * 5.60 + 0.70) * 15
    + Math.sin(s * 13.20 + 2.30) * 5.5
    + Math.sin(s * 27.30 + 4.10) * 2.2;
  const NC = 190;
  const CRACK = (() => {
    const out = [];
    for (let i = 0; i < NC; i++) {
      const s = i / (NC - 1);
      out.push({
        x: lerp(CX0, CX1, s), y: crkY(s),
        a: 0.74 * sm(Math.min(1, s / 0.045)) * sm(Math.min(1, (1 - s) / 0.045)),
        w: 0.78 + 0.22 * Math.sin(s * 9.4 + 0.5),
      });
    }
    return out;
  })();

  // 分叉：每根都从主线长出、又收束回主线
  const BRANCH = [
    { a: 0.19, b: 0.30, dir: -1, h: 32 },
    { a: 0.57, b: 0.69, dir:  1, h: 27 },
    { a: 0.42, b: 0.49, dir: -1, h: 15 },
  ];
  const BR_PTS = BRANCH.map((b) => {
    const nb = 40, out = [];
    for (let i = 0; i < nb; i++) {
      const u = i / (nb - 1), s = lerp(b.a, b.b, u);
      out.push({
        x: lerp(CX0, CX1, s),
        y: crkY(s) + b.dir * b.h * Math.pow(Math.sin(Math.PI * u), 0.7),
        a: 0.58 * Math.pow(Math.sin(Math.PI * u), 0.8),
        w: 0.52 + 0.30 * Math.sin(Math.PI * u),
      });
    }
    return out;
  });

  // ============ 三个小圈（这页要讲的东西：三个最典型的故事） ============
  const CIR = [
    { x: 540,  y: 740, r: 82 },
    { x: 900,  y: 704, r: 88 },
    { x: 1262, y: 734, r: 80 },
  ];
  const OVS = 0.30;                       // 手绘圈收笔时多绕一点（过冲）
  const NP = 148;
  const CIRCLES = CIR.map((o, i) => {
    const pts = [];
    for (let k = 0; k < NP; k++) {
      const q = k / (NP - 1);
      const phi = -Math.PI / 2 - (TAU + OVS) * q;      // 从正上方起笔，顺时针
      const rr = o.r * (1 + 0.022 * Math.sin(phi * 3 + i * 2.1) + 0.012 * Math.sin(phi * 5 + i * 1.3));
      pts.push({ phi, x: o.x + Math.cos(phi) * rr, y: o.y + Math.sin(phi) * rr });
    }
    return pts;
  });

  // ============ 节奏 ============
  const SEQ = [ { t: 0.35, d: 2.05 }, { t: 3.20, d: 2.05 }, { t: 6.05, d: 2.05 } ];
  const LIFT_T = 8.10, EXIT_T = 8.65, EXIT_END = 12.55, TXT_T = 7.75;

  // 笔尖：按下 → 画第一个圈 → 抬到第二个圈 → … → 画完抬笔退出画面
  function tipAt(lt) {
    if (lt < SEQ[0].t) {
      const u = ease.out(clamp(lt / SEQ[0].t));
      const P = CIRCLES[0][0];
      return { x: P.x, y: P.y - 22 * (1 - u) };
    }
    for (let i = 0; i < 3; i++) {
      const s = SEQ[i], q = (lt - s.t) / s.d;
      if (q >= 0 && q < 1) {
        const k = q * (NP - 1), k0 = Math.min(NP - 2, Math.floor(k)), f = k - k0;
        const A = CIRCLES[i][k0], B = CIRCLES[i][k0 + 1];
        return { x: lerp(A.x, B.x, f), y: lerp(A.y, B.y, f) };
      }
      const nx = SEQ[i + 1];
      if (nx && lt < nx.t) {
        const u = ease.inOut(clamp((lt - (s.t + s.d)) / (nx.t - (s.t + s.d))));
        const A = CIRCLES[i][NP - 1], B = CIRCLES[i + 1][0];
        return { x: lerp(A.x, B.x, u), y: lerp(A.y, B.y, u) - 24 * Math.sin(Math.PI * u) };
      }
    }
    const A = CIRCLES[2][NP - 1];
    const lift = sm((lt - LIFT_T) / 0.80);
    const out = ease.in(clamp((lt - EXIT_T) / (EXIT_END - EXIT_T)));
    return { x: A.x + 760 * out, y: A.y - 34 * lift - 500 * out };
  }

  // ============ 主角：一支铅笔（形态唯一，整页只沿自己动） ============
  const HW = 27, TL = 112, PL = 900, GX = 24, GW = 7.5;
  const TAIL = [];
  for (let i = 0; i <= 12; i++) { const q = i / 12; TAIL.push([PL - 26 + 34 * Math.sin(Math.PI * q), -HW + 2 * HW * q]); }
  const BODY_PATH = U.poly([[TL, -HW]].concat(TAIL).concat([[TL, HW]]), true);
  const WOOD_PATH = U.poly([[GX, -GW], [TL, -HW], [TL, HW], [GX, GW]], true);
  const TIP_PATH  = U.poly([[0, 0], [GX, -GW], [GX, GW]], true);
  const OUTLINE = (() => {
    const P = [];
    const put = (x, y, w) => P.push({ x, y, a: 1, w });
    put(0, 0, 0.60);
    put(GX, -GW, 0.70);
    put(TL, -HW, 1);
    for (let i = 0; i < TAIL.length; i++) put(TAIL[i][0], TAIL[i][1], 1);
    put(TL, HW, 1);
    put(GX, GW, 0.70);
    put(0, 0, 0.60);
    return P;
  })();
  const OUT_PATH = U.poly(OUTLINE.map(p => [p.x, p.y]), true);
  const FACET = (() => {
    const P = [];
    for (let i = 0; i <= 16; i++) {
      const q = i / 16;
      P.push({
        x: lerp(TL + 18, PL - 44, q), y: -HW * 0.36 + Math.sin(q * 3.2) * 1.1,
        a: 0.30 * sm(Math.min(1, q / 0.14)) * sm(Math.min(1, (1 - q) / 0.20)),
        w: 0.66,
      });
    }
    return P;
  })();

  // ============ 屏上字 ============
  const TXT = (() => {
    const r = rng(815);
    return ['三', '个', '故', '事'].map((ch, i) => ({
      ch,
      x: 246 + i * 84 + (r() * 2 - 1) * 3,
      y: 258 + (r() * 2 - 1) * 5,
      r: (r() * 2 - 1) * 0.05,
    }));
  })();

  return {
    draw(c, lt, t, IMG) {
      const p = clamp(lt / DUR);

      // 每帧自己画底
      c.fillStyle = C.bg;
      c.fillRect(0, 0, W, H);

      // 镜头横移（整片横着走）
      c.save();
      c.translate(lerp(-110, 110, ease.inOut(p)), 0);

      // —— 纸：落影 + 平涂 + 轮廓（阴影统一朝右下）
      c.globalAlpha = 0.10;
      c.fillStyle = C.gray;
      c.fillRect(PX0 + 14, PY0 + 16, PW, PH);
      c.globalAlpha = 1;
      c.fillStyle = C.paper;
      c.fillRect(PX0, PY0, PW, PH);
      pen(c, EDGE, 91, 1.0, 2.6);

      // —— 纸裂缝（旁边的背景，不抢主角）
      pen(c, CRACK, 13, 0.85, 4.4);
      for (let i = 0; i < BR_PTS.length; i++) pen(c, BR_PTS[i], 40 + i * 9, 0.9, 3.6);

      // —— 三个小圈：一笔一笔画上去；起笔前先有一道极淡的压痕
      for (let i = 0; i < 3; i++) {
        const P = CIRCLES[i];
        const q = clamp((lt - SEQ[i].t) / SEQ[i].d);
        const head = q * (NP - 1);
        const path = [];
        for (let k = 0; k < NP; k++) {
          let a = 0;
          if (k <= head + 0.0001) a = 0.92;
          else if (i === 0 && k <= 24) a = 0.20 * (1 - 0.30 * (k / 24));
          if (a < 0.02) continue;
          path.push({ x: P[k].x, y: P[k].y, a, w: 0.72 + 0.34 * Math.sin(P[k].phi * 4.2 + i) });
        }
        if (path.length > 1) pen(c, path, 500 + i * 37, 0.9, 3.7);
      }

      // —— 铅笔：笔尖始终对着圈的笔头，笔身随手腕小幅摆动
      const tip = tipAt(lt);
      const ang = -0.593 + 0.13 * Math.sin(lt * 0.85);

      c.save();                                            // 铅笔落在纸上的影
      c.translate(tip.x + 10, tip.y + 12);
      c.rotate(ang);
      c.globalAlpha = 0.12;
      c.fillStyle = C.gray;
      c.fill(OUT_PATH);
      c.globalAlpha = 1;
      c.restore();

      c.save();
      c.translate(tip.x, tip.y);
      c.rotate(ang);
      c.fillStyle = C.ink;  c.fill(TIP_PATH);              // 石墨尖
      c.fillStyle = C.bg;   c.fill(WOOD_PATH);             // 削开的木头
      c.fillStyle = C.red;  c.fill(BODY_PATH);             // 笔杆
      pen(c, OUTLINE, 700, 0.9, 4.0);                      // 同一支笔勾轮廓
      pen(c, FACET, 760, 0.8, 3.0);                        // 笔杆棱面线
      c.restore();

      // —— 屏上字：0.6 倍时长出，落在左上留白，不抢重心
      const tp = clamp((lt - TXT_T) / 0.9);
      if (tp > 0.001) {
        c.save();
        c.globalAlpha = tp * 0.95;
        c.fillStyle = C.red;
        c.font = '500 74px "LXGWWenKai-500"';
        c.textBaseline = 'alphabetic';
        for (const g of TXT) {
          c.save();
          c.translate(g.x, g.y - (1 - tp) * 14);
          c.rotate(g.r);
          c.fillText(g.ch, 0, 0);
          c.restore();
        }
        c.restore();
      }

      c.restore();
    },
  };
})();
