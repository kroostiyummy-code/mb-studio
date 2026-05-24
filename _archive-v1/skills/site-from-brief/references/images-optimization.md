# Optimisation des photos client

Règles d'optimisation pour les photos transférées par le patron au brief, avant injection dans `clients/{slug}/public/images/`. Le poids des images est le n°1 facteur de PageSpeed sur un site resto.

---

## Cibles techniques

| Métrique | Cible |
|---|---|
| Largeur maximale | **1600 px** (suffisant pour un écran retina 1440px de large) |
| Format préféré | **WebP** (compression supérieure à JPEG) |
| Format fallback | **JPEG** (compatibilité universelle) |
| Qualité de compression | **85%** (compromis qualité/poids) |
| Poids cible par photo | **< 200 Ko** après optimisation |
| Poids absolu max | **400 Ko** (si l'image est très détaillée et qu'on refuse de descendre en qualité) |

---

## Procédure d'optimisation

### Outils disponibles sur Windows (Mike)

Le plus simple : **Sharp.js** intégré au build Astro via le package `@astrojs/image` (déjà inclus dans Astro 5 par défaut).

Sinon, en CLI :

```powershell
# Avec ImageMagick (si installé) :
magick input.jpg -resize 1600x -quality 85 output.webp

# Avec FFmpeg (souvent déjà installé) :
ffmpeg -i input.jpg -vf "scale=1600:-1" -q:v 4 output.webp
```

Si Mike n'a aucun des deux installés : utiliser une lib Node.js dans le skill via `npm install sharp` localement.

### Procédure Node.js (recommandée pour le skill)

```javascript
const sharp = require('sharp');

await sharp('briefs/le-saint-hilaire/photos/plat-signature.jpg')
  .resize({ width: 1600, withoutEnlargement: true })
  .webp({ quality: 85 })
  .toFile('clients/le-saint-hilaire/public/images/plat-signature.webp');
```

### Vérification après optimisation

Après chaque photo optimisée, vérifier :

1. **Taille du fichier** : doit être < 200 Ko (logger un warning si entre 200 et 400 Ko, erreur si > 400 Ko)
2. **Dimensions** : largeur ≤ 1600 px
3. **Le format final** : `.webp` ou `.jpg` selon le fallback choisi
4. **Le nom de fichier** : kebab-case sans accents, sans espaces (`plat-signature.webp`, pas `Plat Signature.WEBP`)

---

## Conventions de nommage

Fichiers à produire dans `clients/{slug}/public/images/` :

| Usage | Nom du fichier |
|---|---|
| Photo hero (la plus forte) | `hero.webp` (ou `hero.jpg` si fallback) |
| Photos de galerie | `galerie-01.webp`, `galerie-02.webp`, etc. (zero-padding sur 2 chiffres) |
| Logo du resto | `logo.svg` si fourni en vectoriel, sinon `logo.webp` |
| Favicon | `favicon.svg` si fourni en vectoriel, sinon `favicon.png` (32×32 ou 64×64) |
| Photo Open Graph (partage social) | `og.webp` ou `og.jpg` (1200×630 px exactement) |

---

## Cas particuliers

### Photo très haute résolution (4000+ px de large)

- Cas typique : le patron a pris la photo avec son téléphone, format original 4000×3000
- Action : redimensionner à 1600px de large, pas plus
- **Conserver l'original** dans `briefs/{slug}/photos/originals/` au cas où Mike veut une version print plus tard

### Photo en format HEIC (iPhone récent)

- HEIC n'est pas supporté nativement par tous les navigateurs
- Action : **convertir obligatoirement** en WebP ou JPEG
- Avec Sharp : `sharp(input).webp({ quality: 85 })` accepte HEIC en entrée

### Photo trop sombre / trop claire / floue

- **Ne pas tenter de corriger automatiquement** (les outils auto donnent souvent un rendu pire)
- Demander à Mike : "La photo X est sombre. Tu veux que je la garde, que je l'enlève, ou tu peux en demander une autre au patron ?"

### Photo avec watermark visible (souvent sur Instagram)

- Cas typique : le patron a téléchargé sa propre photo Insta avec le logo Insta superposé
- Action : **ne pas l'utiliser** (qualité médiocre + droit d'image discutable)
- Demander la photo originale au patron via SMS

### Plus de 12 photos dans la galerie

- 12 photos = limite haute pour ne pas plomber le poids de page
- Si le patron en a 20 : sélectionner les 12 plus fortes (logique de tri : plat signature > salle > terrasse > équipe > divers)
- Garder les autres dans `briefs/{slug}/photos/extra/` au cas où

---

## Validation finale

Avant de marquer l'étape "images" comme terminée, vérifier :

- [ ] **Toutes les photos** mentionnées dans le brief.md sont présentes dans `clients/{slug}/public/images/`
- [ ] **Aucune photo > 400 Ko** dans le dossier final
- [ ] **Hero photo** présente et bien nommée `hero.webp`
- [ ] **Galerie** : si ≥ 4 photos, `sections.galerie: true` dans settings ; sinon `false`
- [ ] **OG image** (`og.webp` ou `og.jpg`) présente — utilisée pour le partage Facebook/WhatsApp. **Critique pour le SEO social**.

---

## Notes pour le futur

- **Skill `image-helper`** à construire plus tard si les optimisations deviennent répétitives : `/image-helper {photo_path}` → auto-resize, auto-format, génération OG image à partir de la photo hero, etc.
- **Pack Pro 120€/mois** (à introduire après 6e client) inclura un tournage photo professionnel mensuel — résoudra définitivement le problème de qualité photo.
