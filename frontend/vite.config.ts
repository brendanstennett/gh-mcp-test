import devtoolsJson from 'vite-plugin-devtools-json';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy:
      process.env.NODE_ENV === 'development'
        ? {
            '/api': {
              target: 'http://localhost:8000',
              changeOrigin: true,
            },
            '/auth': {
              target: 'http://localhost:8000',
              changeOrigin: true,
            },
          }
        : undefined,
  },
  plugins: [sveltekit(), devtoolsJson()],
  test: {
    projects: [
      {
        extends: './vite.config.ts',
        test: {
          name: 'client',
          environment: 'browser',
          browser: {
            enabled: true,
            provider: 'playwright',
            headless: true,
            instances: [{ browser: 'chromium' }],
          },
          include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
          exclude: ['src/lib/server/**'],
          setupFiles: ['./vitest-setup-client.ts'],
        },
      },
      {
        extends: './vite.config.ts',
        test: {
          name: 'server',
          environment: 'node',
          include: ['src/**/*.{test,spec}.{js,ts}'],
          exclude: ['src/**/*.svelte.{test,spec}.{js,ts}'],
        },
      },
    ],
  },
});
