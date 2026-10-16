// 页01 · 钩子：一只手按住一张还没裂开的纸 —— 掌心下先起一道极淡的压痕，再慢慢裂开、长出分叉，一路裂到纸的两端
SCENES['01'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ease, rng } = U;
  const DUR = 13;

  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F' };
  const sm = (x) => { const u = clamp(x, 0, 1); return u * u * (3 - 2 * u); };

  // ---------- 全片只有这一支笔：逐段变粗细、变浓淡，圆头，带轻微路径抖动 ----------
  function inkLine(c, pts, seed, jit, baseW) {
    const n = pts.length;
    if (n < 2) return;
    const r = rng(seed);
    const jx = new Float64Array(n), jy = new Float64Array(n);
    for (let i = 0; i < n; i++) { jx[i] = (r() * 2 - 1) * jit; jy[i] = (r() * 2 - 1) * jit; }
    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = C.ink;
    for (let i = 0; i < n - 1; i++) {
      const A = pts[i], B = pts[i + 1];
      const al = (A.a + B.a) * 0.5;
      if (al < 0.012) continue;
      c.globalAlpha = clamp(al, 0, 1);
      c.lineWidth = Math.max(0.75, baseW * (A.w + B.w) * 0.5);
      c.beginPath();
      c.moveTo(A.x + jx[i], A.y + jy[i]);
      c.lineTo(B.x + jx[i + 1], B.y + jy[i + 1]);
      c.stroke();
    }
    c.globalAlpha = 1;
  }

  // ============ 载体：一张横放的纸 ============
  const PX0 = 246, PY0 = 168, PX1 = 1674, PY1 = 830;
  const PW = PX1 - PX0, PH = PY1 - PY0;

  const EDGE = (() => {
    const seg = 22, pts = [];
    const add = (xa, ya, xb, yb) => { for (let i = 0; i < seg; i++) { const u = i / seg; pts.push({ x: lerp(xa, xb, u), y: lerp(ya, yb, u), a: 0.46, w: 1 }); } };
    add(PX0, PY0, PX1, PY0); add(PX1, PY0, PX1, PY1);
    add(PX1, PY1, PX0, PY1); add(PX0, PY1, PX0, PY0);
    return pts;
  })();

  // ============ 主角：纸面上一道裂缝（形态唯一，整页只沿自己生长） ============
  const MX0 = PX0 + 22, MX1 = PX1 - 22;              // 两端各离纸边 22px
  const MY = 452;                                     // 横贯高度
  const N = 168;
  const sX = (s) => lerp(MX0, MX1, s);
  const sY = (s) => MY
    + Math.sin(s * 6.75 + 0.60) * 23
    + Math.sin(s * 17.00 + 2.20) * 8.5
    + Math.sin(s * 28.60 + 4.10) * 3.4;
  const ORIGIN = 0.465;                               // 掌根落点：裂缝从这里起头，向两边裂
  const CRK = (() => {
    const out = [];
    for (let i = 0; i < N; i++) {
      const s = i / (N - 1);
      out.push({ s, x: sX(s), y: sY(s), tp: sm(Math.min(1, s / 0.05)) * sm(Math.min(1, (1 - s) / 0.05)) });
    }
    return out;
  })();

  // 分叉：每根都从主线长出、又收束回主线（近端连主线，远端自己收细）
  const BR = [
    { a: 0.245, b: 0.372, dir: -1, h: 17 },
    { a: 0.556, b: 0.690, dir:  1, h: 19 },
    { a: 0.762, b: 0.856, dir: -1, h: 13 },
    { a: 0.452, b: 0.508, dir: -1, h: 10 },
    { a: 0.502, b: 0.556, dir:  1, h:  9 },
  ];

  // ============ 手（只出手，不画脸） ============
  const HAND = (() => {
    const P = [];
    const put = (x, y) => P.push({ x, y });
    const Q = (x0, y0, cx, cy, x1, y1, n) => {
      for (let i = 1; i <= n; i++) {
        const u = i / n, m = 1 - u;
        put(m * m * x0 + 2 * m * u * cx + u * u * x1, m * m * y0 + 2 * m * u * cy + u * u * y1);
      }
    };
    put(826, -150);
    Q(826, -150, 798, 40, 800, 196, 8);          // 手背左缘
    Q(800, 196, 754, 238, 748, 302, 6);          // 拇指外侧
    Q(748, 302, 744, 350, 786, 346, 6);          // 拇指尖
    Q(786, 346, 814, 340, 810, 288, 5);          // 拇指内侧收回
    const B = 288;
    const F = [
      { l: 810, r: 864, tip: 412 },
      { l: 878, r: 932, tip: 434 },
      { l: 946, r: 1000, tip: 420 },
      { l: 1014, r: 1068, tip: 388 },
    ];
    for (let i = 0; i < F.length; i++) {
      const f = F[i];
      Q(f.l, B, f.l, f.tip, (f.l + f.r) / 2, f.tip + 3, 7);
      Q((f.l + f.r) / 2, f.tip + 3, f.r, f.tip, f.r, B, 7);
      if (i < F.length - 1) Q(f.r, B, (f.r + F[i + 1].l) / 2, B + 22, F[i + 1].l, B, 5);
    }
    Q(1068, B, 1082, 236, 1074, 192, 7);
    Q(1074, 192, 1066, 40, 1044, -150, 8);
    return P;
  })();

  const HAND_PATH = (() => {
    const p = new Path2D();
    p.moveTo(HAND[0].x, HAND[0].y);
    for (let i = 1; i < HAND.length; i++) p.lineTo(HAND[i].x, HAND[i].y);
    p.closePath();
    return p;
  })();

  const HAND_PEN = HAND.map((q, i) => ({
    x: q.x, y: q.y,
    a: 0.9,
    w: 0.85 + 0.5 * (0.5 + 0.5 * Math.sin(i * 0.55 + 1.2)),
  }));

  // 手上那几根内部线（指缝 / 拇指 / 掌背关节），同一支笔，末端淡出
  const INNER = (() => {
    const out = [];
    const B = 288;
    [[864, 878], [932, 946], [1000, 1014]].forEach((g, k) => {
      const x = (g[0] + g[1]) / 2, pts = [];
      for (let i = 0; i <= 7; i++) {
        const u = i / 7;
        pts.push({ x: x + Math.sin(u * 3.1) * 3, y: lerp(B + 20, B - 42, u), a: 0.42 * (1 - 0.7 * u), w: 0.72 });
      }
      out.push({ pts, seed: 700 + k });
    });
    const tp = [];
    for (let i = 0; i <= 7; i++) {
      const u = i / 7;
      tp.push({ x: lerp(812, 818, u), y: lerp(320, 198, u), a: 0.4 * (1 - 0.75 * u), w: 0.7 });
    }
    out.push({ pts: tp, seed: 730 });
    const kp = [];
    for (let i = 0; i <= 12; i++) {
      const u = i / 12;
      kp.push({ x: lerp(828, 1052, u), y: B - 70 - Math.sin(u * Math.PI) * 15 + Math.sin(u * 9.4) * 2.5, a: 0.3 * (1 - 0.55 * Math.abs(u - 0.5) * 2), w: 0.68 });
    }
    out.push({ pts: kp, seed: 760 });
    return out;
  })();

  // ============ 屏上字 ============
  const TXT = (() => {
    const r = rng(821);
    return ['还', '爱', '吗'].map((ch, i) => ({
      ch,
      x: 436 + i * 86 + (r() * 2 - 1) * 3,
      y: 722 + (r() * 2 - 1) * 5,
      r: (r() * 2 - 1) * 0.05,
    }));
  })();

  return {
    draw(c, lt, t, IMG) {
      const p = clamp(lt / DUR);

      // 每帧自己画背景
      c.fillStyle = C.bg;
      c.fillRect(0, 0, W, H);

      c.save();
      const z = lerp(1.0, 1.06, ease.inOut(p));          // 缓推
      c.translate(960, 540); c.scale(z, z); c.translate(-960, -540);

      // —— 纸：落影 + 平涂 + 轮廓
      c.globalAlpha = 0.10;
      c.fillStyle = C.gray;
      c.fillRect(PX0 + 16, PY0 + 18, PW, PH);
      c.globalAlpha = 1;
      c.fillStyle = C.paper;
      c.fillRect(PX0, PY0, PW, PH);
      inkLine(c, EDGE, 91, 1.0, 2.9);

      // —— 事件：裂缝的推进。分三段（先起头 → 掌根压下猛裂一下 → 慢慢裂到两端）
      const q = clamp(
        0.20 * sm(p / 0.20) +
        0.34 * sm((p - 0.26) / 0.18) +
        0.46 * sm((p - 0.48) / 0.32)
      );
      const frontL = ORIGIN - q * ORIGIN;                 // 左端裂到哪
      const frontR = ORIGIN + q * (1 - ORIGIN);           // 右端裂到哪
      const breath = 1 + 0.025 * Math.sin(t * 1.05);

      // 主线：同一道线，未裂处是极淡的压痕，裂过的地方浓、粗
      const cpts = new Array(N);
      for (let i = 0; i < N; i++) {
        const g = CRK[i];
        const A = g.s < ORIGIN ? sm((g.s - frontL) / 0.07) : sm((frontR - g.s) / 0.07);
        const head = sm(1 - Math.abs(g.s - ORIGIN) / 0.011) * 0.55;   // 起头的线头：第一帧就有
        const M2 = Math.max(A, head);
        cpts[i] = {
          x: g.x, y: g.y,
          a: (0.19 + 0.73 * M2) * (0.55 + 0.45 * g.tp),
          w: (0.50 + 0.85 * M2) * (0.35 + 0.65 * g.tp) * breath,
        };
      }
      inkLine(c, cpts, 13, 0.85, 4.4);

      // 分叉：跟着裂口前沿一起开，近端连着主线，远端自己收细
      for (let bi = 0; bi < BR.length; bi++) {
        const b = BR[bi];
        const nb = 44, bp = new Array(nb);
        for (let i = 0; i < nb; i++) {
          const u = i / (nb - 1);
          const s = lerp(b.a, b.b, u);
          const x = sX(s);
          const y = sY(s) + b.dir * b.h * Math.pow(Math.sin(Math.PI * u), 0.65);
          const A = s < ORIGIN ? sm((s - frontL) / 0.07) : sm((frontR - s) / 0.07);
          bp[i] = { x, y, a: 0.74 * A, w: 0.34 + 0.5 * A };
        }
        inkLine(c, bp, 40 + bi * 9, 1.0, 3.4);
      }

      // —— 手：压下去（事件2）→ 微抬（事件4），掌心落点始终压在裂缝起头处
      const press = sm((p - 0.24) / 0.10) * (1 - 0.4 * sm((p - 0.50) / 0.30));
      const hy = lerp(-30, 0, sm(p / 0.10)) + 12 * press;

      c.save();
      c.translate(0, hy);
      c.globalAlpha = 0.13;                                // 手落在纸上的影
      c.fillStyle = C.gray;
      c.save(); c.translate(7, 9); c.fill(HAND_PATH); c.restore();
      c.globalAlpha = 0.92;
      c.fillStyle = C.gray;
      c.fill(HAND_PATH);
      c.globalAlpha = 1;
      inkLine(c, HAND_PEN, 55, 1.0, 3.9);
      for (const L of INNER) inkLine(c, L.pts, L.seed, 0.9, 3.0);
      c.restore();

      // —— 屏上字：0.6 倍时长左右出，落在下半张纸的留白里，不抢重心
      const tp = clamp((lt - 0.60 * DUR) / 0.9);
      if (tp > 0.001) {
        c.save();
        c.globalAlpha = tp * 0.94;
        c.fillStyle = C.red;
        c.font = '500 78px "LXGWWenKai-500"';
        c.textBaseline = 'alphabetic';
        for (const g of TXT) {
          c.save();
          c.translate(g.x, g.y - (1 - tp) * 16);
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
