// 17｜反直觉结论：慢推全程线性（最后 10% 停稳）+ 纸上裂缝在 0.40 单独自背影中段往上长开 + 屏上字后段浮出
SCENES['17'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/17_1.png';
  const LINE = "不是在享受";
  // 裂缝：压在背影中线、贴着纸缝沿同一形态自下往上长大（固定折线，不换身份）
  const CR = [[962,776],[944,722],[974,674],[950,622],[986,574],[958,522],[992,474],[962,422],[936,374],[968,322],[946,274]];
  const LW = [2.4, 1.7, 2.2, 1.6, 2.3, 1.8, 2.4, 1.7, 2.1, 1.9]; // 1.5~2.5 之间自然扰动
  return {
    draw(c, lt, t, IMG) {
      const D = 17, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));                 // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);

      // ① 慢推：全程线性，从量出的基准 z 再推 7%；fx/fy 照抄给定焦点
      MD.cover(c, IMG[P], { z: lerp(1.000, 1.070, pm), fx: 0.50, fy: 0.50 });

      // ② 裂缝 0.40 单独长出来，沿同一折线逐段揭示，从背影中段往上裂开
      const g = ss(0.40, 0.72, p);
      if (g > 0) {
        c.save(); c.globalAlpha = 0.85; c.strokeStyle = '#1B1A17';
        c.lineCap = 'round';
        const f = g * (CR.length - 1);
        for (let i = 0; i < CR.length - 1; i++) {
          const k = clamp(f - i); if (k <= 0) break;
          c.lineWidth = LW[i];
          c.beginPath();
          c.moveTo(CR[i][0], CR[i][1]);
          c.lineTo(lerp(CR[i][0], CR[i + 1][0], k), lerp(CR[i][1], CR[i + 1][1], k));
          c.stroke();
        }
        c.restore();
      }

      // ③ 文字 0.30 淡入 + 从下方 14px 浮上来，落在左下留白，不压主体
      const k = ss(0.30, 0.36, p);
      if (k > 0) {
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(LINE, 140, 210 + (1 - k) * 14);
        c.restore();
      }
    }
  };
})();
