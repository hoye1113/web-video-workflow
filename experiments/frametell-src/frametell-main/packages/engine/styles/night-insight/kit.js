/* Night insight kit · 组件 + 7 个页面布局。
 *
 * 页面代码只写一行：
 *   ENGINE.visual('p01', (P) => NIGHT.render(P, SCRIPT.NIGHT.p01));
 * 布局数据放在 script.js 的 SCRIPT.NIGHT 里（或项目自己的 night-spec.js）。
 *
 * 原则：
 *   - 所有组件都是 DOM，位置用 1920×1080 的绝对坐标；
 *   - 入场统一走 PV.show 的淡入 + 上浮，时间用 P.c(i) 跟 cue 对齐；
 *   - 不抢字幕带：底部 180px 只放 caption / 进度，不放主图。
 */
(function () {
  const { h, clamp, ease } = PV;
  let uid = 0;
  const nid = (p) => p + (++uid);

  const abs = (e, x, y, w, hh) => {
    e.style.left = x + 'px';
    e.style.top = y + 'px';
    if (w != null) e.style.width = w + 'px';
    if (hh != null) e.style.height = hh + 'px';
    return e;
  };
  const add = (P, tag, cls, html, parent) => h(tag, cls, html, parent || P.html);
  const fade = (P, e, at, o = {}) => {
    e.classList.add('anim');
    P.show(e, { at: Math.max(0, at), dur: o.dur ?? 0.5, dy: o.dy ?? 24, dx: o.dx ?? 0, scale: o.scale });
    return e;
  };
  const growX = (P, e, at, dur = 0.45) => {
    e.classList.add('anim');
    e.style.transformOrigin = 'left center';
    e.style.transform = 'scaleX(0)';
    P.tick((lt) => {
      const k = ease.out(clamp((lt - at) / dur));
      e.style.opacity = k.toFixed(3);
      e.style.transform = `scaleX(${k.toFixed(4)})`;
    });
    return e;
  };

  const ICONS = {
    toolbox: `<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 17h30v22H9z"/><path d="M17 17v-5h14v5"/><path d="M9 25h30"/><path d="M20 25v5h8v-5"/></svg>`,
    eye: `<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 24s7-10 18-10 18 10 18 10-7 10-18 10S6 24 6 24Z"/><circle cx="24" cy="24" r="5.5"/><path d="M24 38v4"/></svg>`,
    ear: `<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M16 10c8 0 12 6 12 14v7c0 4 2 6 6 6"/><path d="M11 25c0 7 5 12 12 12"/><path d="M13 16c3-4 8-6 13-6"/></svg>`,
    bulb: `<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M24 8a11 11 0 0 0-7 19.6V34h14v-6.4A11 11 0 0 0 24 8Z"/><path d="M19 39h10"/><path d="M21 34v5M27 34v5"/></svg>`,
    warning: `<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M24 7 43 40H5L24 7Z"/><path d="M24 19v10"/><circle cx="24" cy="34" r="1.4" fill="currentColor" stroke="none"/></svg>`,
  };

  const icon = (name, color = '#35E0D0') =>
    `<span class="icon" style="color:${color}">${ICONS[name] || ICONS.eye}</span>`;

  function hud(P, root, chapter, name, at) {
    const box = abs(add(P, 'div', 'hud', '', root), 72, 48, 1776, null);
    box.innerHTML = `<div class="chapter"><b>${chapter || '01'}</b><i></i><span>${name || ''}</span></div><div class="brand">心理图解 · 夜读</div>`;
    fade(P, box, at ?? 0, { dy: 0, dur: 0.45 });
    return box;
  }

  function kicker(P, root, text, x, y, at, orange) {
    const e = abs(add(P, 'div', 'kicker' + (orange ? ' orange' : ''), text, root), x, y, null, null);
    return fade(P, e, at, { dy: 18, dur: 0.4 });
  }

  function title(P, root, lines, x, y, at, o = {}) {
    const box = abs(add(P, 'div', 'ni-title', '', root), x, y, o.w || 1100, null);
    const cls = o.cls || 'h2';
    lines.forEach((line, i) => {
      const e = add(P, 'div', cls + (o.big ? ' big' : ''), line, box);
      fade(P, e, at + i * (o.step ?? 0.16), { dy: 30, dur: 0.55 });
    });
    return box;
  }

  function lead(P, root, html, x, y, at, o = {}) {
    const e = abs(add(P, 'div', 'lead', html, root), x, y, o.w || 760, null);
    e.style.fontSize = (o.size || 36) + 'px';
    return fade(P, e, at, { dy: 22, dur: 0.55 });
  }

  function caption(P, root, html, at, o = {}) {
    const e = abs(add(P, 'div', 'caption' + (o.cyan ? ' cyan' : ''), html, root), 120, o.y || 936, 1680, null);
    return fade(P, e, at, { dy: 16, dur: 0.45 });
  }

  function panel(P, root, x, y, w, hh, at, cls, html) {
    const e = abs(add(P, 'div', 'panel ' + (cls || ''), html || '', root), x, y, w, hh);
    return fade(P, e, at, { dy: 28, dur: 0.5 });
  }

  function phone(P, root, x, y, w, hh, data, at) {
    const box = abs(add(P, 'div', 'phone', '', root), x, y, w, hh);
    box.innerHTML = `<div class="phone-head"><span class="avatar-sm"></span><span class="who">${data.name || '她'}</span><span class="status">${data.status || '在线'}</span></div><div class="chat"></div>`;
    const chat = box.querySelector('.chat');
    const messages = data.messages || [];
    messages.forEach((m, i) => {
      const b = add(P, 'div', 'bubble ' + (m.side === 'out' ? 'out' : 'in') + (m.dim ? ' dim' : ''), m.text, chat);
      fade(P, b, at + 0.28 + i * 0.42, { dy: 16, dur: 0.4 });
    });
    if (data.read) {
      const r = add(P, 'div', 'read', data.read, chat);
      fade(P, r, at + 0.28 + messages.length * 0.42, { dy: 8, dur: 0.35 });
    }
    if (data.typing) {
      const t = add(P, 'div', 'typing', '<i></i><i></i><i></i><span>' + data.typing + '</span>', box);
      fade(P, t, at + 0.4 + messages.length * 0.42, { dy: 8, dur: 0.35 });
    }
    fade(P, box, at, { dy: 38, dur: 0.6, scale: 0.97 });
    return box;
  }

  function heart(P, root, x, y, size, at, o = {}) {
    const id = nid('ni-heart-');
    const e = abs(add(P, 'div', 'heart-wrap', '', root), x, y, size, size);
    e.innerHTML = `<svg class="heart-svg" viewBox="0 0 200 200" aria-hidden="true">
      <defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="${o.a || '#35E0D0'}"/><stop offset=".55" stop-color="${o.b || '#2BB6AA'}"/><stop offset="1" stop-color="${o.c || '#FFA23A'}"/>
      </linearGradient></defs>
      <path d="M100 174C82 158 28 125 28 78c0-28 20-46 44-46 13 0 24 6 28 16 4-10 15-16 28-16 24 0 44 18 44 46 0 47-54 80-72 96Z"
        fill="${o.fill || 'rgba(53,224,208,.035)'}" stroke="url(#${id})" stroke-width="${o.sw || 3.5}"/>
      ${o.crack === false ? '' : '<path class="crack" d="M100 54l-8 34 18 12-12 28 22 14-10 24"/><path class="crack" d="M64 84l24 8M138 104l-20 12" opacity=".8"/>'}
    </svg>`;
    return fade(P, e, at, { dy: 30, dur: 0.7, scale: 0.9 });
  }

  function card(P, root, x, y, w, hh, d, at) {
    const e = panel(P, root, x, y, w, hh, at, d.color || 'orange', '');
    e.classList.add('card');
    e.innerHTML = `${d.tag ? `<span class="tag ${d.tagColor || d.color || 'orange'}"><i class="dot"></i>${d.tag}</span>` : ''}
      ${d.icon ? icon(d.icon, d.iconColor || (d.color === 'cyan' ? '#35E0D0' : '#FFA23A')) : ''}
      <h3>${d.title || ''}</h3>
      <p>${(d.items || []).join('<br>')}</p>`;
    return e;
  }

  function wall(P, root, x, y, w, hh, text, at, color) {
    const e = abs(add(P, 'div', 'wall ' + (color || ''), `<span>${text}</span>`, root), x, y, w, hh);
    return fade(P, e, at, { dy: 24, dur: 0.5, scale: 1.04 });
  }

  function avatar(P, root, x, y, size, color, name, at) {
    const e = abs(add(P, 'div', 'avatar ' + (color || ''), name ? `<span class="name">${name}</span>` : '', root), x, y, size, size);
    return fade(P, e, at, { dy: 24, dur: 0.55 });
  }

  function dash(P, root, x, y, w, at) {
    const e = abs(add(P, 'div', 'dash', '', root), x, y, w, 1);
    return growX(P, e, at, 0.5);
  }

  function arrow(P, root, x, y, w, at) {
    const e = abs(add(P, 'div', 'arrow', '', root), x, y, w, 2);
    return growX(P, e, at, 0.45);
  }

  function quote(P, root, x, y, w, hh, d, at, tail) {
    const e = abs(add(P, 'div', 'panel quote' + (tail ? ' tail' : ''), '', root), x, y, w, hh);
    e.innerHTML = `${d.label ? `<div class="label">${d.label}</div>` : ''}<div class="q">${d.text || ''}</div>`;
    return fade(P, e, at, { dy: 28, dur: 0.5 });
  }

  function choice(P, root, x, y, w, hh, d, at) {
    const e = panel(P, root, x, y, w, hh, at, d.color || 'cyan', '');
    e.classList.add('choice');
    e.innerHTML = `${d.icon ? icon(d.icon, d.color === 'orange' ? '#FFA23A' : '#35E0D0') : ''}<div><h3>${d.title || ''}</h3><p>${d.sub || ''}</p></div>`;
    return e;
  }

  function switchEl(P, root, x, y, at) {
    const e = abs(add(P, 'div', 'switch', '', root), x, y, 92, 44);
    return fade(P, e, at, { dy: 16, dur: 0.4, scale: 0.8 });
  }

  function end(P, root, d, at) {
    const wrap = add(P, 'div', 'end-wrap', '', root);
    const k = add(P, 'div', 'end-kicker', d.kicker || '', wrap);
    fade(P, k, at + 0.05, { dy: 16, dur: 0.4 });
    const t = add(P, 'div', 'end-title', (d.title || []).join('<br>'), wrap);
    fade(P, t, at + 0.18, { dy: 30, dur: 0.55 });
    const ring = add(P, 'div', 'end-ring', '', wrap);
    ring.innerHTML = `<div class="end-pair"><div class="avatar cyan"></div><div class="avatar orange"></div></div>`;
    fade(P, ring, at + 0.45, { dy: 24, dur: 0.6, scale: 0.92 });
    if (d.note) { const n = add(P, 'div', 'end-note', d.note, wrap); fade(P, n, at + 0.8, { dy: 16, dur: 0.4 }); }
    if (d.sub) { const s = add(P, 'div', 'end-sub', d.sub, wrap); fade(P, s, at + 1.0, { dy: 12, dur: 0.4 }); }
    return wrap;
  }

  function render(P, s) {
    const root = add(P, 'div', 'ni', '', P.html);
    const cue = (i, dt = 0) => Math.max(0, P.c(Math.min(i, P.page.cues.length - 1)) + dt);
    const t0 = cue(0);
    const t1 = cue(1);
    const t2 = cue(2);
    const t3 = cue(3);
    hud(P, root, s.chapter, s.name, t0 - 0.2);

    switch (s.layout) {
      case 'hook': {
        kicker(P, root, s.kicker || '', 790, 190, t0 - 0.1);
        title(P, root, s.title || [], 790, 250, t0, { cls: 'h1', big: true, w: 930 });
        if (s.lead) lead(P, root, s.lead, 790, 600, t0 + 0.35, { w: 720 });
        if (s.phone) phone(P, root, 150, 212, 486, 650, s.phone, t0 - 0.05);
        heart(P, root, 1150, 600, 420, t0 + 0.35);
        if (s.note) { const n = abs(add(P, 'div', 'heart-note', s.note, root), 1268, 970, null, null); fade(P, n, t0 + 1.2, { dy: 10, dur: 0.4 }); }
        break;
      }
      case 'split': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1200 });
        if (s.left) card(P, root, 140, 400, 600, 420, s.left, t0 + 0.05);
        if (s.right) card(P, root, 1180, 400, 600, 420, s.right, t0 + 0.16);
        if (s.wall) wall(P, root, 856, 380, 208, 500, s.wall, t0 + 0.28);
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
      case 'translate': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1100 });
        const left = abs(add(P, 'div', 'panel said-card', '', root), 210, 430, 470, 220);
        left.innerHTML = `<div class="label">${s.saidLabel || '你的安慰'}</div><div class="said">${s.said || ''}</div>`;
        fade(P, left, t0 + 0.05, { dy: 26, dur: 0.45 });
        arrow(P, root, 720, 520, 230, t0 + 0.25);
        const right = abs(add(P, 'div', 'panel red heard-card', '', root), 1020, 386, 720, 240);
        right.innerHTML = `<div class="label">${s.heardLabel || '她听到的'}</div><div class="heard">${s.heard || ''}</div><div class="strike"></div>`;
        fade(P, right, t0 + 0.35, { dy: 26, dur: 0.45 });
        const strike = right.querySelector('.strike');
        strike.style.top = '115px';
        growX(P, strike, t0 + 0.75, 0.4);
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
      case 'wall': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1200 });
        const floor = abs(add(P, 'div', 'floor', '', root), 200, 700, 1520, 1);
        growX(P, floor, t0 + 0.1, 0.5);
        avatar(P, root, 470, 560, 126, 'cyan', s.leftName || '你', t0 + 0.05);
        avatar(P, root, 1320, 560, 126, 'orange', s.rightName || '她', t0 + 0.15);
        dash(P, root, 602, 640, 716, t0 + 0.25);
        wall(P, root, 860, 350, 200, 430, s.wall || '道理', t0 + 0.32, 'orange');
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
      case 'heart': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1100 });
        const ring = abs(add(P, 'div', 'ring', '', root), 1040, 360, 560, 560);
        fade(P, ring, t0 + 0.05, { dy: 20, dur: 0.6, scale: 0.92 });
        heart(P, root, 1110, 430, 420, t0 + 0.12, { a: '#35E0D0', b: '#FFA23A', c: '#FF7A45', fill: 'rgba(255,162,58,.08)', sw: 4 });
        if (s.quote) quote(P, root, 260, 460, 620, 300, s.quote, t0 + 0.25, true);
        if (s.tool) { const t = abs(add(P, 'div', 'panel tool', `<div class="t">${s.tool.title || '方案'}</div><div class="l">${s.tool.sub || '先放一边'}</div>`, root), 1500, 760, 270, 100); fade(P, t, t0 + 0.65, { dy: 18, dur: 0.4 }); }
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
      case 'choice': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1200 });
        if (s.left) choice(P, root, 200, 400, 700, 330, s.left, t0 + 0.05);
        if (s.right) choice(P, root, 1020, 400, 700, 330, s.right, t0 + 0.16);
        switchEl(P, root, 914, 520, t0 + 0.35);
        if (s.quote) {
          const q = abs(add(P, 'div', 'panel choice-quote', s.quote, root), 300, 820, 1320, 120);
          fade(P, q, t0 + 0.5, { dy: 22, dur: 0.45 });
        }
        break;
      }
      case 'list': {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1680 });
        const box = abs(add(P, 'div', 'panel list', '', root), 120, 400, 1680, 400);
        const rows = [];
        (s.items || []).slice(0, 4).forEach((text, i) => {
          const row = add(P, 'div', 'list-item', `<span class="list-no">0${i + 1}</span><span>${text}</span>`, box);
          rows.push(row);
          fade(P, row, t0 + 0.1 + i * 0.22, { dy: 18, dur: 0.4 });
        });
        fade(P, box, t0 + 0.05, { dy: 24, dur: 0.5 });
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
      case 'end': {
        end(P, root, s, t0);
        break;
      }
      default: {
        kicker(P, root, s.kicker || '', 120, 132, t0 - 0.2);
        title(P, root, s.title || [], 120, 190, t0, { cls: 'h2', w: 1200 });
        if (s.caption) caption(P, root, s.caption, t1 + 0.15);
        break;
      }
    }
    return root;
  }

  window.NIGHT = { render, hud, kicker, title, lead, caption, panel, phone, heart, card, wall, avatar, dash, arrow, quote, choice, switchEl, end, icon, growX };
})();
