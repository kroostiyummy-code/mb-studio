# Brief Anamour Lucé — maquette pré-porte-à-porte (v2 Dark Lounge)

> Ce dossier contient les **inputs prêts à plug** pour `site-from-brief` et l'**override design** Anamour, produits AVANT le porte-à-porte. Le brief client formel (skill `brief-client`) viendra après la visite chez le patron.

## Pivot v1 → v2 (2026-05-23)

La v1 a été produite avec la base ivoire standard MB Studio + accent cuivre. Mike a partagé un mockup AI externe avec DA **« Dark Mediterranean Grill Lounge »** (fond charbon, cuivre brillant, or doré, polices Syne+Hanken Grotesk, hero plein écran cinématique, menu en bento grid). Il l'a préféré.

**Convergence v2** : refonte de la maquette Astro pour adopter cette DA tout en restant fidèle à la stack MB Studio :
- **Pas de Tailwind CDN** → CSS scoped MB Studio (variables tokens overridées)
- **Pas d'appel Google Fonts au runtime** → Syne + Hanken Grotesk téléchargés en woff2 variables et auto-hébergés (`public/fonts/`)
- **Pas d'icônes Material Symbols externes** → SVG inline (déjà pattern du template)
- **Pas de classes Tailwind** → composants Astro propres, éditables Decap CMS

## Quoi est ici

### `content/` — inputs YAML pour `site-from-brief`

- `settings/site.yml` — fiche d'âme : partition VENIR + editorial + media 3, dominante `#ffb77b`, copywriting hero, histoire « Né du Feu » avec citation, horaires 7j/7 11h-00h30, avis 4,6★/319, photos moodboard AI temporaires
- `menu/sections/` — 4 sections menu (grillades, spécialités, mezzés, desserts) avec **prix indicatifs à confirmer au brief**
- `galerie/galerie.yml` — 6 placeholders Picsum (à remplacer par vraies photos après brief signé)

### `overrides/` — design Anamour (à appliquer par-dessus le template `site-resto/`)

- `styles/tokens.css` — palette dark complète (`--mb-paper: #131313`, `--mb-ink: #e5e2e1`, `--mb-secondary: #f0be76` or doré, `--mb-tertiary: #ffb3ad`), polices Syne+Hanken Grotesk en `--mb-display`/`--mb-sans`
- `styles/base.css` — @font-face Syne (variable 400-800) + Hanken Grotesk (variable 400-700) en plus du fallback Inter/Playfair
- `layouts/Layout.astro` — fontPreloads pointe sur les nouvelles polices variables
- `content.config.ts` — schéma `histoire` étendu (kicker, image, image_alt, quote)
- `components/sections/Hero.astro` — refonte plein écran 100vh, zoom slow 22s, scrim noir triple, kicker cuivre, h1 Syne 800, CTA pill cuivre + pill avis glass-card, arrow bounce
- `components/sections/Menu.astro` — refonte bento grid 4 cols desktop (section #1 = featured 2×2, dernière = wide 2×1, milieu = small 1×1), glass-cards warm sur fond paper-2, prix or doré
- `components/sections/Histoire.astro` — refonte 2 colonnes (texte + image), kicker, statement, body, blockquote citation encadrée accent, halo radial cuivre décoratif
- `components/sections/Footer.astro` — refonte dark `#0e0e0e`, brand Anamour cuivre + slogan or doré, mention signature MB Studio en footer-bottom
- `public/fonts/syne-var.woff2` + `hanken-grotesk-var.woff2` — polices auto-hébergées (~70Ko total, latin subset)

## Contexte stratégique

Voir [`prospects/anamour-luce/analyse-prebrief.md`](../../prospects/anamour-luce/analyse-prebrief.md) pour la lecture émotionnelle complète (6 dimensions), la DA recommandée, les photos cibles prioritaires, le spine commercial VENIR.

## Choix appliqués

| Dimension | Choix | Raison |
|---|---|---|
| Spine | `venir` | Le lieu physique est plus fort que le digital — il faut faire venir avant commander |
| Hero | `editorial` (100vh, zoom, scrim) | Statement émotionnel « L'âme anatolienne, l'esprit moderne. » |
| Tempo / densité | 2 / 2 | Lounge calme, équilibre photos+textes |
| Média | **3** | Intensité visuelle haute |
| Motion | **1** | Lounge calme — mouvement = feu + photos, pas animations |
| Dominante | `#ffb77b` cuivre clair brillant | Couleur métal de braise, glow nocturne |
| Or doré | `#f0be76` | Prix menu, highlights, accents secondaires |
| Display | Syne 800 variable | Anguleux moderne, lounge — différencie d'autres clients MB Studio |
| Body | Hanken Grotesk variable | Humaniste moderne |
| Sections actives | histoire, avis, menu, galerie, localisation, reseaux | Pas de bandeau (hero plein écran porte l'identité), pas de réservation (pas de système réservation), pas d'exigence |

## À reprendre au brief signé

- [ ] Prix réels du menu (les actuels sont indicatifs cohérents avec « 10-20 € »)
- [ ] Année de création (`est_year`)
- [ ] Géo précis (`geo.lat/lng` actuels = estimation)
- [ ] URL Google avis (`google_avis_url`)
- [ ] Réseaux complémentaires (Facebook, TikTok ?)
- [ ] **Vraies photos** à uploader (cf moodboard à générer en avance, photos cibles listées dans analyse-prebrief.md)
- [ ] Confirmation du copywriting hero, histoire, citation
- [ ] Year d'EST. dans le footer si patron veut le mentionner

## Suite

1. **Maquette à montrer** : ZIP livré, contient `dist/` Astro buildé. Décompresser → ouvrir `index.html`. Photos = URLs Aida temporaires (peuvent expirer) + Picsum aléatoires pour galerie.
2. **Optionnel avant porte-à-porte** : générer un moodboard photo dédié (`methode-emotionnelle.md` → moodboard IA obligatoire) avec les photos cibles de `analyse-prebrief.md` — à imprimer pour la visite.
3. **Porte-à-porte** : tablette + maquette HTML + moodboard imprimé.
4. **Si signe** → vrai brief-client (12 sujets), puis `site-from-brief` qui consommera ces inputs + overrides + ceux du brief signé.
