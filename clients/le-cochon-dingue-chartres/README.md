# Le Cochon Dingue — Chartres

Maquette commerciale V2 · DA "Velours & Pierre Froide" · Astro static site.

## Stack

- Astro 5 (static output)
- Tailwind CSS 3 (palette 5 couleurs : ink, cellar, bone, copper, neon)
- Typo : Instrument Serif (display, gratuit, remplace PP Editorial New payant) + Inter Tight (body) + IBM Plex Mono (microcopy)
- Sharp pour pipeline images (WebP optimisé)

## Démarrage

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # → dist/
npm run preview
```

## Photos

1. Déposer les photos brutes dans `photos-source/` selon les noms attendus par `scripts/prepare-images.mjs`
2. Lancer `npm run images` → génère les WebP optimisés dans `src/assets/images/`
3. Tant que les vraies photos ne sont pas en place, le site rend des **placeholders SVG** depuis `public/placeholders/`

## Polices

Chargées via Google Fonts CSS dans `BaseLayout.astro` (preconnect + display=swap). Self-host woff2 = optimisation future.

## Anti-jumeau MB Studio

Combo typo unique : Instrument Serif + Inter Tight + IBM Plex Mono. Aucun conflit avec Al Badea / Casa Tropical V2 / Casa Tropical V4 / Anamour.

## Déploiement

Cloudflare Pages, framework preset Astro, build `npm run build`, output `dist`, Node 20.
