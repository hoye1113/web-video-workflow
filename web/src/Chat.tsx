import { AssistantRuntimeProvider, ComposerPrimitive, MessagePrimitive, ThreadPrimitive } from "@assistant-ui/react";
import { useDataStreamRuntime } from "@assistant-ui/react-data-stream";
import { useEffect, useRef, useState } from "react";
import { runAction } from "./api";

/**
 * 聊天：唯一的操作入口。
 *
 * 后端（/api/chat）按 Vercel AI SDK 的 UI message stream 协议吐字。
 * 模型回话时会顺带输出一个 JSON，后端把它变成 `data-actions` 自定义部件；
 * 这里在 onData 里收到就执行对应动作 —— 这就是"聊天驱动面板"的全部机制。
 */
export function Chat({ project, onChanged }: { project: string; onChanged: () => void }) {
  const [notes, setNotes] = useState<string[]>([]);
  const busy = useRef(false);

  const runtime = useDataStreamRuntime({
    api: "/api/chat",
    body: { project },
    onData: async (d: any) => {
      if (d?.type !== "data-actions") return;
      const acts = d.data?.actions || [];
      for (const a of acts) {
        setNotes((n) => [...n, `▸ ${a.op}${a.shot ? " " + a.shot : ""}`]);
        try {
          const msg = await runAction(project, a);
          setNotes((n) => [...n, `  ${msg}`]);
        } catch (e: any) {
          setNotes((n) => [...n, `  ✗ ${e.message}`]);
        }
      }
      if (acts.length) { busy.current = true; onChanged(); }
    },
    onError: (e) => setNotes((n) => [...n, `✗ ${String(e)}`]),
  });

  // 有动作在跑的时候，隔一会儿刷新一次面板（A3 会改成 SSE 推送）
  useEffect(() => {
    if (!busy.current) return;
    const t = setInterval(onChanged, 2500);
    return () => clearInterval(t);
  }, [notes.length, onChanged]);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="chat">
        <div className="chat-log">
          <ThreadPrimitive.Root>
            <ThreadPrimitive.Viewport>
              <ThreadPrimitive.Messages components={{ UserMessage, AssistantMessage }} />
              <ThreadPrimitive.Empty>
                <p className="muted">
                  在下面说话就行 —— 比如「现在到哪了」「写第 04 页」「这页裂缝太粗」「把整片出了」。
                  不用点按钮。
                </p>
              </ThreadPrimitive.Empty>
            </ThreadPrimitive.Viewport>
          </ThreadPrimitive.Root>
          {notes.length > 0 && (
            <details className="notes">
              <summary>刚才做了什么（{notes.length}）</summary>
              <pre>{notes.join("\n")}</pre>
            </details>
          )}
        </div>
        <ComposerPrimitive.Root className="composer">
          <ComposerPrimitive.Input className="composer-input" placeholder="说你想改什么…" />
          <ComposerPrimitive.Send className="composer-send">发送</ComposerPrimitive.Send>
        </ComposerPrimitive.Root>
      </div>
    </AssistantRuntimeProvider>
  );
}

function UserMessage() {
  return (
    <div className="msg user">
      <span><MessagePrimitive.Parts /></span>
    </div>
  );
}

function AssistantMessage() {
  return (
    <div className="msg bot">
      <MessagePrimitive.Parts />
    </div>
  );
}
