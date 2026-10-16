/* p26 重建边界
 * 底是我们自己的生成图（两只手按在纸上）—— 这一页用「真画」当质感层。
 * 先压一层「互相消耗」的暖暗（不是灰的，别把纸的暖调压死）；暗褪掉之后，
 * 在纸上直接画下两条竖线和一条底线：不是把过去粘回去，是重新立规矩。
 * 标签一律挂在竖线的中段（y≈300），相机推近时不会被顶出画外。
 */
ENGINE.visual('p26', (P) => {
  P.title('重建边界', { accent: 'blue' });

  // ① 底：生成图铺满（不要描边和投影，它是一层底板）
  const base = P.layer();
  base.img('assets/26_1.png', 0, 0, 1920, 1080, { fit: 'cover', border: false, shadow: false, at: 0 });

  // ② 上面这层画线和字
  const over = P.layer();

  // ③「互相消耗」：一层暖褐压上去（0.22 就够，重了就把纸压成灰的），c1 之后褪掉
  const dim = PV.s('rect', { x: 0, y: 0, width: 1920, height: 1080, fill: PV.col('soft'), opacity: 0 }, over.svg);
  over.tick((lt) => {
    const up = PV.ease.out(PV.clamp((lt - 0.2) / 1.5));
    const down = PV.ease.out(PV.clamp((lt - P.c(1, 0.3)) / 1.3));
    dim.setAttribute('opacity', (0.22 * up * (1 - down)).toFixed(3));
  });

  // ④「重新建立规则和边界」：两条竖线从上落下来，标签挂在线的中段
  const Y0 = 170, Y1 = 900;
  over.line(900, Y0, 900, Y1, { color: 'ink', sw: 5, at: P.c(2, 0.1), dur: 0.85 });
  over.line(1330, Y0, 1330, Y1, { color: 'ink', sw: 5, at: P.c(2, 0.75), dur: 0.85 });
  over.tag(900, 420, '规则', { size: 42, color: 'ink', at: P.c(2, 0.95) });
  over.tag(1330, 420, '边界', { size: 42, color: 'ink', at: P.c(2, 1.45) });

  // ⑤「可承受可持续」：一条底线把中间框起来（不是回到过去，是从这里重新开始）
  over.line(800, Y1 + 60, 1430, Y1 + 60, { color: 'green', sw: 5, at: P.c(3, 0.25), dur: 0.75 });
  over.tag(1115, Y1 + 116, '可承受 · 可持续', { size: 40, color: 'green', at: P.c(3, 1.0) });

  // ⑥ 镜头：说到「重新建立规则和边界」时，推近两条线之间（中心放在标签那一带）
  P.cam([P.push(P.c(2, 0.25), 1115, 470, 1.22), P.back(P.endT + 0.45)]);
});
