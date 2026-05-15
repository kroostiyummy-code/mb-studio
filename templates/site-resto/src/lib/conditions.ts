/* conditions.ts — règles d'auto-hide intelligent
   Toute section avec un seuil de qualité passe par ici, JAMAIS de logique inline dans les composants. */

export const MIN_PHOTOS_GALERIE = 4;
export const MIN_RATING_AVIS = 4.0;
export const MIN_COUNT_AVIS = 20;

export function shouldShowGalerie(photoCount: number): boolean {
  return photoCount >= MIN_PHOTOS_GALERIE;
}

export function shouldShowAvis(rating: number, count: number): boolean {
  return rating >= MIN_RATING_AVIS && count >= MIN_COUNT_AVIS;
}

/* Note pour Mike : ces seuils ne sont pas des "préférences UI", ce sont des règles
   commerciales (cf. mémoire feedback-template-architecture). Un patron à 3,7★ avec 12 avis
   verrait son bloc Avis caché par défaut — c'est volontaire et c'est aussi l'argument du
   Pack Suivi mensuel ("on travaille à faire monter votre note, on activera le bloc dans 3 mois"). */
