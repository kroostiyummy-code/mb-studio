/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: '#111111',
        cellar: '#2B1F1A',
        bone: '#F5EFE7',
        copper: '#B06A42',
        neon: '#E85D8E',
      },
      fontFamily: {
        display: ['"Instrument Serif"', 'Georgia', 'serif'],
        body: ['"Inter Tight"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      letterSpacing: {
        kicker: '0.18em',
        tight: '-0.02em',
        display: '-0.025em',
      },
      lineHeight: {
        display: '1.05',
        body: '1.7',
      },
      spacing: {
        section: '8rem',
        'section-lg': '12rem',
      },
      maxWidth: {
        reading: '38rem',
      },
    },
  },
  plugins: [],
};
