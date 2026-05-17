---
name: maquette-flash
description: "Génère 3 maquettes de site resto (Fast-food / Gastro / Traditionnel) à partir de 1 à 4 liens publics du resto cible (fiche Google Business, Facebook, Instagram, site existant). Output unique : 3 captures PNG haute résolution prêtes à charger sur la tablette pour la visite porte-à-porte. MANDATORY TRIGGERS: 'maquette flash', 'maquette-flash', 'génère les maquettes pour', 'prépare les maquettes de'. STRONG TRIGGERS (avec contexte resto): 'prépare une maquette pour [resto]', 'fais-moi 3 maquettes du resto X', 'maquettes pour ma visite chez', 'j'ai rdv chez X, sors les maquettes'. Ne pas déclencher pour : maquettes hors-resto, sites non-Chartres prioritaires, ou demande explicite d'une seule signature (utiliser directement le template site-resto/ dans ce cas)."
---

# Maquette Flash

Skill MB Studio pour produire **3 maquettes différenciées** d'un futur site resto en 30 minutes, prêtes à présenter sur tablette lors d'une visite porte-à-porte.

L'output est conçu pour être **affiché sur tablette devant le patron**, dans l'ordre "1 primaire + 2 alternatives en backup" (voir `references/pitch-presentation.md`). Pas un PDF, pas un site déployé : 3 captures PNG haute résolution chargées dans la galerie photo de la tablette, prêtes à swiper en 2 secondes.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Maquette flash pour Le Saint-Hilaire, voici leur fiche Google + Insta : [URLs]"
- "Prépare les maquettes pour La Vesuvio à Chartres, j'y vais vendredi"
- "J'ai 4 liens du resto Le Comptoir, génère les 3 maquettes"

**Mauvais cas d'usage (ne pas déclencher) :**
- Mike demande une SEULE signature (élégante par exemple) → utiliser directement le template avec swap manuel d'une fixture
- Resto hors Chartres/Eure-et-Loir (non prioritaire en phase 1)
- Pas de lien public fourni et pas de moyen d'en récupérer (rare)

---

## Inputs requis

L'utilisateur doit fournir :

1. **Nom du restaurant cible** (sert de slug pour les fichiers, ex: `le-saint-hilaire`)
2. **1 à 4 URLs publiques** parmi :
   - Fiche Google Business (URL `maps.google.com/...` ou `share.google/...`)
   - Page Facebook
   - Profil Instagram
   - Site existant (eatbu, Wix, Shopify, etc.)
3. **Signature primaire d'intuition** : `fast-food`, `gastro` ou `traditionnel`. Cette intuition se forme en regardant rapidement les photos du resto (esthétique urbain/raffiné/familial). Mike connaît son terrain, il décide.

Si Mike ne précise pas la signature primaire, **demander en une phrase** :
> "Tu sens l'univers du resto plutôt urbain/moderne, élégant/raffiné, ou tradition/familial ?"

Mapper : urbain → `fast-food`, élégant → `gastro`, tradition → `traditionnel`.

---

## Process en 6 étapes

### Étape 1 — Récupération des données publiques

Pour chaque URL fournie, lancer `WebFetch` et extraire les infos selon la checklist détaillée dans `references/extraction-checklist.md`. Récupérer en priorité :

- **Nom officiel** et baseline/slogan
- **Adresse complète** (rue, ville, code postal)
- **Téléphone** (format français à 10 chiffres, à convertir en E.164 +33...)
- **Horaires hebdomadaires** structurés (par jour, créneaux midi/soir)
- **Note Google + nombre d'avis** (si fiche GMB accessible)
- **URL de la page d'avis Google** (pour le CTA "Lire les avis")
- **Réseaux sociaux** liés (Insta, FB, TikTok, Snap)
- **URLs des 4-6 photos publiques** les plus fortes (plats, salle, équipe)

### Étape 2 — Gap analysis et complétion manuelle

Lister ce qui manque pour faire 3 maquettes solides :
- Photos : si on n'a pas pu récupérer 4+ photos via WebFetch (Insta/FB exigent souvent une auth), demander à Mike de me fournir 1-4 URLs d'images publiques OU de pointer des fichiers locaux qu'il a téléchargés sur sa tablette
- Histoire du resto : si elle n'apparaît nulle part, **ne pas l'inventer**. Mettre un placeholder honnête type "Depuis YYYY, [Ville]. Carte du marché, vins choisis avec soin." que Mike pourra ajuster oralement au rdv
- Allergènes / menu détaillé : pas indispensable pour la maquette (réglé au brief), mettre 2-3 plats signatures détectés sur GMB/site avec prix approximatifs

### Étape 3 — Choix des palettes par signature

Chaque maquette aura **sa propre dominante**, pas la même partout. Heuristique :

| Signature | Dominante suggérée | Logique |
|---|---|---|
| Fast-food | Couleur saturée du logo / enseigne si détectée, sinon `#8b0e0e` (rouge profond) | Punchy, contraste fort |
| Gastro | Couleur sombre du registre gastro : `#1a4d3a` (vert forêt), `#2a2825` (anthracite), ou un bordeaux sombre `#5a1f1f` selon le resto | Sobriété, contraste doux |
| Traditionnel | Brun terre `#7d3c1a`, ocre `#a86d2d`, ou bordeaux profond `#6b1e1e` | Chaleur, terroir |

Si Mike a une intuition de couleur (ex: le logo est jaune et bleu) : le suivre.

### Étape 4 — Génération des 3 fichiers settings

À partir des fixtures existantes dans `templates/site-resto/examples/`, créer **3 fichiers** dans le même dossier :

- `maquette-{slug}-fast-food.yml`
- `maquette-{slug}-gastro.yml`
- `maquette-{slug}-traditionnel.yml`

Chaque fichier hérite des infos communes (nom, adresse, horaires, photos, etc.) et change :
- `signature` : la signature correspondante
- `dominante` : la couleur choisie pour cette signature
- Le ton des textes (kicker, baseline, headline) adapté au registre :

| Champ | Fast-food | Gastro | Traditionnel |
|---|---|---|---|
| `reservation.kicker` | "Pas envie de faire la queue ?" | "Une table en vue ?" | "Une bonne table ?" |
| `reservation.titre` | "Réservez votre commande." | "Réservez votre soirée." | "Réservez votre repas." |
| `histoire.statement_lead` | "N°1 à" / "Le 1er" | "Cuisine du" / "L'esprit" | "Depuis X" / "3 générations" |
| `bandeau.messages` | court, claquant, en majuscules | descriptif, italique | familier, factuel |

S'inspirer des 3 fixtures existantes (`kroosti-foodtruck.yml`, `gastronomique-elegant.yml`, `bistrot-tradition.yml`) pour le ton.

### Étape 5 — Capture des 3 PNG

Pour chaque signature, exécuter la séquence :

1. Vérifier que le serveur dev Astro tourne sur `localhost:4321` (sinon le démarrer en background via `npm run dev` dans `templates/site-resto/`)
2. Copier `templates/site-resto/examples/maquette-{slug}-{signature}.yml` vers `templates/site-resto/src/content/settings/site.yml`
3. Attendre 3 secondes (hot-reload Astro)
4. Lancer Chrome headless avec `--window-size=1440,7000` (assez haut pour capturer toute la page sans scroll)
5. Sauver la capture dans `.maquettes/{slug}/{signature}.png`

**Important** : à la fin du dernier capture, **restaurer** `templates/site-resto/src/content/settings/site.yml` depuis `templates/site-resto/examples/kroosti-foodtruck.yml` pour laisser l'environnement propre.

### Étape 6 — Récap pour Mike

Produire un récap textuel court :

```
Maquettes prêtes pour {Nom du resto}

Signature primaire (à montrer en 1er) : {signature_primaire}
  → .maquettes/{slug}/{signature_primaire}.png

Backups (à montrer si le patron hésite) :
  → .maquettes/{slug}/{signature_2}.png ({signature_2})
  → .maquettes/{slug}/{signature_3}.png ({signature_3})

Données récupérées depuis : {liste des URLs sources}

À valider/ajuster au brief :
  - [liste des champs incertains : histoire, prix exact, etc.]
```

---

## Format d'output (imposé)

Le skill produit **uniquement** :

1. Trois fichiers YAML dans `templates/site-resto/examples/maquette-{slug}-*.yml`
2. Trois fichiers PNG dans `.maquettes/{slug}/*.png` (dossier créé si absent)
3. Le récap textuel en sortie console

**Aucun autre artefact**. Pas de PDF, pas de site déployé, pas de mail envoyé. Mike charge les 3 PNG sur sa tablette (via cloud sync ou câble) et c'est terminé.

---

## Règles d'or

1. **Primaire + 2 backups, pas 3 en parallèle.** Le récap nomme clairement la signature primaire que Mike doit montrer en premier. Les 2 autres sont en backup ("si le patron tique"). Voir `references/pitch-presentation.md`.

2. **70% de fidélité suffit.** La maquette de prospection n'a pas besoin d'être 100% juste. Elle doit être suffisamment crédible pour que le patron se voie dedans en 30 secondes. Les 30% restants se calent au brief (étape 2 du process commercial).

3. **Ne jamais inventer.** Si l'histoire du resto, le prix exact, ou un autre détail n'est pas trouvable publiquement, mettre un placeholder honnête plutôt que d'inventer un faux storytelling qui sera contredit au brief.

4. **Vouvoiement systématique** dans tous les textes générés (kicker, baseline, etc.). Le tutoiement reste possible à l'oral uniquement.

5. **Photos manquantes** : si on n'a pas 4 photos publiques de qualité, **désactiver** la galerie pour cette maquette (`sections.galerie: false`) plutôt que de remplir avec des placeholders Picsum qui se voient. La galerie cachée est cohérente avec l'auto-hide intelligent du template.

6. **Pas de menu détaillé** dans la maquette. Mettre 2-3 plats signatures avec prix approximatifs, et un combo si évident. Le menu complet se construit au brief.

7. **Restaurer Kroosti à la fin.** Toujours. L'environnement reste propre pour les prochaines sessions.

8. **Une fixture par signature, jamais 3 fichiers identiques.** Les 3 maquettes doivent être visiblement différentes (palette + signature + ton des textes), c'est ce qui donne du sens au "1 primaire + 2 alternatives".

---

## Resources

- `references/extraction-checklist.md` : que chercher dans chaque source publique (GMB / Facebook / Instagram / site existant)
- `references/pitch-presentation.md` : rappel concentré du pitch "primaire + 2 backups" (la version longue est dans `process.md` à la racine du repo)
- `templates/site-resto/examples/` : 3 fixtures de référence (Kroosti / gastro / bistrot) qui servent de squelettes de départ pour les nouvelles maquettes

---

## Exemple d'invocation

```
Mike : Maquette flash pour Le Saint-Hilaire à Chartres, j'y vais jeudi.
       Voici leur fiche Google : https://maps.google.com/...
       Et leur site eatbu : https://saint-hilaire.eatbu.com
       Mon intuition : élégant.
```

Le skill exécute les 6 étapes et retourne 3 PNG dans `.maquettes/le-saint-hilaire/` (gastro en primaire, fast-food et traditionnel en backup) + un récap des données récupérées et des points à valider au brief.
