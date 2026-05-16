import { defineCollection, z } from 'astro:content';
import { file, glob } from 'astro/loaders';

const jourEnum = z.enum(['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']);

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
    // Pack typo : variante de polices DANS la signature (différenciation inter-clients).
    // Piloté par Mike (jamais exposé Decap). Optionnel → défaut par signature dans Layout.astro.
    pack_typo: z.string().optional(),
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
    google_maps_embed_url: z.string().url().optional(),
    reseaux: z.object({
      instagram: z.string().url().optional(),
      facebook: z.string().url().optional(),
      tiktok: z.string().url().optional(),
      snapchat: z.string().url().optional(),
    }).optional(),
    hero_image: z.string(),
    hero_image_alt: z.string(),
    combo: z.object({
      active: z.boolean(),
      tag: z.string().default('★ COMBO'),
      formule: z.string(),
      prix: z.string(),
    }).optional(),
    // Bloc Réservation — textes éditables par patron (sinon défauts dans le composant)
    reservation: z.object({
      kicker: z.string().optional(),
      titre: z.string().optional(),
      perks: z.array(z.string()).default([]),
    }).optional(),
    // Bloc Histoire — storytelling court avec statement + emphase + timeline
    histoire: z.object({
      statement_lead: z.string(),         // ex: "N°1 à"
      statement_accent: z.string(),       // ex: "Chartres." → rendu en accent
      body: z.string(),                   // 2-3 phrases, **mot** = emphase accent
      lancement_year: z.number().int(),   // ex: 2023
    }).optional(),
    // Avis Google — note moyenne + nombre. Auto-hide si note < 4.0 OU count < 20
    avis_google: z.object({
      note: z.number().min(0).max(5),    // ex: 5.0
      count: z.number().int().min(0),    // ex: 170
    }).optional(),
    // Bandeau actualités — ticker défilant en haut de page (messages courts)
    bandeau: z.object({
      messages: z.array(z.string()).default([]),
    }).optional(),
    // Bloc Notre exigence — checklist "fait maison/local/halal..." + bannière optionnelle
    exigence: z.object({
      headline_parts: z.array(z.string()).default([]),  // ex: ["Tout.", "Vraiment **tout.**", "Fait maison."]
      items: z.array(z.string()).default([]),           // ex: ["Riz cuit minute", "Sauce maison"]
      banner: z.object({
        titre: z.string(),
        sub: z.string().optional(),
      }).optional(),
    }).optional(),
    // Mode de localisation : "fixe" (défaut, resto avec 1 adresse) ou "foodtruck" (tournées hebdo)
    mode: z.enum(['fixe', 'foodtruck']).default('fixe'),
    // Mode fixe : horaires hebdomadaires (créneaux midi / soir / continu)
    horaires: z.array(z.object({
      jour: jourEnum,
      creneaux: z.array(z.object({
        ouvre: z.string().regex(/^\d{2}:\d{2}$/),
        ferme: z.string().regex(/^\d{2}:\d{2}$/),
      })),
    })).optional(),
    // Mode foodtruck : tournée hebdo avec lieux différents par créneau
    horaires_foodtruck: z.array(z.object({
      jour: jourEnum,
      creneaux: z.array(z.object({
        lieu: z.string(),
        ville: z.string(),
        moment: z.enum(['midi', 'soir']),
        ouvre: z.string().regex(/^\d{2}:\d{2}$/),
        ferme: z.string().regex(/^\d{2}:\d{2}$/),
      })),
    })).optional(),
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

const menu = defineCollection({
  loader: glob({ pattern: 'sections/*.yml', base: './src/content/menu' }),
  schema: z.object({
    ordre: z.number(),
    nom_section: z.string(),
    items: z.array(z.object({
      nom: z.string(),
      description: z.string(),
      prix: z.string(),
      allergenes: z.array(z.string()).default([]),
    })),
  }),
});

// Galerie photo — 1 fichier YAML avec liste de photos (le patron ajoute/réordonne via Decap)
const galerie = defineCollection({
  loader: file('src/content/galerie/galerie.yml'),
  schema: z.object({
    photos: z.array(z.object({
      src: z.string(),
      alt: z.string(),
      legende: z.string().optional(),
    })).default([]),
  }),
});

export const collections = { settings, menu, galerie };
