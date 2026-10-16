// 第23页：静图慢推（全程线性，末段10%停稳）+ 文字依次浮现，只服务"面对关系里的真实代价"这一个点
SCENES['23'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/23_1.png';
  const LINES = ["别两边都要"];
  const AT = [0.30, 0.62, 0.85];
  return {
    draw(c, lt, t, IMG) {
      const D = 14, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));          // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色，第一帧不黑

      // ① 慢推：全程线性匀速，z 用给定的 1.09 → 1.17，焦点照抄 fx/fy
      const z = lerp(1.09, 1.17, pm);

      // ② 只有一张图，直接铺（fx/fy 是量出来的焦点，不改）
      MD.cover(c, IMG[P], { z, fx: 0.34, fy: 0.00 });

      // ③ 第 23 页靠后，不做明暗揭示，第一帧就是亮的

      // ④ 文字出现：0.30 / 0.62 / 0.85，每条 0.06 淡入 + 从下浮 14px
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 140, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, AT[i] || 0.85, 210 + i * 76));
    }
  };
})();
