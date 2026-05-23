# Brief Anamour Lucé — maquette pré-porte-à-porte

> Ce dossier contient les **inputs prêts à plug** pour `site-from-brief` (et `new-client` ensuite), produits AVANT le porte-à-porte. Le brief client formel (skill `brief-client`) viendra après la visite chez le patron — il pourra confirmer, corriger ou enrichir ces inputs.

## Quoi est ici

- `content/settings/site.yml` — fiche d'âme MB Studio (partition, dominante, horaires, copywriting hero, bandeau, avis Google)
- `content/menu/sections/` — 4 sections menu (grillades, spécialités, mezzés, desserts) avec **prix indicatifs à confirmer au brief**
- `content/galerie/galerie.yml` — 6 placeholders Picsum avec alt-texts indiquant les vraies photos cibles

## Contexte stratégique

Voir [`prospects/anamour-luce/analyse-prebrief.md`](../../prospects/anamour-luce/analyse-prebrief.md) pour :
- Lecture émotionnelle complète (6 dimensions)
- Direction artistique « Dark Mediterranean Grill Lounge »
- Photos cibles prioritaires
- Spine commercial « VENIR » → CTA principal Réserver une table

## Choix appliqués dans cette maquette

| Dimension | Choix | Raison |
|---|---|---|
| Spine | `venir` | Le lieu physique est plus fort que le digital — il faut faire venir avant commander |
| Hero | `editorial` | Statement émotionnel « La braise turque, à Lucé. » — mérite une mise en scène |
| Tempo / densité | 2 / 2 | Lounge calme, équilibre photos+textes |
| Média | **3** | Intensité visuelle haute — l'analyse pointe une DA forte |
| Motion | **1** | Lounge calme — le mouvement vient du feu et des photos, pas des animations |
| Dominante | `#b87333` cuivre chaud | Couleur métal de braise + cohérent avec la DA |
| Display font | Playfair Display (défaut MB Studio) | Élégance lounge — pas besoin de switcher pour cette première version |
| Sections actives | bandeau, histoire, avis, menu, galerie, localisation, reseaux | Pas de réservation (pas de système réservation visible) ; pas d'exigence (pas d'argument unique fort comme « 100% halal certifié » à valider) |

## À reprendre au brief signé

- [ ] Prix réels du menu (les actuels sont indicatifs cohérents avec « 10-20 € » de l'analyse)
- [ ] Année de création du restaurant (`est_year`)
- [ ] Géo précis (`geo.lat / lng` actuels = estimation depuis l'adresse)
- [ ] URL Google avis (`google_avis_url`)
- [ ] Réseaux complémentaires (Facebook, TikTok ?)
- [ ] Vraies photos à uploader (cf moodboard à générer pré-brief)
- [ ] Valider/affiner copywriting de l'histoire et du bandeau
- [ ] Décider DA finale : ivoire+cuivre (maquette actuelle) vs. base sombre lounge plus radicale

## Suite

1. Générer un **moodboard photo** (`methode-emotionnelle.md` → moodboard IA obligatoire) avec les photos cibles listées dans `analyse-prebrief.md`
2. Faire le porte-à-porte avec cette maquette HTML sur tablette + moodboard imprimé
3. Si signe → vrai brief-client (12 sujets), puis `site-from-brief` qui consommera ces inputs + ceux du brief signé
