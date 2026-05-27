// prepare-images.mjs
// Transforme les photos sources brutes (images-source/) en WebP optimisés (public/images/).
// Spec fusionnée du brief principal (Section 3) + patch four personnalisé (Section "Mise à jour prepare-images.mjs").
//
// Usage :
//   node prepare-images.mjs                    → traite les vraies sources si présentes, sinon génère des placeholders pour les manquantes.
//   node prepare-images.mjs --placeholders     → force la génération de placeholders pour TOUTES les entrées (utile build sans sources).
//   node prepare-images.mjs --strict           → échoue si une source manque (mode CI Mike avec banque complète).

import sharp from 'sharp';
import { mkdir, stat, access } from 'node:fs/promises';
import { constants } from 'node:fs';
import path from 'node:path';

const SRC = './images-source';
const DST = './public/images';

const args = new Set(process.argv.slice(2));
const FORCE_PLACEHOLDERS = args.has('--placeholders');
const STRICT = args.has('--strict');

// Palette pour placeholders (cohérente avec la palette tailwind du site)
const PALETTE = {
  espresso: { r: 26, g: 18, b: 9 },         // #1A1209 background
  espressoDeep: { r: 21, g: 12, b: 5 },     // #150C05 surface-lowest
  surfaceContainer: { r: 39, g: 30, b: 21 },// #271E15
  terracotta: { r: 224, g: 113, b: 64 },    // #E07140
  terracottaDark: { r: 139, g: 47, b: 47 }, // #8B2F2F tomate-profond
  cuivre: { r: 184, g: 118, b: 61 },        // #B8763D
  cream: { r: 242, g: 223, b: 209 },        // #F2DFD1
};

const PHOTOS = [
  // ───────────────────── HERO (patch four personnalisé) ─────────────────────
  {
    src: 'four-piacere-mosaique-source.jpg',
    dst: 'hero-four-piacere.webp',
    width: 1600,
    height: 1067,
    quality: 80,
    budgetKB: 220,
    usage: 'hero desktop (eager + fetchpriority high) — inscription IL PIACERE mosaïque bleue visible',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracotta,
  },
  {
    src: 'four-piacere-mosaique-source.jpg',
    dst: 'hero-four-piacere-mobile.webp',
    width: 800,
    height: 1000,
    quality: 80,
    budgetKB: 140,
    usage: 'hero mobile <picture srcset> — cadrage portrait inscription centrée',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracotta,
  },

  // ───────────────────── LE FEU (patch) ─────────────────────
  {
    src: 'four-piacere-mosaique-source.jpg',
    dst: 'feu-four-complet.webp',
    width: 1920,
    height: 1280,
    quality: 82,
    budgetKB: 260,
    usage: 'LE FEU full-bleed (lazy) — cadrage large four + comptoir inox + reflet IL PIACERE',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracotta,
  },
  {
    src: 'four-flammes-bois-source.jpg',
    dst: 'feu-flammes-bois.webp',
    width: 900,
    height: 1125,
    quality: 78,
    budgetKB: 120,
    usage: 'triple composition #1 — flammes orange sur bûches alignées',
    placeholderColor: PALETTE.surfaceContainer,
    placeholderAccent: PALETTE.terracotta,
  },
  {
    src: 'pate-pizza-source.jpg',
    dst: 'feu-pate-gros-plan.webp',
    width: 800,
    height: 800,
    quality: 78,
    budgetKB: 100,
    usage: 'triple composition #2 — texture micro pâte crue',
    placeholderColor: PALETTE.cream,
    placeholderAccent: PALETTE.cuivre,
  },
  {
    src: 'flammes-orange-fond-noir-source.jpg',
    dst: 'feu-flammes-noires.webp',
    width: 800,
    height: 1000,
    quality: 78,
    budgetKB: 110,
    usage: 'triple composition #3 — flammes vives fond noir',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracottaDark,
  },

  // ───────────────────── TRIPTYQUE ─────────────────────
  {
    src: 'cocktail-spritz-comptoir-source.jpg',
    dst: 'triptyque-boire.webp',
    width: 600,
    height: 750,
    quality: 75,
    budgetKB: 90,
    usage: 'triptyque BOIRE (lazy) — verre spritz au comptoir',
    placeholderColor: PALETTE.surfaceContainer,
    placeholderAccent: PALETTE.terracotta,
  },
  {
    src: 'pizza-burrata-jambon-source.jpg',
    dst: 'triptyque-manger.webp',
    width: 800,
    height: 600,
    quality: 75,
    budgetKB: 100,
    usage: 'triptyque MANGER (lazy) — pizza burrata jambon Parme vue de biais',
    placeholderColor: PALETTE.espresso,
    placeholderAccent: PALETTE.cream,
  },
  {
    src: 'terrasse-soir-tables-source.jpg',
    dst: 'triptyque-samuser.webp',
    width: 700,
    height: 700,
    quality: 75,
    budgetKB: 95,
    usage: 'triptyque S\'AMUSER (lazy) — tables occupées au soir',
    placeholderColor: PALETTE.espresso,
    placeholderAccent: PALETTE.cuivre,
  },

  // ───────────────────── LA TABLE ─────────────────────
  {
    src: 'salle-banquettes-cuir-source.jpg',
    dst: 'table-salle-soir.webp',
    width: 1400,
    height: 933,
    quality: 78,
    budgetKB: 180,
    usage: 'LA TABLE 65% width (lazy) — salle banquettes cuir lumière chaude',
    placeholderColor: PALETTE.surfaceContainer,
    placeholderAccent: PALETTE.cuivre,
  },

  // ───────────────────── LE COMPTOIR ─────────────────────
  {
    src: 'bar-comptoir-bouteilles-source.jpg',
    dst: 'comptoir.webp',
    width: 1200,
    height: 800,
    quality: 78,
    budgetKB: 160,
    usage: 'LE COMPTOIR 60% width (lazy) — bouteilles étagère lumière chaude',
    placeholderColor: PALETTE.surfaceContainer,
    placeholderAccent: PALETTE.terracotta,
  },

  // ───────────────────── LA CAVE ─────────────────────
  {
    src: 'bouteilles-vin-lampes-source.jpg',
    dst: 'cave-bouteilles.webp',
    width: 900,
    height: 1125,
    quality: 78,
    budgetKB: 130,
    usage: 'LA CAVE col gauche (lazy) — bouteilles vin rouge + lampes orange',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracottaDark,
  },

  // ───────────────────── POUR LES GROUPES (patch) ─────────────────────
  {
    src: 'terrasse-treillis-tables-source.jpg',
    dst: 'groupes-terrasse.webp',
    width: 1920,
    height: 1080,
    quality: 80,
    budgetKB: 240,
    usage: 'POUR LES GROUPES full-bleed (lazy) — terrasse jour treillis perspective tables',
    placeholderColor: PALETTE.cuivre,
    placeholderAccent: PALETTE.cream,
  },

  // ───────────────────── OG IMAGE ─────────────────────
  {
    src: 'four-piacere-mosaique-source.jpg',
    dst: 'og-image.webp',
    width: 1200,
    height: 630,
    quality: 82,
    budgetKB: 180,
    usage: 'Open Graph + Twitter Card — same four signature',
    placeholderColor: PALETTE.espressoDeep,
    placeholderAccent: PALETTE.terracotta,
  },
];

async function fileExists(p) {
  try {
    await access(p, constants.R_OK);
    return true;
  } catch {
    return false;
  }
}

function makePlaceholderSvg(photo) {
  const { width, height, dst, placeholderColor: c, placeholderAccent: a } = photo;
  const cHex = `rgb(${c.r},${c.g},${c.b})`;
  const aHex = `rgb(${a.r},${a.g},${a.b})`;
  const label = dst.replace('.webp', '').toUpperCase();
  const fontSize = Math.round(Math.min(width, height) / 22);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <radialGradient id="g" cx="50%" cy="50%" r="70%">
        <stop offset="0%" stop-color="${aHex}" stop-opacity="0.15"/>
        <stop offset="100%" stop-color="${cHex}" stop-opacity="1"/>
      </radialGradient>
      <pattern id="grain" x="0" y="0" width="3" height="3" patternUnits="userSpaceOnUse">
        <rect width="3" height="3" fill="${cHex}"/>
        <rect width="1" height="1" fill="${aHex}" opacity="0.05"/>
      </pattern>
    </defs>
    <rect width="${width}" height="${height}" fill="${cHex}"/>
    <rect width="${width}" height="${height}" fill="url(#g)"/>
    <rect width="${width}" height="${height}" fill="url(#grain)" opacity="0.4"/>
    <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central"
      font-family="IBM Plex Mono, ui-monospace, monospace"
      font-size="${fontSize}" font-weight="500"
      fill="${aHex}" opacity="0.85"
      letter-spacing="${Math.round(fontSize * 0.2)}">
      ${label}
    </text>
    <text x="50%" y="${height - Math.round(height * 0.06)}" text-anchor="middle"
      font-family="IBM Plex Mono, ui-monospace, monospace"
      font-size="${Math.round(fontSize * 0.6)}"
      fill="${aHex}" opacity="0.5">
      PLACEHOLDER · MIKE À REMPLACER
    </text>
  </svg>`;
}

async function processOne(photo) {
  const srcPath = path.join(SRC, photo.src);
  const dstPath = path.join(DST, photo.dst);

  const hasSource = !FORCE_PLACEHOLDERS && (await fileExists(srcPath));

  if (!hasSource && STRICT) {
    throw new Error(`Source manquante (strict mode) : ${srcPath}`);
  }

  try {
    if (hasSource) {
      await sharp(srcPath)
        .resize(photo.width, photo.height, { fit: 'cover', position: 'center' })
        .webp({ quality: photo.quality, effort: 6 })
        .toFile(dstPath);
    } else {
      const svg = Buffer.from(makePlaceholderSvg(photo));
      await sharp(svg)
        .webp({ quality: photo.quality, effort: 6 })
        .toFile(dstPath);
    }

    const { size } = await stat(dstPath);
    const kb = Math.round(size / 1024);
    const within = kb <= photo.budgetKB;
    const status = within ? '✅' : '⚠️';
    const tag = hasSource ? '[SOURCE]' : '[PLACEHOLDER]';
    console.log(`${status} ${tag} ${photo.dst} → ${kb} KB (budget ${photo.budgetKB} KB) — ${photo.usage}`);
    return { ok: true, within, hasSource };
  } catch (err) {
    console.error(`❌ ${photo.src} → ${photo.dst} : ${err.message}`);
    return { ok: false, within: false, hasSource };
  }
}

async function run() {
  await mkdir(SRC, { recursive: true });
  await mkdir(DST, { recursive: true });

  console.log('\n=== prepare-images.mjs — Il Piacere Luisant ===');
  console.log(`Mode : ${FORCE_PLACEHOLDERS ? 'PLACEHOLDERS forcés' : STRICT ? 'STRICT (sources requises)' : 'AUTO (placeholder si source manquante)'}\n`);

  let ok = 0;
  let placeholders = 0;
  let overBudget = 0;
  let failed = 0;
  let totalKB = 0;

  for (const photo of PHOTOS) {
    const res = await processOne(photo);
    if (res.ok) {
      ok += 1;
      if (!res.hasSource) placeholders += 1;
      if (!res.within) overBudget += 1;
      try {
        const { size } = await stat(path.join(DST, photo.dst));
        totalKB += Math.round(size / 1024);
      } catch {}
    } else {
      failed += 1;
    }
  }

  console.log('\n--- Résumé ---');
  console.log(`Traités : ${ok}/${PHOTOS.length}`);
  console.log(`Placeholders : ${placeholders}`);
  console.log(`Hors budget : ${overBudget}`);
  console.log(`Échecs : ${failed}`);
  console.log(`Total public/images : ${totalKB} KB (budget global 1400 KB)`);

  if (failed > 0) process.exit(1);
}

run();
