/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#1A1209',
        surface: '#1A1209',
        'surface-low': '#231A11',
        'surface-lowest': '#150C05',
        'surface-container': '#271E15',
        'surface-high': '#32281F',
        'surface-bright': '#42372D',
        cream: '#F2DFD1',
        'cream-variant': '#DDC1B6',
        terracotta: '#E07140',
        'terracotta-bright': '#FFB598',
        'cuivre-brule': '#B8763D',
        'tomate-profond': '#8B2F2F',
        'olive-discret': '#556B3E',
        outline: '#A58B82',
        'outline-variant': '#56423A',
      },
      fontFamily: {
        serif: ['"Bodoni Moda"', 'Georgia', 'serif'],
        sans: ['"Be Vietnam Pro"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        'display-lg': [
          'clamp(40px, 7vw, 72px)',
          { lineHeight: '1.05', letterSpacing: '-0.02em', fontWeight: '600' },
        ],
        'headline-lg': [
          'clamp(32px, 5vw, 48px)',
          { lineHeight: '1.15', fontWeight: '500' },
        ],
        'headline-md': [
          'clamp(24px, 3.5vw, 32px)',
          { lineHeight: '1.2', fontWeight: '500' },
        ],
        'body-lg': ['18px', { lineHeight: '1.6', fontWeight: '400' }],
        'body-md': ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        caps: [
          '12px',
          { lineHeight: '1.2', letterSpacing: '0.2em', fontWeight: '600' },
        ],
        'caps-sm': [
          '10px',
          { lineHeight: '1.2', letterSpacing: '0.3em', fontWeight: '600' },
        ],
      },
      borderRadius: {
        DEFAULT: '0.25rem',
        sm: '0.125rem',
        lg: '0.5rem',
      },
      spacing: {
        section: 'clamp(80px, 12vw, 160px)',
      },
      transitionTimingFunction: {
        'soft-out': 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
  plugins: [],
};
