import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 后端是 python app/server.py（8777）。聊天是 SSE，要关掉代理的缓冲。
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5199,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8777",
        changeOrigin: true,
        // SSE 必须不缓冲，否则字要等整段才好
        configure: (proxy) => {
          proxy.on("proxyRes", (proxyRes) => {
            proxyRes.headers["cache-control"] = "no-cache, no-transform";
          });
        },
      },
      "/engine": { target: "http://127.0.0.1:8777", changeOrigin: true },
      "/work": { target: "http://127.0.0.1:8777", changeOrigin: true },
    },
  },
});
