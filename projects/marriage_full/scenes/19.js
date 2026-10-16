// 第19页·真相拆解：一张静图线性缓推 z 1.150→1.230（fx0.5/fy0.0 照量出来的焦点），第19/26页已过开篇故不用明暗揭示、第一帧就是亮的，文字「不是谁更爱谁」在 0.30 淡入并自下方 14px 浮起，最后 10% 运动停稳收尾。
SCENES['19'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/19_1.png';
  return {
    draw(c, lt, t, IMG) {
      const D = 12, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));   // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色

      // ① 慢推：全程线性、几乎匀速，不套 easing
      MD.cover(c, IMG[P], { z: lerp(1.150, 1.230, pm), fx: 0.5, fy: 0.0 });

      // ② 文字：0.30 淡入 + 从下 14px 浮上来，落在主体下方的留白
      const k = ss(0.30, 0.36, p);
      if (k > 0) {
        c.save();
        c.globalAlpha = k;
        c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText('不是谁更爱谁', 140, 210 + (1 - k) * 14);
        c.restore();
      }
    }
  };
})();
