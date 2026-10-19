"""面板 ↔ OpenCode agent 的桥：**素材阶段交给 material agent**。

用桌面版自带的 CLI 走它的本地服务（它会自己处理鉴权，不用碰 service.json 里的密码）：
    opencode-cli.exe api get|post <path> --data '{…}'

我们会用到的四个接口（v2.0.30 实测）：
    POST /api/session                     建会话 {title, agent}
    POST /api/session/{id}/move           把会话挪到工程目录 {directory}
    POST /api/session/{id}/prompt         对 agent 说话 {text}
    GET  /api/session/{id}/message        读消息（Assistant 的 content 里是回复）
    GET  /api/permission/request          待批准的权限请求（工具调用）
    POST /api/session/{id}/permission/{rid}/reply   {decision: once|always|reject}

落盘（跟片子走）：
    projects/<片>/agent-session.json      {sessionID, seen: [消息 id]}
"""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLI = pathlib.Path.home() / "AppData" / "Local" / "Programs" / "@opencodedesktop" / "resources" / "opencode-cli.exe"


def _api(method, path, body=None):
    cmd = [str(CLI), "api", method, path]
    if body is not None:
        cmd += ["--data", json.dumps(body, ensure_ascii=False)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=180)
    out = (r.stdout or "").strip()
    if not out:                     # 有的接口就是 204 无响应体（例如 session move）
        if r.returncode == 0:
            return {}
        raise RuntimeError(f"opencode api 失败（{r.returncode}）：{(r.stderr or '')[:200]}")
    i = out.find("{") if "{" in out else out.find("[")
    if i < 0:
        raise RuntimeError(f"opencode api 没返回 JSON：{(out or r.stderr)[:200]}")
    return json.loads(out[i:])


def state_file(proj):
    return ROOT / "projects" / proj / "agent-session.json"


def load(proj):
    f = state_file(proj)
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            pass
    return {"sessionID": "", "seen": []}


def save(proj, st):
    state_file(proj).write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def ensure_session(proj, title=""):
    st = load(proj)
    if st.get("sessionID"):
        return st["sessionID"]
    d = _api("post", "/api/session", {"title": title or f"video-factory · {proj}",
                                      "agent": "material"})
    sid = (d.get("data") or d).get("id") or (d.get("data") or d).get("sessionID")
    if not sid:
        raise RuntimeError(f"建会话没拿到 id：{json.dumps(d, ensure_ascii=False)[:200]}")
    _api("post", f"/api/session/{sid}/move", {"directory": str((ROOT / "projects" / proj).as_posix())})
    st["sessionID"] = sid
    st["seen"] = []
    save(proj, st)
    return sid


def ask(proj, text):
    sid = ensure_session(proj)
    _api("post", f"/api/session/{sid}/prompt", {"text": text})
    return sid


def new_messages(proj):
    """读 agent 的新回复（Assistant 消息里的文本片段）。"""
    st = load(proj)
    sid = st.get("sessionID")
    if not sid:
        return [], []
    d = _api("get", f"/api/session/{sid}/message")
    items = d.get("data") if isinstance(d, dict) else d
    seen = set(st.get("seen") or [])
    fresh, ids = [], []
    for m in items or []:
        mid = m.get("id")
        if not mid or mid in seen:
            continue
        ids.append(mid)
        if m.get("type") != "assistant":
            continue
        txt = m.get("content")
        if isinstance(txt, list):
            parts = []
            for p in txt:
                if isinstance(p, dict):
                    if p.get("type") == "text" and p.get("text"):
                        parts.append(p["text"])
                    elif p.get("type") == "tool" and p.get("name"):
                        parts.append(f'（工具 {p["name"]}）')
            txt = "\n".join(parts)
        if txt and str(txt).strip():
            fresh.append(str(txt).strip())
    if ids:
        st["seen"] = (st.get("seen") or []) + ids
        save(proj, st)
    return fresh, ids


def pending_perms(proj):
    st = load(proj)
    sid = st.get("sessionID")
    if not sid:
        return []
    d = _api("get", "/api/permission/request")
    data = d.get("data") if isinstance(d, dict) else d
    return [p for p in (data or []) if p.get("sessionID") == sid]


def reply_perm(proj, rid, decision="once"):
    st = load(proj)
    sid = st.get("sessionID")
    _api("post", f"/api/session/{sid}/permission/{rid}/reply", {"decision": decision})
    return True
