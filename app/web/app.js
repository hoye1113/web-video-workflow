const $ = (id) => document.getElementById(id);
let projects = [], project = null, shotId = null, jobs = [], seenDone = new Set();

// ---------------------------------------------------------------- API

async function api(path, opt = {}) {
  const r = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opt,
    body: opt.body ? JSON.stringify(opt.body) : undefined,
  });
  const t = await r.text();
  let d = null;
  try { d = t ? JSON.parse(t) : null; } catch { d = { raw: t }; }
  if (!r.ok) throw new Error((d && d.error) || `HTTP ${r.status}`);
  return d;
}
const post = (p, b) => api(p, { method: "POST", body: b });
const put = (p, b) => api(p, { method: "PUT", body: b });

function say(el, txt, bad) { el.textContent = txt || ""; el.style.color = bad ? "#E08A78" : ""; }

// ---------------------------------------------------------------- 项目

async function loadProjects(select) {
  projects = await api("/api/projects");
  const sel = $("projectSel");
  sel.innerHTML = "";
  if (!projects.length) {
    sel.innerHTML = `<option value="">（还没有项目）</option>`;
    return;
  }
  for (const p of projects) {
    const o = document.createElement("option");
    o.value = p.name; o.textContent = `${p.title}（${p.rendered}/${p.shots}）`;
    sel.appendChild(o);
  }
  const name = select || project?.name || projects[0].name;
  sel.value = name;
  await openProject(name);
}

async function openProject(name) {
  project = await api(`/api/projects/${name}`);
  project.name = name;
  $("script").value = project.script || "";
  shotId = project.shots?.[0]?.id || null;
  renderPresets(); renderSkeleton(); renderShots(); renderShotForm();
  refreshPreview(); updateCount();
}

// ---------------------------------------------------------------- 长任务的结果处理

function applyResult(j) {
  const r = j.result || {};
  if (j.kind === "shotlist") {
    project.shots = r.shots || [];
    project.skeleton = r.skeleton || [];
    project.approved = false;
    shotId = project.shots[0]?.id || null;
    renderSkeleton(); renderShots(); renderShotForm(); refreshPreview(); updateCount();
    say($("shotlistState"), `骨架 ${project.skeleton.length} 段 · ${project.shots.length} 页`);
  } else if (j.kind === "scene") {
    $("code").value = r.source || "";
    openDrawer();
    say($("saveState"), "场景代码写好了");
    refreshPreview();
  } else if (j.kind === "review") {
    lastReview = r.review || {};
    renderReview();
  } else if (j.kind === "revise") {
    $("code").value = r.source || "";
    openDrawer();
    const st = $("revState");
    if (st) st.textContent = "改好了，自动重抽帧…";
    post("/api/stills", { project: project.name, shot: shotId }).then(refreshJobs).catch(() => {});
  }
}

function applyFailure(j) {
  const msg = j.error || "任务失败";
  if (j.kind === "shotlist") say($("shotlistState"), msg, true);
  else if (j.kind === "scene") say($("saveState"), msg, true);
  else if (j.kind === "review" || j.kind === "revise") {
    $("reviewBody").innerHTML = `<span style="color:#E08A78">${esc(msg)}</span>`;
  }
}

// ---------------------------------------------------------------- 风格预设

let presets = [];

async function loadPresets() {
  presets = await api("/api/presets");
  renderPresets();
}

function renderPresets() {
  const cur = project?.style?.preset;
  const box = $("presetList");
  box.innerHTML = presets.map((p) => `
      <span class="preset ${p.id === cur ? "on" : ""}" data-id="${p.id}">
        <span class="sw">${p.swatch.map((c) => `<i style="background:${c}"></i>`).join("")}</span>${esc(p.name)}
      </span>`).join("");
  box.querySelectorAll(".preset").forEach((el) => { el.onclick = () => pickPreset(el.dataset.id); });
  const p = presets.find((x) => x.id === cur);
  $("styleState").textContent = project && !p ? "没选" : "";
  $("styleHint").textContent = p ? p.hint : "选一套画风，全片只用这一套。";
}

async function pickPreset(id) {
  if (!project) return say($("saveState"), "先选一个项目", true);
  try {
    project = await put(`/api/projects/${project.name}`, { style: { preset: id } });
    renderPresets();
    say($("saveState"), "画风已换");
  } catch (e) { say($("saveState"), e.message, true); }
}

// ---------------------------------------------------------------- 叙事骨架

function renderSkeleton() {
  const sk = project?.skeleton || [];
  const box = $("skelPanel");
  box.style.display = sk.length ? "flex" : "none";
  if (!sk.length) return;
  const counts = {};
  for (const s of project.shots || []) counts[s.role] = (counts[s.role] || 0) + 1;
  const cur = currentShot()?.role;
  $("skeleton").innerHTML = sk
    .map((r, i) => `${i ? '<span class="arrow">→</span>' : ""}<span class="chip ${r === cur ? "on" : ""}"><i></i>${esc(r)}${counts[r] ? ` · ${counts[r]}` : ""}</span>`)
    .join("");
  const ok = !!project.approved;
  $("btnApprove").style.display = ok ? "none" : "";
  $("skelState").textContent = ok
    ? "已确认"
    : `${sk.length} 段 · ${project.shots?.length || 0} 页`;
}

async function approve() {
  await saveProject({ approved: true });
  renderSkeleton();
  say($("saveState"), "骨架已确认");
}

async function newProject() {
  const name = $("newName").value.trim();
  if (!name) return say($("saveState"), "先填项目名", true);
  try {
    await post("/api/projects", { name, title: name });
    $("newName").value = "";
    await loadProjects(name);
    say($("saveState"), "建好了");
  } catch (e) { say($("saveState"), e.message, true); }
}

async function saveProject(patch = {}) {
  if (!project) return;
  project = await put(`/api/projects/${project.name}`, patch);
  say($("saveState"), "已保存");
  setTimeout(() => say($("saveState"), ""), 1200);
}

// ---------------------------------------------------------------- 切镜头

async function makeShotlist() {
  if (!project) return;
  const script = $("script").value.trim();
  if (!script) return say($("shotlistState"), "先贴文案", true);
  say($("shotlistState"), "已进队列，模型在读文案…");
  $("btnShotlist").disabled = true;
  try {
    await post("/api/shotlist", { project: project.name, script });
    refreshJobs();
  } catch (e) {
    say($("shotlistState"), e.message, true);
  } finally { $("btnShotlist").disabled = false; }
}

// ---------------------------------------------------------------- 镜头

function renderShots() {
  const ul = $("shotList"); ul.innerHTML = "";
  for (const s of project?.shots || []) {
    const li = document.createElement("li");
    li.className = s.id === shotId ? "on" : "";
    const dur = Number(s.dur || 0).toFixed(Number(s.dur) % 1 ? 1 : 0);
    // 代码状态：没写过 / 设定改了要重写 / 有代码
    const code = !s.hasScene ? `<i class="st" title="还没写场景代码"></i>`
      : s.stale ? `<i class="st warn" title="页的设定改过了，这版代码是旧的"></i>`
        : `<i class="st ok" title="有代码"></i>`;
    li.innerHTML = `<span class="no">${s.id}</span>
        <span class="t"><em>${esc(s.role || "")}</em>${esc(s.title || "（没写画面）")}</span>
        <span class="m">${code}<i class="st ${s.status || ""}"></i>${dur}s</span>`;
    li.onclick = () => { shotId = s.id; renderShots(); renderShotForm(); renderSkeleton(); };
    ul.appendChild(li);
  }
}

function currentShot() { return (project?.shots || []).find((s) => s.id === shotId) || null; }
const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function renderShotForm() {
  const s = currentShot();
  $("shotForm").style.display = s ? "flex" : "none";
  $("shotEmpty").style.display = s ? "none" : "block";
  if (!s) return;
  $("shotTag").textContent = `#${s.id}${s.role ? " · " + s.role : ""}`;
  $("fRole").value = s.role || "";
  $("fTitle").value = s.title || "";
  $("fDur").value = s.dur ?? 15;
  $("fCamera").value = s.camera || "停";
  $("fText").value = s.text || "";
  $("fNarration").value = s.narration || "";
  $("fNote").value = s.note || "";
}

let saveTimer = null;
function patchShot(patch) {
  if (!project || !shotId) return;
  const s = currentShot(); if (!s) return;
  Object.assign(s, patch);
  renderShots();
  clearTimeout(saveTimer);
  saveTimer = setTimeout(async () => {
    try { await put(`/api/projects/${project.name}/shots/${shotId}`, patch); say($("saveState"), "已保存"); }
    catch (e) { say($("saveState"), e.message, true); }
    setTimeout(() => say($("saveState"), ""), 900);
  }, 500);
}

// ---------------------------------------------------------------- 预览

function refreshPreview() {
  if (!project) return;
  const url = `/engine/index.html?film=demos/${project.name}&t=${Date.now()}`;
  $("preview").src = url;
  const n = project.shots?.length || 0;
  const secs = (project.shots || []).reduce((a, s) => a + Number(s.dur || 0), 0);
  $("previewHint").textContent = n
    ? `正在连续预览 ${n} 页（共 ${Math.round(secs)} 秒）。页与页之间是硬切。`
    : "这个项目还没有页面。先在上面贴文案、点「切成页面」。";
}
function reloadPreview() { refreshPreview(); }
function playPreview() {
  const w = $("preview").contentWindow;
  try { w.document.getElementById("play")?.click(); } catch { /* 还没加载完 */ }
}

// ---------------------------------------------------------------- 任务

async function refreshJobs() {
  try { jobs = await api("/api/jobs"); } catch { return; }
  const ul = $("jobList"); ul.innerHTML = "";
  for (const j of jobs) {
    const pct = Math.round((j.progress || 0) * 100);
    const cls = j.status === "done" ? "ok" : j.status === "failed" ? "bad" : "";
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="jt"><span>${esc(j.title)}</span>
        <span class="muted">${j.status === "running" ? `${j.frames[0]}/${j.frames[1]} · ${j.elapsed}s` : j.status}</span></div>
      <div class="bar"><i class="${cls}" style="width:${j.status === "failed" ? 100 : pct}%"></i></div>
      ${j.error ? `<div class="err">${esc(j.error)}</div>` : ""}
      ${j.out && j.status === "done" ? `<div style="margin-top:7px"><a class="muted" style="color:var(--accent2)" href="/${j.out}" target="_blank">打开产物 ↗</a></div>` : ""}`;
    ul.appendChild(li);
    if (j.status === "done" && !seenDone.has(j.id)) {
      seenDone.add(j.id);
      if (j.result) applyResult(j);
      if (j.kind === "shot" || j.kind === "preview") onShotRendered(j);
      if (j.kind === "still") { $("reviewBox").classList.add("open"); runReview(); }   // 抽完帧直接进导演回路
    }
    if (j.status === "failed" && !seenDone.has(j.id)) {
      seenDone.add(j.id);
      applyFailure(j);
    }
  }
}

function onShotRendered(job) {
  const m = /镜 ([a-z0-9_]+)/.exec(job.title);
  const s = m && (project?.shots || []).find((x) => x.id === m[1]);
  if (s && s.status !== "rendered") { s.status = "rendered"; renderShots(); }
}

async function queue(name, body, msgEl) {
  if (!project) return;
  say(msgEl || $("saveState"), "排队中…");
  try {
    await post(name, { project: project.name, ...body });
    say(msgEl || $("saveState"), "已进队列");
    refreshJobs();
  } catch (e) { say(msgEl || $("saveState"), e.message, true); }
}

// ---------------------------------------------------------------- 场景代码 / 导演回路

async function writeScene() {
  if (!shotId) return;
  say($("saveState"), "模型在写这一页的代码…");
  $("btnScene").disabled = true;
  try {
    await post("/api/scene", { project: project.name, shot: shotId });
    refreshJobs();
  } catch (e) { say($("saveState"), e.message, true); }
  finally { $("btnScene").disabled = false; }
}

async function openCode() {
  if (!shotId) return;
  const r = await api(`/api/projects/${project.name}/scene/${shotId}`);
  $("code").value = r.source || "// 这一镜还没有代码。点「写场景代码」，或自己写。\n";
  openDrawer();
}
function openDrawer() { $("drawerTitle").textContent = `场景代码 · 镜 ${shotId}`; $("drawer").classList.add("open"); }
function closeDrawer() { $("drawer").classList.remove("open"); }

async function saveCode() {
  if (!shotId) return;
  try {
    await put(`/api/projects/${project.name}/scene/${shotId}`, { source: $("code").value });
    say($("saveState"), "代码已保存");
    refreshPreview();
  } catch (e) { say($("saveState"), e.message, true); }
}

async function runReview() {
  if (!shotId) return;
  $("reviewBody").innerHTML = `<span class="muted">模型在看帧…</span>`;
  $("btnReview").disabled = true;
  try {
    await post("/api/review", { project: project.name, shot: shotId });
    refreshJobs();
  } catch (e) {
    $("reviewBody").innerHTML = `<span style="color:#E08A78">${esc(e.message)}</span>`;
  } finally { $("btnReview").disabled = false; }
}

let lastReview = null;

function renderReview() {
  const v = lastReview || {};
  const probs = (v.problems || []).map((p) => `<li>${esc(p)}</li>`).join("") || "<li>没挑出问题</li>";
  const fixes = (v.fixes || []).map((p) => `<li>${esc(p)}</li>`).join("") || "<li>—</li>";
  $("reviewBody").innerHTML = `
    <div style="color:${v.ok ? "var(--ok)" : "var(--accent)"};font-weight:600;margin-bottom:10px">
      ${v.ok ? "✓ 模型认为这一镜能用" : "✗ 模型认为还要改"}
    </div>
    <h4>问题</h4><ul>${probs}</ul>
    <h4>怎么改</h4><ul>${fixes}</ul>
    ${v.ok ? "" : `<div class="row" style="margin-top:14px">
      <button id="btnRevise" class="btn primary xs">按这些意见改代码</button>
      <span class="muted small">改完会自动重渲一次，再跑一遍导演回路</span></div>`}`;
  const rb = $("btnRevise");
  if (rb) rb.onclick = reviseAndRerender;
}

async function reviseAndRerender() {
  if (!shotId || !lastReview) return;
  $("btnRevise").disabled = true;
  $("reviewBody").insertAdjacentHTML("beforeend", `<p class="muted small" id="revState">模型在改代码…</p>`);
  try {
    await post("/api/revise", { project: project.name, shot: shotId, review: lastReview });
    refreshJobs();
  } catch (e) {
    const st = $("revState");
    if (st) st.innerHTML = `<span style="color:#E08A78">${esc(e.message)}</span>`;
  } finally { const b = $("btnRevise"); if (b) b.disabled = false; }
}

async function showVersions() {
  if (!shotId) return;
  try {
    const vs = await post("/api/versions", { project: project.name, shot: shotId });
    $("reviewBox").classList.add("open");
    const rows = vs.length
      ? vs.map((v) => `<li><b>v${v.n}</b> · ${v.score >= 0 ? v.score + " 分" : "未评审"}
          ${v.ok ? '<span style="color:var(--ok)">✓</span>' : ""}
          ${v.problems?.length ? `<span class="muted">· ${v.problems.length} 条问题</span>` : ""}</li>`).join("")
      : "<li>还没有版本。跑一次「自动跑导演回路」就会每轮存一版。</li>";
    $("reviewBody").innerHTML = `
      <h4>版本存档</h4><ul>${rows}</ul>
      <p class="muted small">回路结束后，场景文件会自动回写成分数最高的那一版。</p>`;
  } catch (e) { $("reviewBody").innerHTML = `<span style="color:#E08A78">${esc(e.message)}</span>`; }
}

// ---------------------------------------------------------------- 事件

$("btnNewProject").onclick = newProject;
$("projectSel").onchange = (e) => e.target.value && openProject(e.target.value);
$("btnShotlist").onclick = makeShotlist;
$("btnApprove").onclick = approve;
$("script").onchange = () => saveProject({ script: $("script").value });
$("btnReload").onclick = reloadPreview;
$("btnPlay").onclick = playPreview;
$("fTitle").onchange = (e) => patchShot({ title: e.target.value });
$("fRole").onchange = (e) => { patchShot({ role: e.target.value }); renderSkeleton(); };
$("fDur").onchange = (e) => { patchShot({ dur: Number(e.target.value) || 15 }); refreshPreview(); updateCount(); };
$("fCamera").onchange = (e) => patchShot({ camera: e.target.value });
$("fText").onchange = (e) => patchShot({ text: e.target.value });
$("fNote").onchange = (e) => patchShot({ note: e.target.value });
$("fNarration").onchange = (e) => patchShot({ narration: e.target.value });
$("btnScene").onclick = writeScene;
$("btnCode").onclick = openCode;
$("btnSaveCode").onclick = saveCode;
$("btnCloseCode").onclick = closeDrawer;
$("btnStills").onclick = () => queue("/api/stills", { shot: shotId });
$("btnRender").onclick = () => queue("/api/render", { shot: shotId });
$("btnDirector").onclick = () => {
  if (!shotId) return;
  const rounds = Number($("fRounds").value || 3);
  const mins = Math.round(rounds * 3);
  if (!confirm(`自动跑 ${rounds} 轮导演回路？\n\n每轮：渲帧 → 打分 → 改代码 → 存档。\n最后只保留得分最高的那一版。\n预计 ${mins} 到 ${mins * 2} 分钟。`)) return;
  queue("/api/director", { shot: shotId, rounds });
};
$("btnVersions").onclick = showVersions;
$("btnConcat").onclick = () => queue("/api/concat", {});
$("btnClearJobs").onclick = async () => { await post("/api/jobs/clear"); refreshJobs(); };
$("btnReview").onclick = runReview;
$("btnCloseReview").onclick = () => $("reviewBox").classList.remove("open");
$("btnDelete").onclick = async () => {
  if (!shotId) return;
  project.shots = project.shots.filter((s) => s.id !== shotId);
  await saveProject({ shots: project.shots });
  shotId = project.shots[0]?.id || null;
  renderShots(); renderShotForm(); refreshPreview(); updateCount();
};
function updateCount() {
  const n = project?.shots?.length || 0;
  const secs = (project?.shots || []).reduce((a, s) => a + Number(s.dur || 0), 0);
  $("shotCount").textContent = n ? `${n} 页 · ${Math.round(secs)}s` : "";
}

// 抽帧完自动弹导演回路（逻辑已并进 refreshJobs）

loadProjects().then(loadPresets).then(refreshJobs);
setInterval(refreshJobs, 1600);
