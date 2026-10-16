// 07 案例一·周先生：静图匀速慢推(收尾停稳) + 开头明暗揭示 + 「追问细节」文字浮现，全程只动不画
SCENES['07'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/07_1.png';
  return {
    draw(c, lt, t, IMG) {
      const D = 14, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));            // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色，第 0 帧图已铺好

      // ① 慢推：全程线性、几乎匀速，基准 z 再往前推 7%；fx/fy 用给定焦点，不改
      const z = lerp(1.000, 1.070, pm);
      MD.cover(c, IMG[P], { z, fx: 1.00, fy: 0.50 });

      // ② 明暗揭示：开头 0→6% 灯慢慢打开（第 7 页靠前，可用），透明度线性降到 0
      const kd = clamp(lt / (D * 0.06));
      c.fillStyle = 'rgba(20,16,12,' + (0.65 * (1 - kd)).toFixed(3) + ')';
      c.fillRect(0, 0, W, H);

      // ③ 文字依次出现：0.30 浮现，淡入 + 从下 14px 浮上来，落在左侧留白区（主体在右）
      const k = ss(0.30, 0.36, p);
      if (k > 0) {
        c.save();
        c.globalAlpha = k;
        c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText('追问细节', 140, 210 + (1 - k) * 14);
        c.restore();
      }
    }
  };
})();
