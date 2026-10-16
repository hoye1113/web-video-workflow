// 第24页「行动与落点」：静图 11s 慢推，z 1.00→1.07 全程线性推近，焦点用测量值 (0.00,0.50)；最后 10% 运动停稳；文字「只剩 / 情绪」在 0.30 / 0.62 依次淡入并从下浮起；本页在片子后段，不做明暗揭示，第一帧就是亮的；只有一张图，不做特写插入。
SCENES['24'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/24_1.png';
  const LINES = ['只剩', '情绪'];
  const AT = [0.30, 0.62];
  return {
    draw(c, lt, t, IMG) {
      const D = 11;
      const p = clamp(lt / D);            // 全页进度
      const pm = clamp(lt / (D * 0.9));   // 运动进度：最后 10% 停住

      // ① 兜底底色（图铺不满时才露出来）
      c.fillStyle = '#F3EDE2';
      c.fillRect(0, 0, W, H);

      // ② 慢推：从量出来的基准 z 线性推到 +7%，fx/fy 照抄焦点，不做 easing
      const z = lerp(1.000, 1.070, pm);
      MD.cover(c, IMG[P], { z, fx: 0.00, fy: 0.50 });

      // ③ 文字依次出现：淡入 + 从下方 14px 浮上来，落在画面左下留白，不压主体
      LINES.forEach((s, i) => {
        const k = ss(AT[i], AT[i] + 0.06, p);
        if (k <= 0) return;
        c.save();
        c.globalAlpha = k;
        c.fillStyle = '#1B1A17';
        c.font = '500 54px "LXGWWenKai-500"';
        c.textAlign = 'left';
        c.textBaseline = 'middle';
        c.fillText(s, 140, 210 + i * 76 + (1 - k) * 14);
        c.restore();
      });
    }
  };
})();
