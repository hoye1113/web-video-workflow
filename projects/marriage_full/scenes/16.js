// 16：单图慢推（全程线性，末 10% 停稳）+ 文字两段依次浮现；本例无特写、无明暗揭示，第一帧即亮。
SCENES['16'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/16_1.png';
  const LINES = ['来回', '几小时'];
  const AT = [0.30, 0.62];
  return {
    draw(c, lt, t, IMG) {
      const D = 17, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));            // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色

      // ① 慢推：从量出的基准 z 线性推 7%，fx/fy 照抄给定的焦点
      const z = lerp(1.000, 1.070, pm);

      // ② 只有一张图，铺上去：焦点 (0.00, 0.50)
      MD.cover(c, IMG[P], { z, fx: 0.0, fy: 0.5 });

      // ③ 第 16/26 页，靠后，不用明暗揭示 —— 第一帧就是亮的

      // ④ 文字依次出现：0.30 / 0.62 两段，淡入 + 从下浮 14px，放在上方留白区
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 150, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, AT[i], 170 + i * 74));
    }
  };
})();
