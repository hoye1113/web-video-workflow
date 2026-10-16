// 11 案例二·刘先生：一条平缓的灰线（婚姻的平淡）横铺在画面下方，一条上下跳动的红亮线（刺激）从它的中点一路抖动地窜起； 主角=那条红亮线（高 640px，占画面高 59%），灰平线只是旁边的参照/载体，别让它抢戏。节奏：0.0s 灰线已从落点向两侧铺开、红线冒头 → 0.17*dur 灰线铺满 → 0.55*dur 红线升到顶（全程左右震、顶端上下跳）→ 0.6*dur 手写「拿平淡做对比」落在左上留白 → 0.75*dur 抖动加剧收束。镜头缓推。
SCENES['11'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg:'#F3EDE2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F' };
  const DUR = 16;
  const XL = 200, XR = 1740, X0 = 1180, Y0 = 780, TOP = 140;   // 平线两端 / 红线落点 / 基线 / 线顶
  const TXT = '拿平淡做对比';

  // 同一支笔：折线分段描边，线宽在 1.5~2.5 倍之间自然顿挫，圆头连接（不是矢量等宽线）
  const pen = (c, pts, col, w, seed) => {
    const r = rng(seed);
    c.save(); c.strokeStyle = col; c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      c.lineWidth = w * (0.75 + r() * 0.75);
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };

  return {
    draw(c, lt) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                 // 每帧自己画背景
      // 镜头缓推：全程线性、末尾收稳，朝主角（右侧竖线）轻推
      const z = lerp(1.0, 1.10, clamp(lt / (DUR * 0.92)));
      c.save(); c.translate(1060, 480); c.scale(z, z); c.translate(-1060, -480);

      // ① 灰平线（参照/载体）：从红线落点向两侧铺开——第一帧就有一小段，画面不空
      const fp = 0.06 + 0.94 * ease.out(clamp(lt / (0.17 * DUR)));
      const xa = X0 - (X0 - XL) * fp, xb = X0 + (XR - X0) * fp;
      const flat = [];
      for (let i = 0; i <= 30; i++) {
        const x = xa + (xb - xa) * (i / 30);
        flat.push([x, Y0 + 2.4 * Math.sin(x * 0.011 + 0.7)]);     // 低频微起伏：干净连续，仍读作一条平线
      }
      pen(c, flat, C.gray, 3.0, 11);

      // ② 红亮线（主角）：从基线上窜，边升边左右抖动，顶端上下跳；后段抖动加剧
      const rise = 0.08 + 0.92 * ease.out(clamp(lt / (0.55 * DUR)));
      const inten = ss(0.75 * DUR, 0.95 * DUR, lt);
      const bob = 0.5 + 0.5 * Math.sin(lt * (3.4 + 2.6 * inten) + 0.4);
      const topY = Y0 - (Y0 - TOP) * rise * (0.86 + 0.14 * bob);
      const red = [];
      for (let i = 0; i <= 26; i++) {
        const s = i / 26;                                          // 同一形态沿自身长大：s=0 在基线，s=1 在顶端
        const amp = (2 + 30 * Math.pow(s, 1.3)) * (0.35 + 0.65 * rise) * (1 + 0.55 * inten);
        const wob = Math.sin(s * 3.4 - lt * 2.4) + 0.35 * Math.sin(s * 8.0 + lt * 3.7);
        const rip = 7 * Math.pow(s, 0.7) * Math.sin(s * 6.2 + lt * 3.0) * (0.5 + 0.5 * rise);
        red.push([X0 + amp * wob, Y0 + s * (topY - Y0) + rip]);
      }
      pen(c, red, C.red, 5.0, 23);
      c.restore();

      // ③ 0.6*dur：屏上字，手写体，落在左上留白，不抢画面重心
      const pt = ss(9.2, 10.8, lt);
      if (pt > 0.01) {
        c.save(); c.font = '500 56px \"LXGWWenKai-500\"';
        c.fillStyle = C.ink; c.textAlign = 'left'; c.textBaseline = 'middle';
        let tx = 170;
        for (let i = 0; i < TXT.length; i++) {
          const cw = c.measureText(TXT[i]).width;
          const k = clamp(pt * 1.5 - i * 0.09);                    // 逐字手写式浮现
          if (k > 0.01) {
            c.globalAlpha = 0.92 * k;
            c.save(); c.translate(tx, 250 + (1 - k) * 16);
            c.fillText(TXT[i], 0, 0); c.restore();
          }
          tx += cw + 8;
        }
        c.restore();
      }
    }
  };
})();
