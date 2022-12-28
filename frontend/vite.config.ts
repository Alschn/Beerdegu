/// <reference types="vitest" />
import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import type {UserConfig as VitestUserConfigInterface} from 'vitest/config';

const vitestConfig: VitestUserConfigInterface = {
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    css: false,
    coverage: {
      provider: 'c8',
      reporter: ['html', 'lcov', 'text'],
      src: ['src'],
      exclude: [
        '**/src/setupTests.ts',
        '**/src/mocks/**',
        '**/src/tests/**',
        '**/src/config/**',
        '**/src/vite-env.d.ts',
      ],
      all: true,
    }
  }
};

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
  },
  build: {
    outDir: 'build',
  },
  test: vitestConfig.test,
});
