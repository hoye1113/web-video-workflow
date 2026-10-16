// 第20页·真相拆解：一条手绘曲线冲上纸顶、又长长地沉下去（短期情绪麻醉）——第一帧压痕在场并已起头，0~0.3*dur 冲高、0.3~0.82*dur 长沉、0.60*dur 出字、0.85*dur 尾端继续往下沉收束；镜头全程拉远。
SCENES['20'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', gray: '#6B655B', red: '#C8402F', teal: '#2F5D62' };
  const DUR = 12;
  // 主角＝曲线本身：宽 PX1-PX0 = 1204px（画面 63%），高 760px（画面 70%）；纸只是载体
  const PX0 = 356, PX1 = 1560, PBASE = 920, PTOP = 160, N = 300;   // 峰值在 u=0.2（曲线 20% 处冲到顶）

  // 曲线骨架：0~0.2 快冲（那口劲），0.2~1 长长沉下，峰顶是圆头不是尖角
  const BASE = [];
  {
    const r = rng(2001);
    for (let i = 0; i <= N; i++) {
      const u = i / N;
      const h = u < 0.2 ? 1 - Math.pow(1 - u / 0.2, 1.7) : Math.exp(-2.6 * Math.pow(u - 0.2, 1.1));
      BASE.push([lerp(PX0, PX1, u) + (r() * 2 - 1) * 2.2,
                 PBASE - h * (PBASE - PTOP) + (r() * 2 - 1) * 2.2]);
    }
  }
  // 全片同一支笔：分段描边，线宽 1.5~2.5 倍自然顿挫，圆头圆角，不换第二套笔触
  const pen = (c, pts, w, seed, taper, a) => {
    if (!pts || pts.length < 2) return;
    const r = rng(seed);
    c.save(); c.globalAlpha = a === undefined ? 1 : a; c.strokeStyle = C.ink;
    c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      const s = i / (pts.length - 1), tp = taper ? clamp((1 - s) / taper) : 1;
      c.lineWidth = w * (0.8 + r() * 0.5) * (0.4 + 0.6 * tp);
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };
  // 手画的横线：固定抖动（不随帧变，否则线会逐帧发颤）
  const JIT = (() => { const r = rng(181), o = []; for (let i = 0; i < 64; i++) o.push((r() - 0.5) * 3.0); return o; })();
  const flat = (x0, x1, y, n) => {
    const o = []; for (let i = 0; i <= n; i++) o.push([lerp(x0, x1, i / n), y + JIT[i % 64]]); return o;
  };
  // 屏上字：逐字浮出、逐字微微抖，像同一支笔写的
  const TXT = '短期情绪麻醉';
  const handText = (c, s, xR, y, size, a) => {
    const r = rng(11), ws = []; let tw = 0;
    c.save(); c.fillStyle = C.ink; c.font = '500 ' + size + 'px "LXGWWenKai-500"'; c.textBaseline = 'middle';
    for (const ch of s) { const w = c.measureText(ch).width; ws.push(w); tw += w + size * 0.05; }
    let x = xR - tw;
    for (let i = 0; i < s.length; i++) {
      const ca = clamp(a * 1.7 - i * 0.13), w = ws[i];
      if (ca > 0.01) {
        c.save(); c.globalAlpha = ca; c.translate(x + w / 2, y + (r() - 0.5) * 5 + (1 - ca) * 10);
        c.rotate((r() - 0.5) * 0.045); c.fillText(s[i], -w / 2, 0); c.restore();
      }
      x += w + size * 0.05;
    }
    c.restore();
  };

  return {
    draw(c, lt, t, IMG) {
      const p = clamp(lt / DUR);
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                       // 每帧自己画背景

      const z = lerp(1.16, 0.95, ease.inOut(p));                        // 镜头：全程拉远
      c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.rotate(-0.019); c.translate(-W / 2, -H / 2);

      // ① 载体：一张纸（微微歪一点，第一帧就在）
      c.fillStyle = C.paper; c.fillRect(300, 110, 1320, 870);
      c.save(); c.globalAlpha = 0.16; c.strokeStyle = C.gray; c.lineWidth = 2.6;
      c.strokeRect(300, 110, 1320, 870); c.restore();

      // ② 现实线（红，曲线上不去也躲不开；末了尾端还要往下沉）
      const BL = flat(PX0, PX1, PBASE, 60), br = rng(909);
      c.save(); c.globalAlpha = 0.5; c.strokeStyle = C.red; c.lineCap = 'round'; c.lineJoin = 'round';
      for (let i = 1; i < BL.length; i++) {
        c.lineWidth = 3.4 * (0.8 + br() * 0.5);
        c.beginPath(); c.moveTo(BL[i - 1][0], BL[i - 1][1]); c.lineTo(BL[i][0], BL[i][1]); c.stroke();
      }
      c.restore();

      // ③ 生长进度：0~0.3 冲上纸顶 → 0.3~0.82 长长沉下 → 末段收束
      let uTip;
      if (lt < 3.6) uTip = 0.014 + 0.186 * ease.out(clamp(lt / 3.6));
      else if (lt < 9.9) uTip = 0.20 + 0.78 * ease.inOut(clamp((lt - 3.6) / 6.3));
      else uTip = 0.98 + 0.02 * ease.out(clamp((lt - 9.9) / 2.1));
      const k = clamp(Math.round(uTip * N), 4, N);

      // 同一个形状继续长大／变形：末段整体往现实线上沉，不换身份
      const dip = 62 * ss(9.4, 11.9, lt);
      const P = new Array(N + 1);
      for (let i = 0; i <= N; i++) P[i] = [BASE[i][0], BASE[i][1] + dip * ss(0.70, 1.0, i / N)];

      // ④ 第一帧就交代主角与走向：整条曲线的极淡铅笔压痕
      pen(c, BASE, 2.6, 700, 0, lerp(0.16, 0.05, clamp(lt / 9)));

      // ⑤ 主角：同一支笔从起点沿同一形态长出来，笔尖收细
      pen(c, P.slice(0, k + 1), 6.2, 2020, 0.12, 0.95);

      c.restore();

      // ⑥ 0.60*dur 出字，落在右上留白，不抢重心
      const pt = ss(7.2, 8.1, lt);
      if (pt > 0.01) handText(c, TXT, 1540, 286, 54, pt);
    }
  };
})();
