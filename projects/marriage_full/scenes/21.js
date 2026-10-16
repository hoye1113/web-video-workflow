// 21｜真相拆解·回归≠修复：一张静图极慢线性推近（z 1.35→1.44，最后 10% 停稳），本页靠后不用明暗揭示、第一帧即亮；唯一自绘局部是纸上那道新折痕，0.40 单独沿同一折线长出来随即停住；文字「回归」「≠修复」在 0.30/0.62 依次淡入上浮。
SCENES['21'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/21_1.png';
  const LINES = ['回归', '≠修复'];
  // 纸上那道新折痕（归一化 u/v，量自 21_1.png 揉皱的纸面），沿同一折线逐段长出
  const CR = [[0.355, 0.500], [0.395, 0.470], [0.435, 0.485], [0.475, 0.448], [0.515, 0.462], [0.555, 0.428]];
  const LW = [2.2, 1.7, 2.3, 1.8, 2.1];   // 1.5~2.5 之间自然扰动
  return {
    draw(c, lt, t, IMG) {
      const D = 15, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));           // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色，第 0 帧图已铺好

      // ① 慢推：全程线性、几乎匀速（不套 easing），fx/fy 照抄量出来的焦点
      const geo = MD.cover(c, IMG[P], { z: lerp(1.350, 1.440, pm), fx: 0.99, fy: 0.00 });

      // ② 唯一自绘局部：折痕在 0.40 单独长出，沿同一折线逐段揭示后停住（不换身份）
      const g = ss(0.40, 0.56, p);
      if (g > 0) {
        c.save(); c.globalAlpha = 0.72; c.strokeStyle = '#1B1A17'; c.lineCap = 'round';
        const f = g * (CR.length - 1);
        for (let i = 0; i < CR.length - 1; i++) {
          const k = clamp(f - i); if (k <= 0) break;
          const [x0, y0] = MD.toScreen(geo, CR[i]);
          const [x1, y1] = MD.toScreen(geo, CR[i + 1]);
          c.lineWidth = LW[i];
          c.beginPath(); c.moveTo(x0, y0); c.lineTo(lerp(x0, x1, k), lerp(y0, y1, k)); c.stroke();
        }
        c.restore();
      }

      // ③ 文字依次出现：0.30 / 0.62，淡入 + 从下浮 14px，落在左下留白，不压主体
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 140, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, [0.30, 0.62][i], 210 + i * 76));
    }
  };
})();
