/// <reference types="vitest" />
import { defineConfig } from "vite";
import tailwindcss from "tailwindcss";
import atImport from "postcss-import";

export default defineConfig({
  root: "./client/",
  build: {
    outDir: "./dist",
    cssCodeSplit: true,
    rollupOptions: {
      input: ["./client/src/main.ts"],
      output: {
        entryFileNames: "bundle.js",
        assetFileNames: "bundle.css",
      },
    },
  },
  css: {
    postcss: {
      plugins: [atImport(), tailwindcss()],
    },
  },
  test: {
    environment: "happy-dom",
  },
});
