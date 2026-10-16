/** 跟后端的接口。后端在 app/server.py，代理见 vite.config.ts。 */

export type Shot = {
  id: string;
  role?: string;
  title?: string;
  note?: string;
  narration?: string;
  dur: number;
  camera?: string;
  text?: string;
  status?: string;
  hasScene?: boolean;
  stale?: boolean;
  sceneHash?: string;
  /** 逐页路由：这一页的画面走哪条做法 */
  mode?: "image" | "code" | "mixed";
  /** mode=image/mixed 时，给生图模型的描述 */
  imagePrompt?: string;
  /** 生图产出的图（有就是已经生过了） */
  images?: string[];
};

export type Project = {
  name: string;
  title: string;
  style?: { preset?: string; name?: string; look?: string; palette?: string[]; hint?: string };
  skeleton?: string[];
  filmType?: string;
  shots: Shot[];
  approved?: boolean;
  fps?: number;
};

export type Job = {
  id: string;
  kind: string;
  title: string;
  status: "queued" | "running" | "done" | "failed";
  progress: number;
  frames: [number, number];
  elapsed: number;
  error?: string;
  log: string[];
  out?: string;
};

async function req<T>(path: string, opt: { method?: string; body?: unknown } = {}): Promise<T> {
  const r = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    method: opt.method,
    body: opt.body ? JSON.stringify(opt.body) : undefined,
  });
  const t = await r.text();
  let d: any = null;
  try { d = t ? JSON.parse(t) : null; } catch { d = { raw: t }; }
  if (!r.ok) throw new Error(d?.error || `HTTP ${r.status}`);
  return d as T;
}

export const api = {
  projects: () => req<{ name: string; title: string; shots: number; rendered: number }[]>("/api/projects"),
  project: (name: string) => req<Project>(`/api/projects/${name}`),
  presets: () => req<{ id: string; name: string; hint: string; swatch: string[] }[]>("/api/presets"),
  jobs: () => req<Job[]>("/api/jobs"),

  // 下面是"动作"，聊天里模型说要做什么，前端就来调这些
  writeScene: (project: string, shot: string) =>
    req<Job>("/api/scene", { method: "POST", body: { project, shot } }),
  renderShot: (project: string, shot: string) =>
    req<Job>("/api/render", { method: "POST", body: { project, shot } }),
  stills: (project: string, shot: string) =>
    req<Job>("/api/stills", { method: "POST", body: { project, shot } }),
  review: (project: string, shot: string) =>
    req<Job>("/api/review", { method: "POST", body: { project, shot } }),
  genImages: (project: string, shots?: string[]) =>
    req<Job>("/api/images", { method: "POST", body: { project, shots } }),
  genScenes: (project: string, shots?: string[]) =>
    req<Job>("/api/scenes", { method: "POST", body: { project, shots } }),
  imageAudit: (project: string, shots?: string[], regen = true) =>
    req<Job>("/api/image_audit", { method: "POST", body: { project, shots, regen } }),
  director: (project: string, shot: string, rounds = 3) =>
    req<Job>("/api/director", { method: "POST", body: { project, shot, rounds } }),
  concat: (project: string, name = "成片.mp4") =>
    req<Job>("/api/concat", { method: "POST", body: { project, name } }),
  exportFilm: (project: string) =>
    req<Job>("/api/film", { method: "POST", body: { project, name: "成片.mp4" } }),
};

/** 执行一条模型给的动作。返回一句人话的结果，聊天里可以回显。 */
export async function runAction(project: string, a: { op: string; shot?: string; shots?: string[] }): Promise<string> {
  const s = a.shot || "";
  switch (a.op) {
    case "write_scene":  await api.writeScene(project, s);  return `开始写第 ${s} 页的代码`;
    case "render_shot":  await api.renderShot(project, s);  return `开始渲第 ${s} 页`;
    case "review_shot":  { await api.stills(project, s); await api.review(project, s); return `抽帧并评审第 ${s} 页`; }
    case "gen_images":   {
      const shots = a.shots?.length ? a.shots : (s ? [s] : undefined);
      await api.genImages(project, shots);
      return shots ? `去生第 ${shots.join("、")} 页的图` : "去把缺的图都生出来";
    }
    case "write_scenes": {
      const shots = a.shots?.length ? a.shots : (s ? [s] : undefined);
      await api.genScenes(project, shots);
      return shots ? `开始写第 ${shots.join("、")} 页的代码` : "开始写还没写的页";
    }
    case "image_audit":  await api.imageAudit(project);  return "开始体检生成的图（构图不合格的会重画）";
    case "render_film":  await api.exportFilm(project);     return "开始出整片";
    case "list_pages":   return "（刷新页面列表）";
    default:             return `不认识的操作：${a.op}`;
  }
}
