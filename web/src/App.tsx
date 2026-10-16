import { useCallback, useEffect, useState } from "react";
// react-resizable-panels v4 改了导出名：PanelGroup→Group，PanelResizeHandle→Separator
import { Group, Panel, Separator } from "react-resizable-panels";
import { api, type Job, type Project } from "./api";
import { Chat } from "./Chat";
import { PageList } from "./PageList";
import { Jobs, Preview } from "./Panels";

export default function App() {
  const [names, setNames] = useState<{ name: string; title: string }[]>([]);
  const [project, setProject] = useState<Project | null>(null);
  const [shot, setShot] = useState<string | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [tick, setTick] = useState(0);
  const [err, setErr] = useState("");

  const loadProjects = useCallback(async () => {
    try {
      const ps = await api.projects();
      setNames(ps);
      if (ps.length && !project) {
        const p = ps.find((x) => x.name === "marriage_full") || ps[0];
        setProject(await api.project(p.name));
      }
    } catch (e: any) { setErr(e.message); }
  }, [project]);

  const refresh = useCallback(async () => {
    if (!project) return;
    try {
      setProject(await api.project(project.name));
      setJobs(await api.jobs());
    } catch (e: any) { setErr(e.message); }
  }, [project?.name]);

  useEffect(() => { loadProjects(); }, [loadProjects]);
  useEffect(() => {
    const t = setInterval(async () => {
      try { setJobs(await api.jobs()); } catch { /* 忽略 */ }
    }, 2000);
    return () => clearInterval(t);
  }, []);

  const pick = async (name: string) => {
    setProject(await api.project(name));
    setShot(null);
    setTick(Date.now());
  };

  return (
    <div className="app">
      <header className="bar">
        <span className="brand">代码生成视频工厂</span>
        <select value={project?.name || ""} onChange={(e) => pick(e.target.value)}>
          {names.map((n) => (
            <option key={n.name} value={n.name}>{n.title}（{n.name}）</option>
          ))}
        </select>
        {project?.style?.name && <span className="chip">{project.style.name}</span>}
        {project?.skeleton?.length ? (
          <span className="skel">
            {project.skeleton.map((r, i) => (
              <span key={r + i}>{i > 0 && <b>→</b>}{r}</span>
            ))}
          </span>
        ) : null}
        <span className="grow" />
        {err && <span className="err-inline">{err}</span>}
      </header>

      <div className="main">
        <Group>
          <Panel defaultSize={22} minSize={14}>
            <PageList shots={project?.shots || []} current={shot} onPick={(id) => { setShot(id); setTick(Date.now()); }} />
          </Panel>
          <Separator className="rz" />
          <Panel defaultSize={58} minSize={30}>
            <div className="colstack">
              <Preview project={project?.name || ""} tick={tick} />
            </div>
          </Panel>
          <Separator className="rz" />
          <Panel defaultSize={20} minSize={12}>
            <Jobs jobs={jobs} />
          </Panel>
        </Group>
      </div>

      <div className="bottom">
        <Chat project={project?.name || ""} onChanged={refresh} />
      </div>
    </div>
  );
}
