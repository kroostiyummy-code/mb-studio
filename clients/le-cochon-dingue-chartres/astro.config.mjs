import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://le-cochon-dingue-chartres.pages.dev',
  output: 'static',
  integrations: [tailwind(), sitemap()],
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto',
    assets: 'assets',
  },
  vite: {
    build: { cssMinify: 'lightningcss' },
  },
});
