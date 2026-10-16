// 第01页·钩子：单图全程线性慢推(z 1.02→1.09, 焦点 fx1.00/fy0.00) + 开篇 6% 明暗揭示 + 屏上字后段浮现，最后 10% 停稳
SCENES['01'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/01_1.png';
  const LINES = ["还会爱吗"];
  return {
    draw(c, lt, t, IMG) {
      const D = 13, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));       // 运动进度：最后 10% 停住

      // ① 每帧先铺底色（图铺不满时露出来的兜底）
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);

      // ② 慢推：全程匀速，用 pm 直接线性不套 easing；z 用给定的 1.02→1.09，fx/fy 照抄量出来的焦点
      const z = lerp(1.02, 1.09, pm);
      MD.cover(c, IMG[P], { z, fx: 1.00, fy: 0.00 });

      // ③ 明暗揭示：开头 0~0.06 由暗到亮，像灯慢慢打开（全片第 1 页，开篇可用）
      const dark = 1 - ss(0, 0.06, p);
      if (dark > 0) {
        c.fillStyle = `rgba(20,16,12,${(0.65 * dark).toFixed(3)})`;
        c.fillRect(0, 0, W, H);
      }

      // ④ 本页只有一张图，跳过细节插入
      // ⑤ 屏上字：无标点拆不开，单条在后段浮现；淡入 0.06 + 从下浮 14px，放左下留白，不压主体(0.65,0.34)
      LINES.forEach((s, i) => {
        const at = [0.30, 0.62, 0.85][i] || 0.85;
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 140, 210 + i * 76 + (1 - k) * 14);
        c.restore();
      });
    }
  };
})();
