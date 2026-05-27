/**
 * Pipeline images sharp pour Le Cochon Dingue.
 *
 * Usage :
 *   1. Dépose tes photos brutes dans ./photos-source/ avec les noms ci-dessous (clé `src`)
 *   2. npm run images
 *   3. Les WebP optimisés apparaissent dans ./src/assets/images/ (clé `dst`)
 *
 * Une fois les vrais fichiers présents, swappe les <img src="/placeholders/..."> par
 * <Image src={import('../assets/images/...webp')} ... /> dans les composants .astro.
 */
import sharp from 'sharp';
import fs from 'node:fs/promises';
import path from 'node:path';

const SRC_DIR = './photos-source';
const DST_DIR = './public/assets/images';

const PIPELINE = [
  { src: 'facade-nuit-original.jpg', dst: 'hero-devanture.webp',
    w: 1920, h: 1280, quality: 78, budget: 180, usage: 'hero · eager · fetchpriority high' },
  { src: 'facade-nuit-original.jpg', dst: 'hero-devanture-mobile.webp',
    w: 800, h: 1067, quality: 75, budget: 110, usage: 'hero mobile · eager' },

  { src: 'gm-2023-original.png', dst: 'gm-2023.webp',
    w: 320, h: 320, quality: 85, budget: 40, usage: 'lazy' },
  { src: 'gm-2024-original.png', dst: 'gm-2024.webp',
    w: 320, h: 320, quality: 85, budget: 40, usage: 'lazy' },
  { src: 'gm-2025-original.png', dst: 'gm-2025.webp',
    w: 320, h: 320, quality: 85, budget: 40, usage: 'lazy' },

  { src: 'comptoir-interieur-original.jpg', dst: 'boutique-interieur.webp',
    w: 1200, h: 1600, quality: 75, budget: 140, usage: 'lazy · portrait 3/4' },

  { src: 'pate-chartres-tranche-original.jpg', dst: 'pate-chartres-signature.webp',
    w: 1400, h: 1750, quality: 78, budget: 170, usage: 'lazy · portrait 4/5' },

  { src: 'comptoir-charcuterie-original.jpg', dst: 'comptoir-charcuterie.webp',
    w: 800, h: 600, quality: 75, budget: 90, usage: 'lazy · landscape 4/3' },
  { src: 'tourte-chaude-original.jpg', dst: 'tourte-chaude.webp',
    w: 800, h: 600, quality: 75, budget: 90, usage: 'lazy' },
  { src: 'terrines-vitrine-original.jpg', dst: 'terrines-vitrine.webp',
    w: 800, h: 600, quality: 75, budget: 90, usage: 'lazy' },
  { src: 'ardoise-craie-original.jpg', dst: 'ardoise-craie.webp',
    w: 800, h: 600, quality: 75, budget: 90, usage: 'lazy' },

  { src: 'cave-lustre-original.jpg', dst: 'cave-lustre.webp',
    w: 1920, h: 1280, quality: 70, budget: 180, usage: 'lazy · cave background' },
  { src: 'sous-sol-fauteuils-original.jpg', dst: 'sous-sol-fauteuils.webp',
    w: 800, h: 600, quality: 75, budget: 100, usage: 'lazy · grid' },
  { src: 'sous-sol-detail-original.jpg', dst: 'sous-sol-detail.webp',
    w: 800, h: 600, quality: 75, budget: 100, usage: 'lazy · grid' },

  { src: 'carte-chartres-screenshot.png', dst: 'carte-chartres.webp',
    w: 1200, h: 600, quality: 72, budget: 80, usage: 'lazy · venir section' },

  { src: 'comptoir-interieur-original.jpg', dst: 'og-image.webp',
    w: 1200, h: 630, quality: 80, budget: 130, usage: 'og:image · social (fallback : comptoir tant que façade non fournie)' },
];

async function run() {
  await fs.mkdir(DST_DIR, { recursive: true });
  let totalKB = 0;
  let processed = 0;
  let missing = 0;

  for (const item of PIPELINE) {
    const srcPath = path.join(SRC_DIR, item.src);
    const dstPath = path.join(DST_DIR, item.dst);
    try {
      await fs.access(srcPath);
    } catch {
      console.log(`⏭️  ${item.dst} → source manquante (${item.src})`);
      missing += 1;
      continue;
    }
    try {
      const buffer = await sharp(srcPath)
        .resize(item.w, item.h, { fit: 'cover', position: 'attention' })
        .webp({ quality: item.quality, effort: 6 })
        .toBuffer();
      await fs.writeFile(dstPath, buffer);
      const kb = Math.round(buffer.length / 1024);
      totalKB += kb;
      processed += 1;
      const status = kb <= item.budget ? '✅' : '⚠️  OVER';
      console.log(`${status} ${item.dst} → ${kb} Ko (budget ${item.budget} Ko) · ${item.usage}`);
    } catch (err) {
      console.error(`❌ ${item.src} → ${item.dst} : ${err.message}`);
    }
  }

  console.log('');
  console.log(`📦 ${processed} image(s) générée(s), ${missing} source(s) manquante(s).`);
  console.log(`📦 Total transféré : ${totalKB} Ko (budget global < 1500, cible < 1200).`);
}

run();
