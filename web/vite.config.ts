import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 后端是 python app/server.py（8777）。
// /api 里有 SSE 长连接（聊天、任务进度），代理必须关掉缓冲，否则字要等整段。
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5199,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8777",
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on("proxyRes", (proxyRes) => {
            if ((proxyRes.headers["content-type"] || "").includes("event-stream")) {
              proxyRes.headers["cache-control"] = "no-cache, no-transform";
              proxyRes.headers["x-accel-buffering"] = "no";
            }
          });
        },
      },
      "/engine": { target: "http://127.0.0.1:8777", changeOrigin: true },
      "/work": { target: "http://127.0.0.1:8777", changeOrigin: true },
    },
  },
});
