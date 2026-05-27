# Il Piacere — Luisant

Site Astro statique pour le restaurant Il Piacere (Luisant, 28600).
Maquette commerciale MB Studio v1, dérivée du brief Agent 4 V2 + patch four personnalisé.

## Stack

- Astro 5 (output static)
- Tailwind CSS 3 (config palette dédiée Il Piacere)
- Sharp (transformation WebP au build)
- Sitemap auto

## Commandes

```bash
npm install                      # dépendances
node prepare-images.mjs          # WebP depuis images-source/ (placeholders si absents)
node prepare-images.mjs --placeholders   # force placeholders pour tout
npm run build                    # build statique → dist/
npm run preview                  # serveur local du build
npm run dev                      # serveur dev
```

## Photos source (Mike)

Déposer les sources brutes dans `images-source/` (gitignored) avec les noms exacts
listés dans `prepare-images.mjs`. La photo signature `four-piacere-mosaique-source.jpg`
doit être cadrée pour que l'inscription "IL PIACERE" en mosaïque bleue reste lisible
en mobile 375px.

Tant que les sources ne sont pas déposées, des placeholders WebP unicolores typés
(palette du site) sont générés automatiquement pour permettre le build.

## Conformité brief

- Polices : Bodoni Moda + Be Vietnam Pro + IBM Plex Mono (Google Fonts OFL, gratuit)
- Schema.org Restaurant complet
- Aucun framework JS lourd, scroll natif
- prefers-reduced-motion respecté
- Footer 2026 + crédit MB Studio
