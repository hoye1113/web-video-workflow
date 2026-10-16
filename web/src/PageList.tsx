import type { Shot } from "./api";

/** 左栏：页面列表。**只读的状态显示**，不是操作面板。 */
export function PageList({
  shots, current, onPick,
}: { shots: Shot[]; current: string | null; onPick: (id: string) => void }) {
  // 按骨架分段分组：28 行平铺看不出版片结构，分组后一屏看到的是"哪一段有几页"
  const groups: { role: string; items: Shot[] }[] = [];
  for (const s of shots) {
    const role = s.role || "（未分段）";
    const g = groups[groups.length - 1];
    if (g && g.role === role) g.items.push(s);
    else groups.push({ role, items: [s] });
  }

  return (
    <div className="panel">
      <div className="panel-head">
        <span>页面</span>
        <span className="muted">
          {shots.length} 页 · {Math.round(shots.reduce((a, s) => a + (s.dur || 0), 0))}s
          {shots.some((s) => s.mode === "image" || s.mode === "mixed") && (
            <> · 生图 {shots.filter((s) => s.mode === "image" || s.mode === "mixed").length}</>
          )}
        </span>
      </div>
      <ul className="pages">
        {groups.map((g) => (
          <li key={g.role} className="group">
            <div className="group-head">
              {g.role}
              <span className="muted">{g.items.length} 页</span>
            </div>
            {g.items.map((s) => {
              const code = !s.hasScene ? "none" : s.stale ? "stale" : "has";
              return (
                <div key={s.id} className={`row ${s.id === current ? "on" : ""}`} onClick={() => onPick(s.id)}>
                  <span className="no">{s.id}</span>
                  <span className="t">{s.title}</span>
                  <span className="m">
                    {s.mode && s.mode !== "code" && (
                      <b className={`mode ${s.mode}`} title={s.mode === "image" ? "生图" : "生图 + 代码动效"}>
                        {s.mode === "image" ? "图" : "混"}
                      </b>
                    )}
                    <i className={`dot ${code}`} title={
                      code === "has" ? "有代码" : code === "stale" ? "设定改过了，代码是旧的" : "还没写"
                    } />
                    {Math.round(s.dur || 0)}s
                  </span>
                </div>
              );
            })}
          </li>
        ))}
        {shots.length === 0 && <li className="muted" style={{ padding: 12 }}>还没有页面</li>}
      </ul>
    </div>
  );
}
