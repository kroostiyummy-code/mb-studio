# Template `site-resto/`

Template MB Studio pour sites de restaurants. **Dupliqué dans un repo Git séparé pour chaque client** (jamais de mono-repo — voir principe non-négociable #7 dans le `CLAUDE.md` du repo MB Studio).

## Stack

- **Astro 5** (génération statique)
- **Decap CMS** (édition autonome par le patron via formulaire web)
- **Cloudflare Pages** (hébergement gratuit, build à chaque push)

## Architecture en 1 minute

### Les 12 sections du template

Chaque section est un composant `.astro` autonome dans `src/components/sections/`. Trois sont codées en vrai (Hero, Footer, StickyCallBar), les 9 autres sont des **stubs** à étoffer en phase 2.

| # | Composant | Statut |
|---|---|---|
| 1 | `Bandeau.astro` | stub (optionnel) |
| 2 | `Hero.astro` | ✅ codé |
| 3 | `Histoire.astro` | stub |
| 4 | `Avis.astro` | stub (conditionnel — note ≥ 4.0 ET avis ≥ 20) |
| 5 | `Reservation.astro` | stub |
| 6 | `Menu.astro` | stub |
| 7 | `Exigence.astro` | stub (optionnel) |
| 8 | `Galerie.astro` | stub (auto-hide si < 4 photos) |
| 9 | `Localisation.astro` | stub |
| 10 | `Reseaux.astro` | stub (optionnel) |
| 11 | `Footer.astro` | ✅ codé |
| 12 | `StickyCallBar.astro` | ✅ codé |

### Sections retirables au build, pas cachées CSS

`src/pages/index.astro` monte chaque section conditionnellement (`{settings.sections.X && <X />}`). Une section désactivée **n'apparaît PAS** dans le HTML final — pas de poids mort, la promesse "site < 1.5s" tient.

### Les 3 signatures typographiques MB Studio

Pilotées par `settings.signature` dans `src/content/settings/site.yml`. Chacune vit dans `src/styles/signatures/`, activée via la class `signature-{name}` sur `<body>` (pas d'import dynamique, pas de switch à l'exécution).

| Signature | Familles ciblées | Polices |
|---|---|---|
| `fast-food` | pizzeria, burger, foodtruck, brasserie urbaine | Archivo Black + Bebas Neue + Barlow Condensed |
| `gastro` | gastronomique, bistrot raffiné | Playfair Display + Inter |
| `traditionnel` | crêperie, bistrot familial, terroir | Bitter + Source Sans 3 |

Les polices Google sont chargées **conditionnellement dans le `<head>`** selon la signature active (pas de poids mort).

### Frontière Decap CMS / Frontmatter (à respecter)

Le patron ne touche JAMAIS au design.

| Quoi | Côté patron (Decap) | Côté Mike (frontmatter) |
|---|---|---|
| Dominante couleur | ✅ color picker | — |
| Accent | ❌ (figé selon signature) | ✅ `accent_override` possible |
| Signature typo | ❌ | ✅ choisie d'après brief |
| Neutres (crème/ardoise/noir) | ❌ | ❌ figés MB Studio |
| Contenu (textes, photos, menu, horaires) | ✅ tout éditable | — |

## Comment dupliquer pour un nouveau client

Cette procédure sera automatisée par le skill `new-client` quand il sera construit. En attendant, manuellement :

1. **Créer un nouveau repo GitHub** sous le compte MB Studio (ex: `cochon-dingue-site`)
2. `cp -r templates/site-resto/* /chemin/du/nouveau/repo/`
3. Dans le nouveau repo : `git init`, premier commit, push sur GitHub
4. Éditer `src/content/settings/site.yml` avec les infos brief du client :
   - `nom`, `slogan`, `ville`, `telephone`, `dominante`, etc.
   - `signature` = piochée d'après la question identité au brief (urbain/moderne / élégant/raffiné / tradition/familial)
5. Éditer `public/admin/config.yml` : remplacer `USER/REPO` par le vrai `mb-studio/cochon-dingue-site`
6. Uploader la photo hero dans `public/images/`
7. Connecter le repo à Cloudflare Pages → build & deploy automatique sur chaque push

## Développer en local

```bash
npm install
npm run dev    # http://localhost:4321
```

Pour tester l'édition Decap en local :

```bash
npx decap-server
# puis ouvrir http://localhost:4321/admin/
```

## Construire pour la prod

```bash
npm run build  # sortie dans dist/
npm run preview
```

## Cas zéro

Le template est livré pré-rempli avec les settings de **Kroostiyummy.fr** (le foodtruck de Mike, premier cas client MB Studio). Tu peux donc lancer `npm run dev` immédiatement et voir le rendu, puis remplacer les settings par ceux d'un vrai client.
