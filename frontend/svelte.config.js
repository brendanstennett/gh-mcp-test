import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter(),
    // Don't use aliases during production builds
    ...(process.env.NODE_ENV !== 'production' && {
      alias: {
        '@express-svelte/validation': '../validation/index.ts',
        '@express-svelte/errors': '../errors/index.ts',
        '@express-svelte/shared': '../shared/index.ts',
      },
    }),
  },
};

export default config;
