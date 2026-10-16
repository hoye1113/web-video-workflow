import { useState } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useDataStreamRuntime } from "@assistant-ui/react-data-stream";

/**
 * 最小验证：assistant-ui 接我们自己的后端（/api/chat，UI message stream 协议）。
 * 先不引 Thread 组件库（那要跑它的 CLI 生成），直接用运行时 + 自己搓最简列表，
 * 验的是「协议通不通、流式到不到、onData 能不能收到自定义部件」。
 */
export function App() {
  const [parts, setParts] = useState<string[]>([]);
  const [text, setText] = useState("");

  const runtime = useDataStreamRuntime({
    api: "/api/chat",
    body: { project: "marriage_full" },
    onData: (d) => {
      console.log("[onData]", d);
      setParts((p) => [...p, `${d.type}: ${JSON.stringify(d.data).slice(0, 80)}`]);
    },
    onError: (e) => console.error("[chat error]", e),
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div style={{ font: "14px/1.7 system-ui", padding: 16, maxWidth: 900 }}>
        <h3>assistant-ui × video-factory 验证</h3>
        <p style={{ color: "#666" }}>
          下面这个输入框是 assistant-ui 的运行时。发一句话，看后端流式回不回得来。
        </p>
        <div style={{ border: "1px solid #ddd", borderRadius: 8, height: 300, overflow: "auto", padding: 12, background: "#fafafa" }}>
          <ThreadView onText={setText} />
        </div>
        <div style={{ marginTop: 8 }}>
          <Composer />
        </div>
        <details style={{ marginTop: 12 }}>
          <summary>收到的自定义数据部件（onData）</summary>
          <pre style={{ fontSize: 12 }}>{parts.join("\n") || "（还没有）"}</pre>
        </details>
        <details>
          <summary>当前累积文本</summary>
          <pre style={{ fontSize: 12 }}>{text || "（空）"}</pre>
        </details>
      </div>
    </AssistantRuntimeProvider>
  );
}

// —— 下面两个是最简的线程渲染，用 assistant-ui 的 primitive ——
import { ThreadPrimitive, MessagePrimitive, ComposerPrimitive } from "@assistant-ui/react";

function ThreadView({ onText }: { onText: (t: string) => void }) {
  return (
    <ThreadPrimitive.Root>
      <ThreadPrimitive.Viewport>
        <ThreadPrimitive.Messages
          components={{
            UserMessage,
            AssistantMessage: (p) => <AssistantMessage {...p} onText={onText} />,
          }}
        />
      </ThreadPrimitive.Viewport>
    </ThreadPrimitive.Root>
  );
}

function UserMessage() {
  return (
    <div style={{ textAlign: "right", margin: "10px 0" }}>
      <span style={{ background: "#e8e8e8", padding: "6px 10px", borderRadius: 8, display: "inline-block" }}>
        <MessagePrimitive.Parts />
      </span>
    </div>
  );
}

function AssistantMessage({ onText }: any) {
  return (
    <div style={{ margin: "10px 0", whiteSpace: "pre-wrap" }}>
      <MessagePrimitive.Parts />
    </div>
  );
}

function Composer() {
  return (
    <ComposerPrimitive.Root style={{ display: "flex", gap: 8 }}>
      <ComposerPrimitive.Input
        placeholder="说点什么，比如：现在进展怎么样？"
        style={{ flex: 1, padding: "8px 10px", border: "1px solid #ccc", borderRadius: 8 }}
      />
      <ComposerPrimitive.Send
        style={{ padding: "8px 16px", borderRadius: 8, border: 0, background: "#C8553D", color: "#fff", cursor: "pointer" }}
      >
        发送
      </ComposerPrimitive.Send>
    </ComposerPrimitive.Root>
  );
}
