import type { Job } from "./api";

/** 中栏：连续预览。直接嵌引擎自己的预览页（它本来就是完整的播放器）。 */
export function Preview({ project, tick }: { project: string; tick: number }) {
  const src = project ? `/engine/index.html?film=demos/${project}&t=${tick}` : "about:blank";
  return (
    <div className="panel grow">
      <div className="panel-head">
        <span>连续预览</span>
        <span className="muted">引擎实时渲染</span>
      </div>
      <div className="stage">
        <iframe key={tick} src={src} title="预览" />
      </div>
    </div>
  );
}

/** 右栏：任务。只读。 */
export function Jobs({ jobs }: { jobs: Job[] }) {
  return (
    <div className="panel">
      <div className="panel-head">
        <span>任务</span>
        <span className="muted">{jobs.filter((j) => j.status === "running").length} 个在跑</span>
      </div>
      <ul className="jobs">
        {jobs.slice(0, 12).map((j) => (
          <li key={j.id}>
            <div className="jt">
              <span className="ellip">{j.title}</span>
              <span className="muted">
                {j.status === "running"
                  ? `${j.frames[0]}/${j.frames[1]} · ${Math.round(j.elapsed)}s`
                  : j.status}
              </span>
            </div>
            <div className="jbar">
              <i
                className={j.status === "done" ? "ok" : j.status === "failed" ? "bad" : ""}
                style={{ width: `${j.status === "failed" ? 100 : Math.round((j.progress || 0) * 100)}%` }}
              />
            </div>
            {j.error && <div className="err">{j.error.slice(0, 200)}</div>}
          </li>
        ))}
        {jobs.length === 0 && <li className="muted">还没有任务</li>}
      </ul>
    </div>
  );
}
