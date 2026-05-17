# Checklist d'extraction par source publique

Que chercher dans chaque source quand Mike donne 1-4 URLs publiques d'un resto cible. Le but : remplir le settings YAML avec un maximum d'infos justes en un seul WebFetch par source.

---

## Fiche Google Business (GMB)

**Format d'URL typique :**
- `https://maps.google.com/?cid=XXXXX`
- `https://www.google.com/maps/place/Nom-du-Resto/@lat,lng,zoom/...`
- `https://share.google/XXXX` (lien court partagé)
- `https://goo.gl/maps/XXXX`

**À extraire en priorité** (carte la plus riche d'infos d'un coup) :

| Champ settings | Source GMB |
|---|---|
| `nom` | Titre de la fiche |
| `slogan` ou `baseline` | Catégorie principale + ville (ex: "Pizzeria à Chartres") si pas de slogan officiel |
| `adresse` | Bloc "Adresse" complet, format `rue, code postal ville` |
| `geo.lat` / `geo.lng` | Coords extraites de l'URL ou via Schema.org de la page |
| `telephone` | Bloc "Téléphone" — convertir en E.164 : `02 47 12 34 56` → `+33247123456` |
| `telephone_display` | Garder format français lisible (espacés par 2 chiffres) |
| `horaires` | Bloc "Horaires" — convertir en structure `jour: [{ouvre, ferme}]`. Attention aux jours fermés (créneaux vides) et aux services midi+soir séparés. |
| `avis_google.note` | Note moyenne (ex: 4.7) |
| `avis_google.count` | Nombre d'avis (ex: 87) |
| `google_avis_url` | L'URL de la fiche elle-même, qui ouvre les avis quand on clique sur la note |
| Photos | 4 à 8 photos publiques visibles dans la fiche — récupérer les URLs CDN Google `https://lh3.googleusercontent.com/...` |

**Notes :**
- Si la fiche GMB a une catégorie type "Restaurant français" → indice fort signature `traditionnel`. "Burger / Pizzeria / Foodtruck" → `fast-food`. "Restaurant gastronomique / Bistronomique / Étoilé" → `gastro`.
- Si la note < 4.0 ou count < 20, le composant Avis auto-cache. Inutile de remplir le champ `avis_google` dans ce cas.
- Toujours vérifier si la fiche a un site web renseigné (autre source potentielle à scraper).

---

## Site existant (eatbu, Wix, custom)

**Format d'URL :**
- `https://*.eatbu.com`
- `https://*.wix.com` ou domaine custom Wix
- Domaine `.fr` ou `.com` du resto

**À extraire en priorité :**

| Champ settings | Source site existant |
|---|---|
| `slogan` / `baseline` | Souvent dans le hero ou le `<title>` HTML |
| `histoire.body` | Bloc "À propos" / "Notre histoire" / "Le chef" si présent. Garder 2-3 phrases courtes. |
| `histoire.lancement_year` | Date "depuis YYYY" mentionnée quelque part dans le site |
| Menu (sections + items) | Page "La carte" / "Menu" si présente. Récupérer 5-10 plats avec prix. |
| Photos | Images visibles dans le HTML (`<img src=...>`) |
| `reseaux.*` | Liens vers Insta/FB/etc. souvent dans le footer |

**Attention aux pièges :**
- Les sites eatbu sont génériquement structurés : éviter de copier le ton "marketing eatbu" ("le meilleur du goût", etc.) dans nos baselines. Reformuler en plus sobre.
- Les Wix peuvent avoir 50 sections inutiles (testimonials générés, "Welcome to my restaurant"). Ne garder que les infos factuelles.

---

## Facebook (Page resto)

**Format d'URL :**
- `https://www.facebook.com/{page_id}`
- `https://www.facebook.com/share/XXXX/`

**À extraire** (limité par WebFetch sans auth) :

| Champ settings | Source FB |
|---|---|
| `reseaux.facebook` | L'URL elle-même |
| `histoire.body` (fallback) | Bloc "À propos" de la page si visible |
| Photos | Image de profil + photo de couverture si récupérables |

**Limitation :** Facebook ne laisse pas WebFetch lire grand-chose sans auth. La plupart des photos et posts seront inaccessibles. Considérer FB comme une source secondaire confirmative, pas comme source principale d'extraction.

---

## Instagram (compte resto)

**Format d'URL :**
- `https://www.instagram.com/{handle}`

**À extraire** (limité par WebFetch sans auth) :

| Champ settings | Source Insta |
|---|---|
| `reseaux.instagram` | L'URL elle-même |
| Bio courte | Visible parfois dans le `<meta description>` |
| Photos | Quasi impossible sans auth — proposer à Mike de capturer 4-6 photos lui-même |

**Approche recommandée :** Si Mike a accès au compte Insta du resto ou veut télécharger 4-6 photos manuellement, c'est plus efficace que de scraper. Mike peut me passer les URLs de fichiers locaux (`/images/galerie/photo-1.jpg` après upload).

---

## Quand on n'arrive pas à tout extraire

Pour chaque champ manquant à la fin du WebFetch global :

1. **Si critique pour la maquette** (nom, adresse, téléphone, horaires) → demander à Mike de le fournir explicitement avant de générer les YAML
2. **Si secondaire** (slogan, histoire, prix exact, photos hors hero) → mettre un **placeholder honnête** et noter dans le récap final que c'est à caler au brief :

| Champ manquant | Placeholder à utiliser |
|---|---|
| `slogan` | `"Restaurant {catégorie} à {ville}"` (factuel, pas marketing) |
| `baseline` | Pas la remplir (champ optionnel) |
| `histoire.body` | `"Depuis {année}, à {ville}. À compléter au brief : 2-3 phrases sur le pourquoi du resto."` |
| `prix_appel` | Ne pas la remplir (champ optionnel — pour un gastro c'est mieux sans) |
| `combo` | Ne pas l'activer (champ optionnel) |
| Photos galerie | Si < 4 photos, **désactiver** `sections.galerie: false`. Sinon la section auto-cache de toute façon. |

**Règle absolue** : ne jamais inventer un storytelling, un chef, une histoire familiale. Le patron va corriger au brief, et le décalage entre fiction et réalité crée de la défiance.

---

## Récap pour Mike — format

À la fin de l'extraction, produire un résumé clair :

```
Données récupérées pour {Nom du resto} :
  ✓ Nom, adresse, téléphone, horaires (depuis GMB)
  ✓ Note 4.7 / 87 avis (depuis GMB)
  ✓ 3 photos hero candidates (depuis site eatbu)
  ✓ Instagram et Facebook (URLs uniquement)

À valider au brief :
  ⚠ Histoire du resto (placeholder mis dans les 3 maquettes)
  ⚠ Menu détaillé (3 plats signatures détectés, prix à confirmer)
  ⚠ Photos galerie : seulement 3 trouvées (< seuil 4) → galerie désactivée
    sur les maquettes. À uploader au brief pour activer la section.
```

Ça permet à Mike d'arriver au rdv en sachant exactement quels sujets ouvrir avec le patron.
