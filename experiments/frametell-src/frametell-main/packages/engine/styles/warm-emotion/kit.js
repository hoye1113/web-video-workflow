/* Warm emotion · 情感组件套装（8 个）：门 / 手机 / 照片 / 背影 / 纸 / 光 / 距离 / 空位。
 *
 * 照 `lib/warm.js` 的写法：平涂 + 一层阴影 + 一处高光，不描粗边不发光（夜间除外）。
 * **凡是会变的属性都接受"数值或 lt 的函数"**，页面才保持对 t 纯粹；
 * 入场统一走 mount()（上浮 14px + 淡入，无弹跳），`o.at` / `o.dur` 控时，`o.out` 或 `.hide(t)` 出场。
 *
 * 纪律（GRAMMAR.md）：这些是**处境里的物**，不是图表。
 * 不许拿它们拼"标题 + 三卡 + 箭头"；`silhouette` 只能当**背景里的无名人物**，
 * 小芽 / 小树必须由定妆图生成。
 */
(function () {
  const { s, col, clamp, lerp, ease, Builder } = PV;
  const B = Builder.prototype;
  const val = (v, lt, d) => (typeof v === 'function' ? v(lt) : v ?? d);
  const rgb = (c) => { const h = col(c).replace('#', ''); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  /** 颜色 c 朝调色板的 ink 压暗 k（0..1） */
  const shade = (c, k = 0.2) => { const a = rgb(c), b = rgb('ink'); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(',')})`; };
  /** 颜色 c 朝调色板的 paper 提亮 k（0..1）—— 夜里做"受光面"用 */
  const tint = (c, k = 0.2) => { const a = rgb(c), b = rgb('paper'); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(',')})`; };
  const fmt = (n) => (+n).toFixed(2);
  const enter = (lt, at, dur = 0.7) => ease.out(clamp((lt - at) / dur));
  const isNight = () => (typeof window !== 'undefined' && window.STYLE && window.STYLE.theme === 'night');
  let uid = 0;
  const nid = (p) => p + (++uid);

  /** 画进自己的组、按 o.at 入场、按 o.out（或 .hide(t)）出场。draw(g) 返回 { update(lt), ...句柄 } */
  function mount(self, o, draw) {
    const g = s('g', { opacity: 0 }, self.svg);
    const at = o.at ?? 0, dur = o.dur ?? 0.7;
    let outAt = o.out, outDur = 0.5;
    const parts = draw(g);
    self.tick((lt) => {
      const k = enter(lt, at, dur);
      const out = outAt != null ? 1 - ease.out(clamp((lt - outAt) / outDur)) : 1;
      g.setAttribute('opacity', fmt(k * out));
      g.setAttribute('transform', `translate(0 ${fmt((1 - k) * 14)})`);
      parts?.update?.(lt);
    });
    return { g, ...(parts || {}), hide(t, d = 0.5) { outAt = t; outDur = Math.max(0.01, d); return this; } };
  }

  /* ───────────────────────── 门 ─────────────────────────
   * door(cx, baseY, w, h, o) —— 门框 + 门板（可开合）+ 门缝的光。
   * o: { open: 0..1 或 fn(lt), side: 'left'|'right'（铰链侧）, light, glow } */
  B.door = function (cx, baseY, w = 320, h = 520, o = {}) {
    return mount(this, o, (g) => {
      const x0 = cx - w / 2, y0 = baseY - h;
      const night = isNight();   // 构建时定死，别在 update 里读全局（会串页）
      // 门框里那点亮（门开着才看得见）：先铺在门板下面
      const gap = s('rect', { x: x0 + w * 0.06, y: y0 + h * 0.05, width: w * 0.88, height: h * 0.9, fill: col(o.light || 'orange') }, g);
      const hingeRight = o.side === 'right';
      const leaf = s('g', {}, g);
      s('rect', { x: 0, y: 0, width: w * 0.9, height: h * 0.94, rx: 6, fill: shade('faint', 0.06), stroke: col('soft'), 'stroke-width': 3 }, leaf);
      s('rect', { x: w * 0.08, y: h * 0.12, width: w * 0.74, height: h * 0.3, rx: 4, fill: shade('faint', 0.14), opacity: 0.7 }, leaf);
      s('circle', { cx: w * 0.78, cy: h * 0.5, r: 8, fill: col('soft') }, leaf);
      // 门框
      s('rect', { x: x0, y: y0, width: w, height: h, rx: 8, fill: 'none', stroke: col('soft'), 'stroke-width': 8 }, g);
      return {
        update(lt) {
          const open = clamp(val(o.open, lt, 0));
          // 绕铰链侧旋转：0 度关着，越开越像往屋里掀
          const deg = open * (hingeRight ? -62 : 62);
          const ox = hingeRight ? w * 0.9 : 0;
          leaf.setAttribute('transform', `translate(${fmt(hingeRight ? x0 + w * 0.05 : x0 + w * 0.05)} ${fmt(y0 + h * 0.03)}) translate(${fmt(ox)} 0) rotate(${fmt(deg)}) translate(${fmt(-ox)} 0)`);
          // 门缝透出的光：开得越大越亮（夜间更亮，因为屋里屋外反差大）
          gap.setAttribute('opacity', fmt(open * (night ? 0.92 : 0.7)));
        },
      };
    });
  };

  /* ───────────────────────── 手机 ─────────────────────────
   * phone(cx, cy, w, o) —— 一块会亮的屏。o: { lit: 0..1, notify: bool, tilt, glow } */
  B.phone = function (cx, cy, w = 180, o = {}) {
    return mount(this, o, (g) => {
      const h = w * 2.05, r = w * 0.14;
      const night = isNight();   // 构建时定死
      const halo = s('ellipse', { cx: 0, cy: 0, rx: w * 1.7, ry: w * 1.9, fill: col('orangeF'), opacity: 0 }, g);
      const body = s('g', {}, g);
      s('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: r, fill: col('ink'), opacity: 0.9 }, body);
      const screen = s('rect', { x: -w / 2 + w * 0.07, y: -h / 2 + w * 0.09, width: w * 0.86, height: h - w * 0.18, rx: r * 0.7, fill: col('orangeF') }, body);
      // 屏上那几行"看不懂但知道有内容"的字块（不写具体文字：屏上字只做标签，正文归口播）
      const lines = [0.34, 0.46, 0.4].map((k, i) => s('rect', { x: -w * 0.3, y: -h * 0.1 + i * w * 0.16, width: w * 0.6 * k, height: w * 0.055, rx: w * 0.03, fill: col('soft'), opacity: 0.5 }, body));
      const dot = s('circle', { cx: w * 0.26, cy: -h * 0.34, r: w * 0.075, fill: col('red') }, body);
      return {
        update(lt) {
          const lit = clamp(val(o.lit, lt, 0));
          body.setAttribute('transform', `translate(${fmt(val(cx, lt))} ${fmt(val(cy, lt))}) rotate(${fmt(val(o.tilt, lt, 0))})`);
          screen.setAttribute('opacity', fmt(0.12 + lit * 0.88));
          lines.forEach((l) => l.setAttribute('opacity', fmt(0.12 + lit * 0.5)));
          // 屏照亮了周围：白天是暖橘，夜里更亮更集中
          const haloK = lit * (night ? 0.5 : 0.26);
          halo.setAttribute('opacity', fmt(haloK));
          halo.setAttribute('transform', `translate(${fmt(val(cx, lt))} ${fmt(val(cy, lt))})`);
          dot.setAttribute('opacity', fmt(val(o.notify, lt, 0) ? (0.55 + 0.45 * Math.abs(Math.sin(lt * 2.4))) : 0));
          dot.setAttribute('transform', `translate(${fmt(-val(cx, lt))} ${fmt(-val(cy, lt))})`);
        },
      };
    });
  };

  /* ───────────────────────── 照片 ─────────────────────────
   * photo(cx, cy, w, o) —— 一张相纸。里面的"画面"只用色块暗示，绝不画脸。
   * o: { tilt, lift: 抬起高度, cut: 0..1 从中间断开 } */
  B.photo = function (cx, cy, w = 300, o = {}) {
    return mount(this, o, (g) => {
      const h = w * 0.78, hw = w / 2, inset = w * 0.07;
      // 两半各画自己那半边（和 paper 同一个教训：整块重画会让另一半盖住它）
      const L = s('g', {}, g), R = s('g', {}, g);
      // 左半：白边 + 画面 + 左边那个人
      s('rect', { x: -hw, y: -h / 2, width: hw, height: h, fill: '#fff', opacity: 0.96 }, L);
      s('rect', { x: -hw + inset, y: -h / 2 + h * 0.08, width: hw - inset, height: h * 0.66, fill: col('blueF') }, L);
      s('circle', { cx: -w * 0.14, cy: -h * 0.02, r: w * 0.09, fill: tint('purple', 0.35), opacity: 0.85 }, L);
      s('rect', { x: -w * 0.26, y: h * 0.2, width: w * 0.26, height: h * 0.1, fill: col('faint'), opacity: 0.6 }, L);
      // 右半：白边 + 画面 + 右边那个人
      s('rect', { x: 0, y: -h / 2, width: hw, height: h, fill: '#fff', opacity: 0.96 }, R);
      s('rect', { x: 0, y: -h / 2 + h * 0.08, width: hw - inset, height: h * 0.66, fill: col('blueF') }, R);
      s('circle', { cx: w * 0.14, cy: -h * 0.02, r: w * 0.09, fill: tint('blue', 0.4), opacity: 0.85 }, R);
      s('rect', { x: 0, y: h * 0.2, width: w * 0.26, height: h * 0.1, fill: col('faint'), opacity: 0.6 }, R);
      return {
        update(lt) {
          const cut = clamp(val(o.cut, lt, 0)), lift = val(o.lift, lt, 0), tilt = val(o.tilt, lt, 0);
          const X = val(cx, lt), Y = val(cy, lt) - lift;
          L.setAttribute('transform', `translate(${fmt(X - cut * w * 0.06)} ${fmt(Y)}) rotate(${fmt(tilt - cut * 4)}) translate(${fmt(-cut * 5)} 0)`);
          R.setAttribute('transform', `translate(${fmt(X + cut * w * 0.06)} ${fmt(Y)}) rotate(${fmt(tilt + cut * 4)}) translate(${fmt(cut * 5)} 0)`);
        },
      };
    });
  };

  /* ───────────────────────── 背影 ─────────────────────────
   * silhouette(cx, baseY, h, o) —— 背景里的**无名人物**剪影（头 + 肩 + 身，无五官）。
   * ⚠️ 只用来当背景群众 / 远处的人。小芽、小树必须由定妆图生成，不许用这个冒充。 */
  B.silhouette = function (cx, baseY, h = 420, o = {}) {
    return mount(this, o, (g) => {
      const c = col(o.color || 'soft');
      const night = isNight();   // 构建时定死
      const body = s('g', {}, g);
      s('circle', { cx: 0, cy: -h * 0.86, r: h * 0.11, fill: c }, body);
      s('path', { d: `M${-h * 0.19} 0 L${-h * 0.16} ${-h * 0.62} Q 0 ${-h * 0.78} ${h * 0.16} ${-h * 0.62} L${h * 0.19} 0 Z`, fill: c }, body);
      return {
        update(lt) {
          body.setAttribute('transform', `translate(${fmt(val(cx, lt))} ${fmt(val(baseY, lt))}) scale(${fmt(val(o.scale, lt, 1))} ${fmt(val(o.scale, lt, 1))})`);
          // 夜里让它几乎融进背景：远处的、看不清的人
          body.setAttribute('opacity', fmt(val(o.alpha, lt, night ? 0.55 : 0.78)));
        },
      };
    });
  };

  /* ───────────────────────── 纸 ─────────────────────────
   * paper(cx, cy, w, h, o) —— 一张纸，能折、能皱、能撕。
   * o: { crease: 0..1 折, crumple: 0..1 皱, tear: 0..1 撕, tilt } */
  B.paper = function (cx, cy, w = 420, h = 540, o = {}) {
    return mount(this, o, (g) => {
      // 左右两半**各画自己那一半** —— 否则右半会把左半的折痕整块盖住（冒烟测试抓到的 bug）
      const L = s('g', {}, g), R = s('g', {}, g);
      s('path', { d: `M${-w / 2} ${-h / 2} L0 ${-h / 2} L0 ${h / 2} L${-w / 2} ${h / 2} Z`, fill: col('paper'), stroke: col('faint'), 'stroke-width': 2.5 }, L);
      s('path', { d: `M0 ${-h / 2} L${w / 2} ${-h / 2} L${w / 2} ${h / 2} L0 ${h / 2} Z`, fill: col('paper'), stroke: col('faint'), 'stroke-width': 2.5 }, R);
      // 折痕：一条对角折线 + 折起的角（从左上角往右下）
      const crease = s('path', { d: '', fill: 'none', stroke: shade('faint', 0.22), 'stroke-width': 3 }, L);
      const corner = s('path', { d: '', fill: shade('faint', 0.1), opacity: 0.9 }, L);
      // 皱：一组长短不一的折线，越皱越多越密
      const wrinkles = [0, 1, 2, 3, 4, 5, 6].map(() => s('path', { d: '', fill: 'none', stroke: shade('faint', 0.3), 'stroke-width': 2, opacity: 0 }, L));
      const tearEdge = s('path', { d: '', fill: col('redF'), opacity: 0.85 }, R);
      return {
        update(lt) {
          const cr = clamp(val(o.crease, lt, 0)), cp = clamp(val(o.crumple, lt, 0)), tr = clamp(val(o.tear, lt, 0));
          const X = val(cx, lt), Y = val(cy, lt), tilt = val(o.tilt, lt, 0);
          L.setAttribute('transform', `translate(${fmt(X - tr * w * 0.1)} ${fmt(Y)}) rotate(${fmt(tilt - tr * 3)})`);
          R.setAttribute('transform', `translate(${fmt(X + tr * w * 0.1)} ${fmt(Y)}) rotate(${fmt(tilt + tr * 3)})`);
          // 折：折角随 crease 展开
          const cw = w * 0.42 * cr;
          crease.setAttribute('d', cr > 0.01 ? `M${fmt(-w / 2)} ${fmt(-h / 2 + cw)} L${fmt(-w / 2 + cw)} ${fmt(-h / 2 + cw)} L${fmt(-w / 2 + cw)} ${fmt(-h / 2)}` : '');
          corner.setAttribute('d', cr > 0.01 ? `M${fmt(-w / 2)} ${fmt(-h / 2 + cw)} L${fmt(-w / 2 + cw)} ${fmt(-h / 2 + cw)} L${fmt(-w / 2 + cw)} ${fmt(-h / 2)} Z` : '');
          // 皱：折线随 crumple 逐个亮起（不是一次性全出现）
          wrinkles.forEach((el, i) => {
            const k = clamp(cp * 7 - i);
            const y = -h / 2 + h * (0.18 + i * 0.11);
            const amp = 0.7 + 0.3 * Math.sin(i * 1.7 + lt * 0.6);
            el.setAttribute('d', k > 0.01 ? `M${fmt(-w / 2 + 26)} ${fmt(y)} q ${fmt(w * 0.14 * amp)} ${fmt(-h * 0.022)} ${fmt(w * 0.17)} 0 t ${fmt(w * 0.17)} 0` : '');
            el.setAttribute('opacity', fmt(k * 0.75));
          });
          // 撕：右半露一条毛边
          tearEdge.setAttribute('d', tr > 0.01 ? `M${fmt(-w / 2)} ${fmt(-h / 2)} L${fmt(-w / 2 + w * 0.02)} ${fmt(-h * 0.2)} L${fmt(-w / 2)} ${fmt(h * 0.12)} L${fmt(-w / 2 + w * 0.02)} ${fmt(h / 2)} L${fmt(-w / 2)} ${fmt(h / 2)} Z` : '');
        },
      };
    });
  };

  /* ───────────────────────── 光 ─────────────────────────
   * light(cx, cy, r, o) —— 一束光。情感片里**光就是情绪**，这是最该先用好的一个。
   * o: { k: 0..1 强度, kind: 'window'|'lamp'|'screen'|'wash', full: 铺满全屏（做明暗揭示） } */
  B.light = function (cx, cy, r = 600, o = {}) {
    return mount(this, { ...o, dur: o.dur ?? 1.1 }, (g) => {
      // o.ground：铺一层全幅底色（夜间页自己造"深底"，因为片的背景只在初始化时算一次）
      const ground = o.ground ? s('rect', { x: -3000, y: -3000, width: 6000, height: 6000, fill: col(o.ground), opacity: 1 }, g) : null;
      const id = nid('wm-light');
      const defs = s('defs', {}, g);
      const grad = s('radialGradient', { id }, defs);
      const warm = col(o.color || 'orange');
      s('stop', { offset: '0%', 'stop-color': warm, 'stop-opacity': isNight() ? 0.5 : 0.34 }, grad);
      s('stop', { offset: '55%', 'stop-color': warm, 'stop-opacity': isNight() ? 0.2 : 0.12 }, grad);
      s('stop', { offset: '100%', 'stop-color': warm, 'stop-opacity': 0 }, grad);
      const disc = s(o.full ? 'rect' : 'circle', o.full
        ? { x: -2000, y: -2000, width: 4000, height: 4000, fill: `url(#${id})` }
        : { cx: 0, cy: 0, r, fill: `url(#${id})` }, g);
      // lamp / screen 再叠一个更硬的芯，window / wash 保持柔
      const hard = (o.kind === 'lamp' || o.kind === 'screen')
        ? s('circle', { cx: 0, cy: 0, r: r * 0.26, fill: col('yellow'), opacity: 0 }, g) : null;
      return {
        update(lt) {
          const k = clamp(val(o.k, lt, 1));
          disc.setAttribute('transform', o.full ? '' : `translate(${fmt(val(cx, lt))} ${fmt(val(cy, lt))})`);
          disc.setAttribute('opacity', fmt(k));
          if (hard) {
            hard.setAttribute('transform', `translate(${fmt(val(cx, lt))} ${fmt(val(cy, lt))})`);
            hard.setAttribute('opacity', fmt(k * 0.4));
          }
        },
      };
    });
  };

  /* ───────────────────────── 距离 ─────────────────────────
   * span(x0, x1, y, o) —— 一段**实体长物**（长桌沿 / 矮墙顶 / 长凳），用它把两个人隔开。
   * 距离不用尺子量，用"同一张桌子，两端很远"来说。o: { reach: 0..1 伸展, thick, color } */
  B.span = function (x0, x1, y, o = {}) {
    return mount(this, o, (g) => {
      const th = o.thick ?? 26;
      const top = s('rect', { x: 0, y: 0, width: 1, height: th, rx: th * 0.3, fill: col(o.color || 'softF') }, g);
      const edge = s('rect', { x: 0, y: th * 0.72, width: 1, height: th * 0.28, rx: th * 0.14, fill: shade(o.color || 'softF', 0.16) }, g);
      const leg = s('rect', { x: 0, y: th, width: 10, height: 90, rx: 4, fill: shade(o.color || 'softF', 0.22), opacity: 0.8 }, g);
      return {
        update(lt) {
          const X0 = val(x0, lt), X1 = val(x1, lt), Y = val(y, lt);
          const reach = clamp(val(o.reach, lt, 1));
          const x = X0, w = Math.max(1, (X1 - X0) * reach);
          top.setAttribute('x', fmt(x)); top.setAttribute('width', fmt(w)); top.setAttribute('y', fmt(Y));
          edge.setAttribute('x', fmt(x)); edge.setAttribute('width', fmt(w)); edge.setAttribute('y', fmt(Y + th * 0.72));
          leg.setAttribute('x', fmt(X1 - 40)); leg.setAttribute('y', fmt(Y + th));
          leg.setAttribute('opacity', fmt(reach > 0.85 ? 0.8 : 0));
        },
      };
    });
  };

  /* ───────────────────────── 空位 ─────────────────────────
   * emptyseat(cx, baseY, w, o) —— 一个空出来的位置：椅子还在，人不在。
   * o: { fade: 0..1 空位显出来的程度, color } —— 常用手法：人先 hide()，再把空位淡入。 */
  B.emptyseat = function (cx, baseY, w = 260, o = {}) {
    return mount(this, o, (g) => {
      const h = w * 1.15, c = col(o.color || 'muted');
      const seat = s('g', {}, g);
      s('rect', { x: -w * 0.42, y: -h * 0.44, width: w * 0.84, height: h * 0.1, rx: 8, fill: c, opacity: 0.75 }, seat);
      s('rect', { x: -w * 0.42, y: -h, width: w * 0.14, height: h * 0.58, rx: 10, fill: c, opacity: 0.75 }, seat);
      s('rect', { x: -w * 0.42, y: -h * 0.36, width: w * 0.09, height: h * 0.36, rx: 6, fill: c, opacity: 0.6 }, seat);
      s('rect', { x: w * 0.33, y: -h * 0.36, width: w * 0.09, height: h * 0.36, rx: 6, fill: c, opacity: 0.6 }, seat);
      // 座面上那一点"凹陷"：曾经有人坐过的痕迹
      const dent = s('ellipse', { cx: 0, cy: -h * 0.38, rx: w * 0.3, ry: h * 0.035, fill: shade(o.color || 'muted', 0.2), opacity: 0 }, seat);
      return {
        update(lt) {
          seat.setAttribute('transform', `translate(${fmt(val(cx, lt))} ${fmt(val(baseY, lt))})`);
          const k = clamp(val(o.fade, lt, 1));
          dent.setAttribute('opacity', fmt(k * 0.5));
          seat.setAttribute('opacity', fmt(0.35 + k * 0.5));
        },
      };
    });
  };
})();
