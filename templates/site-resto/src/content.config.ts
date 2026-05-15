import { defineCollection, z } from 'astro:content';
import { file } from 'astro/loaders';

const settings = defineCollection({
  loader: file('src/content/settings/site.yml'),
  schema: z.object({
    nom: z.string(),
    slogan: z.string(),
    baseline: z.string().optional(),
    est_year: z.number().int(),
    ville: z.string(),
    region_code: z.string(),
    signature: z.enum(['brutalist', 'elegant', 'tradition']),
    dominante: z.string().regex(/^#[0-9a-fA-F]{6}$/),
    accent_override: z.string().regex(/^#[0-9a-fA-F]{6}$/).optional(),
    prix_appel: z.string().optional(),
    telephone: z.string(),
    telephone_display: z.string(),
    adresse: z.string().optional(),
    geo: z.object({
      lat: z.number(),
      lng: z.number(),
    }).optional(),
    google_avis_url: z.string().url().optional(),
    reseaux: z.object({
      instagram: z.string().url().optional(),
      facebook: z.string().url().optional(),
      tiktok: z.string().url().optional(),
      snapchat: z.string().url().optional(),
    }).optional(),
    hero_image: z.string(),
    hero_image_alt: z.string(),
    sections: z.object({
      bandeau: z.boolean().default(false),
      histoire: z.boolean().default(true),
      avis: z.boolean().default(true),
      reservation: z.boolean().default(true),
      menu: z.boolean().default(true),
      exigence: z.boolean().default(false),
      galerie: z.boolean().default(true),
      localisation: z.boolean().default(true),
      reseaux: z.boolean().default(false),
    }),
  }),
});

export const collections = { settings };
