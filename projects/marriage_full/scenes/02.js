// 页02｜钩子：一道纸裂缝从纸的底边慢慢往上爬，缝里露出后面的暗色，屏上字「窗户纸」
SCENES['02'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', gray: '#6B655B', red: '#C8402F', teal: '#2F5D62' };
  const LW = 4.5;                                    // 一支笔：全页只有一个线宽

  // ---------- 纸：一张略斜的纸，四周留白 ----------
  const SX = 400, SY = 120, SW = 1180, SH = 860, SR = 16;
  const CX = SX + SW / 2, CY = SY + SH / 2;
  const sheet = (() => {
    const p = new Path2D();
    p.moveTo(SX + SR, SY);
    p.arcTo(SX + SW, SY, SX + SW, SY + SH, SR);
    p.arcTo(SX + SW, SY + SH, SX, SY + SH, SR);
    p.arcTo(SX, SY + SH, SX, SY, SR);
    p.arcTo(SX, SY, SX + SW, SY, SR);
    p.closePath(); return p;
  })();
  const ink = (c, path, fill, lw = LW) => {
    if (fill) { c.fillStyle = fill; c.fill(path); }
    if (lw) { c.strokeStyle = C.ink; c.lineWidth = lw; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(path); }
  };

  // ---------- 裂缝中心线：从纸的下边缘起，一路往上爬（占纸面约六成六），整体贴着纸的中央竖轴 ----------
  const N = 46, BY = SY + SH, TY = BY - SH * 0.66;
  const CL = [];
  {
    const r = rng(2026);
    let zig = 0;
    for (let i = 0; i < N; i++) {
      const u = i / (N - 1);
      const y = lerp(BY, TY, Math.pow(u, 1.02));
      const base = lerp(1030, 992, Math.pow(u, 0.9));        // 起点落在纸的中央竖轴附近，往上略往左
      const wob = Math.sin(u * 3.4 + 0.5) * 13 + Math.sin(u * 6.9 + 1.7) * 7;   // 平缓的走向
      zig = zig * 0.78 + (r() * 2 - 1) * 2.6;                // 撕裂的细毛边：接着上一点走，不是逐点锯齿
      CL.push([base + wob + zig, y]);
    }
  }
  const NM = [];
  for (let i = 0; i < N; i++) {
    const a = CL[Math.max(0, i - 1)], b = CL[Math.min(N - 1, i + 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1], d = Math.sqrt(dx * dx + dy * dy) || 1;
    NM.push([-dy / d, dx / d]);                              // 法线（指向右）
  }

  // ---------- 裂缝什么时候爬到哪个位置（这一页的四拍）----------
  const KEY = [[0, 0, 0.7], [2.6, 0.40, 1], [3.1, 0.43, 1], [7.0, 0.90, 1], [9.0, 1.0, 1]];
  const crackAt = (x) => {
    if (x <= 0) return 0;
    for (let i = 0; i < KEY.length - 1; i++) {
      const ta = KEY[i][0], va = KEY[i][1], tb = KEY[i + 1][0], vb = KEY[i + 1][1];
      if (x <= tb) return lerp(va, vb, Math.pow(clamp((x - ta) / (tb - ta)), KEY[i][2]));
    }
    return 1;
  };

  // ---------- 缝口宽度 / 纸纹（种子随机，全部固定）----------
  const OMAX = 16;                                    // 缝口张开的半宽：满开时约纸宽的 2%–3%
  const OA = [], GR = [];
  {
    const r = rng(77);
    let a = 0, b = 0;
    for (let i = 0; i < N; i++) {
      a = a * 0.82 + (r() * 2 - 1) * 0.16;             // 两片纸的错口：低频慢慢错开，不逐点乱跳
      b = b * 0.82 + (r() * 2 - 1) * 0.16;
      OA.push([1 + a, 1 + b]);
    }
    for (let k = 0; k < 44; k++) GR.push({ x: r(), y: r(), a: 0.05 + r() * 0.09, s: 1.6 + r() * 2.8 });
  }

  // ---------- 屏上字：窗户纸（竖排，一笔一笔写出来）----------
  const LAB = ['窗', '户', '纸'];
  const drawLabel = (c, lt) => {
    c.save();
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillStyle = C.ink;
    c.font = '600 108px "LXGWWenKai-500"';
    for (let i = 0; i < LAB.length; i++) {
      const st = 6.55 + i * 0.42;
      const q = ss(st, st + 0.55, lt);
      if (q <= 0) continue;
      const x = 212, y = 372 + i * 152;
      c.save();
      c.beginPath(); c.rect(x - 78, y - 84, 156, 168 * q); c.clip();     // 从上往下写出来
      c.globalAlpha = ss(st, st + 0.32, lt);
      c.fillText(LAB[i], x, y + (1 - q) * 10);
      c.restore();
    }
    c.restore();
  };

  return {
    draw(c, lt, t) {
      const g = crackAt(lt);                                   // 裂缝爬到哪儿（0..1）
      const fr = Math.floor(lt * 12);                          // 12fps 的手绘抖笔
      const bl = (i) => (U.hash(Math.floor(i / 3) * 131 + 7, fr) * 2 - 1) * 1.4;   // 同一支笔、12fps 抖笔：沿缝低频，整条一起动

      // 1) 背景（每帧自己画）
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);

      // 2) 纸落下来、轻轻转正（镜头是停的，动的是纸自己）
      const set = ease.out(clamp((lt - 0.15) / 1.4));
      const ang = (1 - set) * -0.052 + Math.sin(lt * 7.6) * 0.011 * (1 - set);
      c.save();
      c.translate(CX, CY);
      c.rotate(ang);
      c.translate(-CX, -CY - (1 - set) * 34);

      // 3) 纸下的影：一层暖灰平涂（色板里的 #6B655B），方向统一右下，不叠偏蓝的层
      c.save();
      c.globalAlpha = 0.10 * (0.35 + 0.65 * set);
      c.fillStyle = C.gray;
      c.translate(22, 26); c.fill(sheet);
      c.restore();

      // 4) 纸面
      c.save();
      c.clip(sheet);
      c.fillStyle = C.paper; c.fillRect(SX - 60, SY - 60, SW + 120, SH + 120);
      c.fillStyle = C.gray;
      for (const p of GR) { c.globalAlpha = p.a; c.beginPath(); c.arc(SX + p.x * SW, SY + p.y * SH, p.s * 0.5, 0, TAU); c.fill(); }
      c.globalAlpha = 1;

      // 5) 裂缝：尖端先过去，两片纸才慢慢让开；缝里露出后面的暗色
      const f = g * (N - 1);
      const k = Math.max(0, Math.min(Math.floor(f), N - 2));
      const ti = clamp(f - k, 0, 1);                            // 尖端落在 CL[k] → CL[k+1] 之间
      const OL = [], OR = [];
      for (let i = 0; i <= k; i++) {
        const u = i / (N - 1);
        const pass = clamp((f - i) / 4.2);                                   // 尖端过去后 4.2 个点才张开
        const mouth = Math.pow(ss(0, 0.05, u), 0.75);                        // 贴纸边那一段收成尖口：从纸边起裂
        const wide = OMAX * mouth * ss(0, 1, pass) * lerp(0.9, 1.1, ss(6, 10, lt));
        OL.push(Math.max(0, wide * OA[i][0]));
        OR.push(Math.max(0, wide * OA[i][1]));
      }
      // 中心线 + 左右两条缘：沿中心线对称张开，同一次手抖整体位移，不产生错位重影
      const LP = [], RP = [];
      for (let i = 0; i <= k; i++) {
        const tr = bl(i);
        const px = CL[i][0] + NM[i][0] * tr, py = CL[i][1] + NM[i][1] * tr;
        LP.push([px - NM[i][0] * OL[i], py - NM[i][1] * OL[i]]);
        RP.push([px + NM[i][0] * OR[i], py + NM[i][1] * OR[i]]);
      }
      const tip = [lerp(CL[k][0], CL[k + 1][0], ti), lerp(CL[k][1], CL[k + 1][1], ti)];

      // 6) 一条 path 画完整道缝：左缘上行 → 尖端锥形收细 → 右缘下行。
      //    纯负形缺口：缝里就是底衬的暗色，靠它和纸底色的对比立住裂口，不再描一圈深色外轮廓
      if (g > 0.001) {
        const tear = new Path2D();
        tear.moveTo(LP[0][0], LP[0][1]);
        for (let i = 1; i <= k; i++) tear.lineTo(LP[i][0], LP[i][1]);
        tear.lineTo(tip[0], tip[1]);
        for (let i = k; i >= 0; i--) tear.lineTo(RP[i][0], RP[i][1]);
        tear.closePath();
        c.fillStyle = C.teal; c.fill(tear);
        // 裂口边缘只勾一条细铅笔线：和纸的轮廓同一支笔、同一线宽
        c.strokeStyle = C.ink; c.lineWidth = LW; c.lineJoin = 'round'; c.lineCap = 'round';
        c.stroke(tear);
      }
      c.restore();                                   // 结束纸面裁剪

      // 7) 纸的轮廓（细铅笔线）
      ink(c, sheet, null);
      c.restore();                                   // 结束纸的位移/旋转

      // 8) 屏上字
      drawLabel(c, lt);
    },
  };
})();
