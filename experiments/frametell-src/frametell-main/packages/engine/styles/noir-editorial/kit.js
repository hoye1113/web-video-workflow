/* Noir editorial kit · hairlines, chapter HUD, serif reveals, counters, connectors,
 * line-art diagrams and a waveform. Everything is a pure function of page time. */
(function () {
  const { s, h, col, clamp, lerp, ease, Builder } = PV;
  const B = Builder.prototype;
  const fmt = (n) => (+n).toFixed(2);
  const pad2 = (n) => String(n).padStart(2, '0');
  const val = (v, lt, d) => (typeof v === 'function' ? v(lt) : (v ?? d));

  /* ── raw SVG helpers ─────────────────────────────────────── */

  function line(B, parent, x1, y1, x2, y2, o = {}) {
    const el = s('line', {
      x1, y1, x2, y2,
      stroke: col(o.color || 'faint'),
      'stroke-width': o.sw ?? 1.2,
      'stroke-linecap': 'round',
    }, parent);
    const at = o.at ?? 0, dur = o.dur ?? 0.7;
    const len = Math.hypot(x2 - x1, y2 - y1) || 1;
    if (o.dashed) {
      el.setAttribute('stroke-dasharray', o.dash || '4 8');
      el.style.opacity = '0';
      B.tick((lt) => { el.style.opacity = ((o.opacity ?? 1) * ease.out(clamp((lt - at) / dur))).toFixed(3); });
    } else {
      el.style.strokeDasharray = `${len} ${len}`;
      el.style.strokeDashoffset = len;
      B.tick((lt) => {
        const k = ease.out(clamp((lt - at) / dur));
        el.style.strokeDashoffset = (len * (1 - k)).toFixed(2);
        el.style.opacity = ((o.opacity ?? 1) * k).toFixed(3);
      });
    }
    return el;
  }

  function path(B, parent, d, o = {}) {
    const el = s('path', {
      d,
      fill: o.fill ? col(o.fill) : 'none',
      stroke: o.stroke === false ? 'none' : col(o.color || 'faint'),
      'stroke-width': o.sw ?? 1.4,
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
    }, parent);
    const at = o.at ?? 0, dur = o.dur ?? 0.8;
    const len = el.getTotalLength() || 1;
    el.style.strokeDasharray = `${len} ${len}`;
    el.style.strokeDashoffset = len;
    B.tick((lt) => {
      const k = ease.out(clamp((lt - at) / dur));
      el.style.strokeDashoffset = (len * (1 - k)).toFixed(2);
      el.style.opacity = ((o.opacity ?? 1) * k).toFixed(3);
    });
    return el;
  }

  function circle(B, parent, cx, cy, r, o = {}) {
    const el = s('circle', {
      cx, cy, r,
      fill: o.fill ? col(o.fill) : 'none',
      stroke: o.stroke === false ? 'none' : col(o.color || 'faint'),
      'stroke-width': o.sw ?? 1.2,
    }, parent);
    const at = o.at ?? 0, dur = o.dur ?? 0.5;
    el.style.opacity = '0';
    B.tick((lt) => {
      const k = ease.out(clamp((lt - at) / dur));
      el.style.opacity = ((o.opacity ?? 1) * k).toFixed(3);
      el.style.transform = `translate(${cx}px ${cy}px) scale(${(0.86 + 0.14 * k).toFixed(3)}) translate(${-cx}px ${-cy}px)`;
    });
    return el;
  }

  /* ── chapter header (always on the HUD, never moved by the camera) ─ */

  B.noirHeader = function (index, total, en, o = {}) {
    const at = o.at ?? 0.1;
    const gold = o.color || 'orange';
    line(this, this.svg, 140, 58, 1780, 58, { color: 'faint', sw: 1, at, dur: 1.1, opacity: 0.9 });
    line(this, this.svg, 140, 58, 300, 58, { color: gold, sw: 1.5, at: at + 0.1, dur: 0.7 });
    circle(this, this.svg, 140, 84, 3.2, { color: gold, fill: gold, stroke: false, at: at + 0.05, dur: 0.35 });

    const a = this.text(`${pad2(index)} / ${pad2(total)}`, {
      x: 156, y: 70, size: 16, font: 'mono', color: gold, at, mode: 'fade', dur: 0.5,
    });
    a.el.style.letterSpacing = '0.14em';

    const b = this.text(en, {
      x: 300, y: 71, size: 13, font: 'mono', color: 'muted', at: at + 0.12, mode: 'fade', dur: 0.6,
    });
    b.el.style.letterSpacing = '0.24em';
    b.el.style.textTransform = 'uppercase';

    line(this, this.svg, 540, 78, 760, 78, { color: 'faint', sw: 1, at: at + 0.25, dur: 0.6, opacity: 0.9 });

    const r = this.text(o.right || `NOIR / ${pad2(index)}`, {
      x: 1640, y: 71, size: 13, font: 'mono', color: 'muted', at: at + 0.2, mode: 'fade', dur: 0.6,
    });
    r.el.style.letterSpacing = '0.22em';

    // small registration marks at the right edge
    circle(this, this.svg, 1774, 84, 2.4, { color: 'faint', fill: 'faint', stroke: false, at: at + 0.3, dur: 0.3 });
    line(this, this.svg, 1760, 96, 1780, 96, { color: 'faint', sw: 1, at: at + 0.35, dur: 0.3, opacity: 0.7 });
  };

  /* ── serif title with a per-character mask reveal ───────── */

  B.noirReveal = function (str, o = {}) {
    const el = h('div', 'tx ' + (o.font || 'serif'), null, this.html);
    const size = o.size ?? 92;
    Object.assign(el.style, {
      left: (o.x ?? 140) + 'px',
      top: (o.y ?? 220) + 'px',
      fontSize: size + 'px',
      lineHeight: String(o.lh ?? 1.18),
      color: col(o.color || 'ink'),
      fontWeight: String(o.weight ?? 400),
      letterSpacing: o.track ?? '0.04em',
      whiteSpace: o.wrap ? 'normal' : 'nowrap',
    });
    if (o.w) { el.style.width = o.w + 'px'; el.style.whiteSpace = 'normal'; }
    if (o.align === 'c') {
      const w = o.w ?? 1200;
      el.style.width = w + 'px';
      el.style.left = (o.x - w / 2) + 'px';
      el.style.textAlign = 'center';
    }

    const rows = [];
    const spans = [];
    const lines = String(str).split('\n');
    for (const lineText of lines) {
      const row = h('div', 'line', null, el);
      row.style.whiteSpace = 'pre';
      rows.push(row);
      for (const ch of Array.from(lineText)) {
        const sp = h('span', 'ch', ch === ' ' ? '&nbsp;' : ch, row);
        sp.style.display = 'inline-block';
        sp.style.opacity = '0';
        sp.style.willChange = 'opacity, transform, filter';
        spans.push(sp);
      }
    }

    const at = o.at ?? 0, dur = o.dur ?? 0.62, stagger = o.stagger ?? 0.032;
    const dy = o.dy ?? 0.26;
    this.tick((lt) => {
      for (let i = 0; i < spans.length; i++) {
        const k = ease.out(clamp((lt - at - i * stagger) / dur));
        const sp = spans[i];
        sp.style.opacity = k.toFixed(3);
        sp.style.transform = k >= 1 ? '' : `translateY(${((1 - k) * dy).toFixed(3)}em)`;
        sp.style.filter = k >= 0.98 ? 'none' : `blur(${((1 - k) * 5).toFixed(2)}px)`;
      }
    });
    return { el, spans };
  };

  /* ── small type ─────────────────────────────────────────── */

  B.noirLabel = function (str, x, y, o = {}) {
    const t = this.text(str, {
      x, y, size: o.size ?? 14, font: o.font || 'mono',
      color: o.color || 'muted', at: o.at ?? 0, mode: 'fade', dur: o.dur ?? 0.5,
    });
    t.el.style.letterSpacing = o.track ?? '0.2em';
    if (o.upper !== false) t.el.style.textTransform = 'uppercase';
    return t;
  };

  B.noirNarration = function (str, o = {}) {
    const at = o.at ?? 0;
    line(this, this.svg, 820, 872, 1100, 872, { color: 'faint', sw: 1, at: at - 0.15, dur: 0.5, opacity: 0.8 });
    this.noirLabel(o.kicker || 'NARRATION', 820, 884, { size: 12, color: 'muted', at: at - 0.05, track: '0.24em' });
    const t = this.text(str, {
      x: 960, y: 912, w: 1500, align: 'c', size: o.size ?? 34,
      color: o.color || 'ink', at, mode: 'fade', dur: 0.5, lh: 1.35,
    });
    t.el.classList.add('narration');
    return t;
  };

  /* ── counter ────────────────────────────────────────────── */

  B.noirCounter = function (x, y, value, o = {}) {
    const el = h('div', 'tx ' + (o.font || 'mono'), null, this.html);
    Object.assign(el.style, {
      left: x + 'px', top: y + 'px',
      fontSize: (o.size ?? 120) + 'px',
      lineHeight: '1',
      color: col(o.color || 'blue'),
      fontWeight: String(o.weight ?? 400),
      letterSpacing: o.track ?? '0.01em',
      whiteSpace: 'nowrap',
      opacity: '0',
    });
    if (o.align === 'c') { el.style.width = (o.w ?? 500) + 'px'; el.style.left = (x - (o.w ?? 500) / 2) + 'px'; el.style.textAlign = 'center'; }
    const at = o.at ?? 0, dur = o.dur ?? 0.8;
    const dec = o.decimals ?? 0;
    this.tick((lt) => {
      const k = ease.out(clamp((lt - at) / dur));
      el.style.opacity = k.toFixed(3);
      const v = value * k;
      el.textContent = (o.prefix || '') + (dec ? v.toFixed(dec) : Math.round(v).toLocaleString('en-US')) + (o.suffix || '');
    });
    return el;
  };

  /* ── line-art diagrams ─────────────────────────────────── */

  B.noirConnector = function (x1, y1, x2, y2, o = {}) {
    const g = s('g', {}, this.svg);
    line(this, g, x1, y1, x2, y2, o);
    if (o.dot !== false) circle(this, g, x2, y2, o.r ?? 2.6, { color: o.color || 'blue', fill: o.color || 'blue', stroke: false, at: (o.at ?? 0) + (o.dur ?? 0.7) * 0.75, dur: 0.3 });
    return g;
  };

  B.noirNode = function (x, y, r = 10, o = {}) {
    const g = s('g', {}, this.svg);
    circle(this, g, x, y, r, { color: o.color || 'blue', sw: o.sw ?? 1.2, at: o.at ?? 0, dur: o.dur ?? 0.5 });
    circle(this, g, x, y, Math.max(2, r * 0.22), { color: o.color || 'blue', fill: o.color || 'blue', stroke: false, at: (o.at ?? 0) + 0.15, dur: 0.3 });
    return g;
  };

  B.noirCurve = function (d, o = {}) {
    const g = s('g', {}, this.svg);
    const el = path(this, g, d, o);
    if (o.glow) el.style.filter = `drop-shadow(0 0 ${o.glow}px ${col(o.color || 'blue')})`;
    return g;
  };

  B.noirEye = function (x, y, size = 100, o = {}) {
    const g = s('g', { transform: `translate(${x} ${y}) scale(${size / 100})` }, this.svg);
    const c = o.color || 'blue';
    path(this, g, 'M-48 0 C-26 -32 26 -32 48 0 C26 32 -26 32 -48 0 Z', { color: c, sw: 1.6, at: o.at ?? 0, dur: 0.8 });
    circle(this, g, 0, 0, 21, { color: c, sw: 1.2, at: (o.at ?? 0) + 0.25, dur: 0.5 });
    circle(this, g, 0, 0, 7, { color: c, fill: c, stroke: false, at: (o.at ?? 0) + 0.4, dur: 0.35 });
    circle(this, g, 0, 0, 38, { color: c, sw: 0.8, at: (o.at ?? 0) + 0.15, dur: 0.5, opacity: 0.28 });
    return g;
  };

  B.noirWave = function (x, y, w, h, o = {}) {
    const g = s('g', {}, this.svg);
    const n = o.bars ?? 44;
    const gap = o.gap ?? 5;
    const bw = Math.max(1.5, (w - gap * (n - 1)) / n);
    const bars = [];
    for (let i = 0; i < n; i++) {
      const r = s('rect', { x: x + i * (bw + gap), y: y + h / 2, width: bw, height: 2, rx: bw / 2, fill: col(o.color || 'blue') }, g);
      bars.push(r);
    }
    const base = s('line', { x1: x, y1: y + h / 2, x2: x + w, y2: y + h / 2, stroke: col('faint'), 'stroke-width': 0.8, opacity: 0.5 }, g);
    const at = o.at ?? 0, dur = o.dur ?? 0.6;
    this.tick((lt) => {
      const k = ease.out(clamp((lt - at) / dur));
      g.style.opacity = k.toFixed(3);
      for (let i = 0; i < bars.length; i++) {
        const v = 0.18 + 0.82 * Math.abs(Math.sin(i * 0.71 + lt * 2.1) * Math.cos(i * 0.19 - lt * 0.63));
        const bh = 3 + v * h * 0.86;
        bars[i].setAttribute('height', bh.toFixed(1));
        bars[i].setAttribute('y', (y + (h - bh) / 2).toFixed(1));
        bars[i].setAttribute('opacity', (0.25 + v * 0.75).toFixed(2));
      }
    });
    return g;
  };

  B.noirBook = function (x, y, w, o = {}) {
    const g = s('g', {}, this.svg);
    const hh = o.h ?? w * 0.52;
    const c = o.color || 'orange';
    const spine = x + w / 2;
    path(this, g, `M${x} ${y + 16} Q${x + w * 0.24} ${y - 4} ${spine} ${y + 18} L${spine} ${y + hh - 8} Q${x + w * 0.24} ${y + hh - 30} ${x} ${y + hh - 12} Z`, { color: c, sw: 1.5, at: o.at ?? 0, dur: 0.8 });
    path(this, g, `M${x + w} ${y + 16} Q${x + w * 0.76} ${y - 4} ${spine} ${y + 18} L${spine} ${y + hh - 8} Q${x + w * 0.76} ${y + hh - 30} ${x + w} ${y + hh - 12} Z`, { color: c, sw: 1.5, at: (o.at ?? 0) + 0.1, dur: 0.8 });
    for (let i = 0; i < 4; i++) {
      const yy = y + 42 + i * (hh - 70) / 4;
      line(this, g, x + 22, yy, spine - 14, yy + 2, { color: 'muted', sw: 0.8, at: (o.at ?? 0) + 0.35 + i * 0.06, dur: 0.45, opacity: 0.6 });
      line(this, g, spine + 14, yy + 2, x + w - 22, yy, { color: 'muted', sw: 0.8, at: (o.at ?? 0) + 0.4 + i * 0.06, dur: 0.45, opacity: 0.6 });
    }
    return g;
  };

  B.noirCrack = function (x, y, w, hh, o = {}) {
    const g = s('g', {}, this.svg);
    const c = o.color || 'red';
    const mid = x + w / 2;
    const d = `M${mid} ${y} L${mid - w * 0.12} ${y + hh * 0.22} L${mid + w * 0.08} ${y + hh * 0.4} L${mid - w * 0.14} ${y + hh * 0.58} L${mid + w * 0.06} ${y + hh * 0.76} L${mid} ${y + hh}`;
    const el = path(this, g, d, { color: c, sw: o.sw ?? 1.8, at: o.at ?? 0, dur: o.dur ?? 0.9 });
    el.style.filter = `drop-shadow(0 0 7px ${col(c)})`;
    path(this, g, `M${mid - w * 0.06} ${y + hh * 0.3} L${mid - w * 0.2} ${y + hh * 0.36}`, { color: c, sw: 0.9, at: (o.at ?? 0) + 0.35, dur: 0.4, opacity: 0.65 });
    path(this, g, `M${mid + w * 0.02} ${y + hh * 0.62} L${mid + w * 0.18} ${y + hh * 0.7}`, { color: c, sw: 0.9, at: (o.at ?? 0) + 0.45, dur: 0.4, opacity: 0.65 });
    return g;
  };

  B.noirTwoNodes = function (x1, y1, x2, y2, o = {}) {
    const g = s('g', {}, this.svg);
    const c = o.color || 'blue';
    line(this, g, x1, y1, x2, y2, { color: o.lineColor || 'faint', sw: o.sw ?? 1.1, at: o.at ?? 0, dur: 0.8, opacity: 0.8 });
    circle(this, g, x1, y1, o.r ?? 8, { color: c, sw: 1.2, at: o.at ?? 0, dur: 0.5 });
    circle(this, g, x2, y2, o.r ?? 8, { color: c, sw: 1.2, at: (o.at ?? 0) + 0.12, dur: 0.5 });
    circle(this, g, x1, y1, Math.max(2, (o.r ?? 8) * 0.25), { color: c, fill: c, stroke: false, at: (o.at ?? 0) + 0.2, dur: 0.3 });
    circle(this, g, x2, y2, Math.max(2, (o.r ?? 8) * 0.25), { color: c, fill: c, stroke: false, at: (o.at ?? 0) + 0.32, dur: 0.3 });
    return g;
  };

  B.noirScale = function (x, y, w, o = {}) {
    const g = s('g', {}, this.svg);
    const c = o.color || 'orange';
    const beamY = y + 36;
    line(this, g, x, y + 170, x, beamY, { color: 'soft', sw: 1.2, at: o.at ?? 0, dur: 0.6 });
    line(this, g, x - w / 2, beamY, x + w / 2, beamY, { color: 'soft', sw: 1.2, at: (o.at ?? 0) + 0.1, dur: 0.7 });
    line(this, g, x - w / 2, beamY, x - w / 2 + 18, beamY + 50, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.35, dur: 0.4, opacity: 0.7 });
    line(this, g, x - w / 2 + 18, beamY + 50, x - w / 2 - 18, beamY + 50, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.45, dur: 0.4, opacity: 0.7 });
    path(this, g, `M${x - w / 2 - 18} ${beamY + 50} Q${x - w / 2} ${beamY + 84} ${x - w / 2 + 18} ${beamY + 50}`, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.5, dur: 0.4 });
    line(this, g, x + w / 2, beamY, x + w / 2 - 18, beamY + 50, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.4, dur: 0.4, opacity: 0.7 });
    line(this, g, x + w / 2 - 18, beamY + 50, x + w / 2 + 18, beamY + 50, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.5, dur: 0.4, opacity: 0.7 });
    path(this, g, `M${x + w / 2 - 18} ${beamY + 50} Q${x + w / 2} ${beamY + 84} ${x + w / 2 + 18} ${beamY + 50}`, { color: 'soft', sw: 0.9, at: (o.at ?? 0) + 0.55, dur: 0.4 });
    circle(this, g, x, beamY, 5, { color: c, fill: c, stroke: false, at: (o.at ?? 0) + 0.2, dur: 0.3 });
    return g;
  };

  B.noirHouse = function (x, y, w, o = {}) {
    const g = s('g', {}, this.svg);
    const c = o.color || 'orange';
    const hh = o.h ?? w * 0.62;
    path(this, g, `M${x} ${y + 58} L${x + w / 2} ${y} L${x + w} ${y + 58}`, { color: c, sw: 1.6, at: o.at ?? 0, dur: 0.8 });
    path(this, g, `M${x + 22} ${y + 58} L${x + 22} ${y + hh} L${x + w - 22} ${y + hh} L${x + w - 22} ${y + 58}`, { color: c, sw: 1.4, at: (o.at ?? 0) + 0.15, dur: 0.8 });
    path(this, g, `M${x + w * 0.42} ${y + hh} L${x + w * 0.42} ${y + hh - 46} L${x + w * 0.58} ${y + hh - 46} L${x + w * 0.58} ${y + hh}`, { color: c, sw: 1.1, at: (o.at ?? 0) + 0.55, dur: 0.5 });
    line(this, g, x - 18, y + hh + 18, x + w + 18, y + hh + 18, { color: 'faint', sw: 1.2, at: (o.at ?? 0) + 0.7, dur: 0.7, opacity: 0.85 });
    path(this, g, `M${x + w * 0.22} ${y + hh + 18} L${x + w * 0.28} ${y + hh + 42} L${x + w * 0.24} ${y + hh + 58}`, { color: 'red', sw: 1.1, at: (o.at ?? 0) + 0.9, dur: 0.4, opacity: 0.75 });
    return g;
  };

  B.noirSprout = function (x, y, hh, o = {}) {
    const g = s('g', {}, this.svg);
    const c = o.color || 'green';
    path(this, g, `M${x} ${y + hh} C${x - 8} ${y + hh * 0.62} ${x + 2} ${y + hh * 0.38} ${x} ${y + hh * 0.14}`, { color: c, sw: 1.7, at: o.at ?? 0, dur: 0.8 });
    path(this, g, `M${x} ${y + hh * 0.56} C${x - 56} ${y + hh * 0.48} ${x - 68} ${y + hh * 0.28} ${x - 60} ${y + hh * 0.22} C${x - 32} ${y + hh * 0.24} ${x - 12} ${y + hh * 0.38} ${x} ${y + hh * 0.56} Z`, { color: c, sw: 1.2, fill: 'greenF', at: (o.at ?? 0) + 0.25, dur: 0.7 });
    path(this, g, `M${x} ${y + hh * 0.36} C${x + 44} ${y + hh * 0.3} ${x + 62} ${y + hh * 0.14} ${x + 58} ${y + hh * 0.08} C${x + 32} ${y + hh * 0.1} ${x + 12} ${y + hh * 0.22} ${x} ${y + hh * 0.36} Z`, { color: c, sw: 1.2, fill: 'greenF', at: (o.at ?? 0) + 0.4, dur: 0.7 });
    circle(this, g, x, y + hh * 0.14, 3.5, { color: c, fill: c, stroke: false, at: (o.at ?? 0) + 0.55, dur: 0.3 });
    return g;
  };

  B.noirGhost = function (str, o = {}) {
    const el = h('div', 'tx serif ghost', null, this.html);
    Object.assign(el.style, {
      left: (o.x ?? 1200) + 'px',
      top: (o.y ?? 260) + 'px',
      fontSize: (o.size ?? 260) + 'px',
      lineHeight: '1',
      opacity: String(o.opacity ?? 0.2),
      letterSpacing: o.track ?? '0.02em',
      whiteSpace: 'nowrap',
    });
    el.textContent = str;
    return el;
  };

  /* ── card / hairline utilities used by pages ───────────── */

  B.noirCard = function (x, y, w, hh, o = {}) {
    const box = this.box(x, y, w, hh, {
      r: o.r ?? 2, fill: o.fill || 'paper', color: o.color || 'faint',
      sw: o.sw ?? 1.1, rough: 0, single: true, texture: false,
      at: o.at ?? 0, dur: o.dur ?? 0.6, pen: false,
    });
    if (o.title) {
      this.text(o.title, {
        x: x + w / 2, y: y + (o.ty ?? 22), w, align: 'c',
        size: o.size ?? 28, font: o.font || 'serif', color: o.tcolor || 'ink',
        at: (o.at ?? 0) + 0.25, mode: 'fade', dur: 0.4,
      });
    }
    return box;
  };

  B.noirHairline = function (x1, x2, y, o = {}) {
    return line(this, this.svg, x1, y, x2, y, o);
  };
})();
