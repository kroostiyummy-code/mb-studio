---
name: brief-client
description: "Questionnaire structuré pour le brief client en 1h chez le patron (étape 2 du process commercial MB Studio, après signature du bon de commande à l'étape 1). Mode interactif : Claude pose les questions dans l'ordre prescrit, Mike entre les réponses du patron, Claude reformule et synthétise. Output : `briefs/{slug}/brief.md` (document narratif complet) + `briefs/{slug}/settings.yml` (settings YAML prêt à coller dans le futur repo client pour site-from-brief). MANDATORY TRIGGERS: 'brief client', 'lance le brief', 'on fait le brief de'. STRONG TRIGGERS (avec contexte): 'je suis chez le patron pour le brief', 'rdv brief chez X', 'on remplit le brief de'. Ne pas déclencher pour : brief stratégique global MB Studio, brief pré-vente, ou simple questionnaire d'audit (utiliser audit-eatbu)."
---

# Brief Client

Skill MB Studio pour guider Mike pendant le **brief client en 1h** chez le patron (étape 2 du process commercial, juste après la signature du bon de commande à l'étape 1).

L'objectif : **repartir du rdv avec tout le contenu nécessaire à la production du site**, sans avoir à recontacter le patron pour des questions de détail. Tout est récolté en une session.

L'output est conçu pour être consommé par le futur skill `site-from-brief`. Le brief.md sert aussi de **document de référence humain** que Mike peut relire avant la livraison.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Lance le brief pour Le Saint-Hilaire, je suis chez le patron"
- "On démarre le brief de La Vesuvio"
- "RDV brief chez Le Comptoir, signature retenue : tradition"

**Mauvais cas d'usage (ne pas déclencher) :**
- Avant signature du bon de commande (le brief est étape 2, pas étape 1)
- Pour préparer une visite (utiliser `maquette-flash` à la place)
- Pour un audit froid (utiliser `audit-eatbu`)

---

## Inputs requis au démarrage

Demander à Mike, en une seule passe d'ouverture :

> "OK on lance. Donne-moi :
> 1. Le nom du resto (qui servira de slug pour les fichiers)
> 2. La signature retenue par le patron (brutalist / elegant / tradition)
> 3. Sa couleur dominante (peux être déduite du logo, ou choisie au feeling)
> 4. As-tu fait la capture eatbu ? (oui / pas encore — voir étape 0 ci-dessous)"

Si l'une des 4 manque, demander en une phrase courte. Pas de questions imbriquées : Mike est en rdv, le tempo doit être rapide.

---

## Étape 0 — Capture du site eatbu (avant d'arriver chez le patron)

**Pourquoi** : pour pouvoir comparer plus tard l'ancien site vs le nouveau dans le rapport de mise en service présenté au patron à la livraison (voir skill `audit-livraison`). Sans cette capture, la comparaison "avant/après" devient impossible.

**Quand** : à faire **avant** le rdv brief, depuis chez Mike. Pas pendant le brief (Mike est dans le rdv, focus patron).

**Comment** (30 secondes, à faire une fois) :

1. Ouvrir l'URL eatbu du patron (déjà connue depuis `audit-eatbu`).
2. Faire une capture pleine page **mobile** (375px de large, c'est le format majoritaire des visites).
3. Faire une capture pleine page **desktop** (1280px).
4. Lancer un Lighthouse mobile sur l'URL eatbu. Noter les 4 scores (Performance, Accessibilité, SEO, Bonnes pratiques) et le temps de chargement (FCP + LCP).
5. Sauvegarder dans `briefs/{slug}/eatbu-snapshot/` :
   - `mobile.png`
   - `desktop.png`
   - `lighthouse.json` (rapport brut Lighthouse)
   - `metrics.md` (résumé 4 lignes : scores + LCP + URL + date capture)

**Si Mike répond "pas encore"** au démarrage du brief : ne PAS bloquer le brief. Le rappeler en fin de session avec un "Pense à faire la capture eatbu en rentrant ce soir, avant de lancer la production." Le brief n'a pas besoin du snapshot pour fonctionner — c'est seulement `audit-livraison` qui en aura besoin plus tard.

---

## Process en 12 sujets

Le skill conduit l'entretien en couvrant les 12 sujets de `references/questionnaire.md` dans l'ordre. Pour chaque sujet :

1. **Annoncer** le sujet en une phrase ("On passe à l'histoire du resto")
2. **Poser** les questions dans l'ordre prescrit
3. **Reformuler** la réponse en synthèse courte ("Donc si je résume : depuis 2018, repris par votre fils en 2022, cuisine de marché.")
4. **Valider** ou ajuster avec Mike avant de passer au sujet suivant

Mike entre les réponses du patron de manière libre (texte court). Le skill enregistre, reformule, demande validation, passe au suivant.

### Vue d'ensemble des 12 sujets

| # | Sujet | Durée approx |
|---|---|---|
| 1 | Identité (nom, slogan, baseline, ville, téléphone) | 5 min |
| 2 | Histoire du resto | 8 min |
| 3 | Spécialités et carte | 15 min |
| 4 | Adresse et horaires (mode fixe ou foodtruck) | 5 min |
| 5 | Réseaux sociaux et avis Google | 3 min |
| 6 | Photos (transfert depuis téléphone patron) | 10 min |
| 7 | Bandeau actualités (optionnel) | 3 min |
| 8 | Notre exigence (optionnel) | 3 min |
| 9 | Réservation (textes personnalisés) | 2 min |
| 10 | Acompte 245€ encaissé (forme + reçu) | 1 min |
| 11 | Achat du nom de domaine (sur compte patron) | 5 min |
| 12 | Accès gestionnaire Google Business | 3 min |

**Total estimé : 60 min** (peut déborder à 75 min selon le patron, c'est OK).

Voir `references/questionnaire.md` pour le détail exhaustif des questions par sujet.

---

## Format d'output

À la fin du brief, le skill produit **deux fichiers** dans le dossier `briefs/{slug}/` (créer le dossier si absent) :

### 1. `briefs/{slug}/brief.md`

Document Markdown narratif structuré selon le template `templates/brief-vide.md`. Lisible par humain. Contient :
- Métadonnées de la session (date, signature retenue, etc.)
- Synthèse de l'identité du resto
- Histoire racontée par le patron, reformulée
- Carte complète avec sections, items, prix, allergènes
- Horaires structurés
- Notes de Mike sur le patron, son attitude, ses préférences exprimées
- Liste des photos transférées
- Liste des éléments restants à clarifier post-brief (si quelque chose était flou)

### 2. `briefs/{slug}/settings.yml`

Fichier YAML directement compatible avec le schéma de `templates/site-resto/`. Prêt à coller dans le `src/content/settings/site.yml` du futur repo client (qui sera créé par le skill `new-client`).

Voir `templates/settings-from-brief.yml` pour le squelette.

---

## Règles d'or

1. **Vouvoyer le patron** dans les questions formulées (mais Mike me parle à moi en tutoyant, c'est normal).

2. **Toujours demander des chiffres précis** (année exacte, prix exact, horaire HH:MM). Jamais "vers 2018", toujours "2018 ou 2019 ?". L'imprécision crée des bugs au moment de générer le site.

3. **Reformuler à la fin de chaque sujet** : "Donc si je résume bien…" puis attendre validation. Si Mike corrige, mettre à jour ma synthèse avant de passer au suivant.

4. **Pas de jargon tech** dans les questions destinées au patron. Test : si une question contient un mot anglais (sauf nom propre) ou un sigle (SEO, CMS), la reformuler.

5. **Garder le tempo**. Le brief dure 1h. Si on passe trop de temps sur un sujet, suggérer à Mike : "On peut creuser ce point après le brief si tu veux, on passe au suivant ?"

6. **Le brief est validé par le patron à la fin**. Mike lit le récap final au patron qui valide chaque point. Toute correction du patron à ce moment est intégrée immédiatement dans le brief.md.

7. **Photos = sujet sensible**. Le patron peut ne pas avoir de belles photos. Ne pas insister si la galerie sort vide — la mécanique auto-hide du template (< 4 photos = section cachée) prévoit ce cas. Mike peut proposer au patron de faire 4-6 photos rapides avec le téléphone à la fin du brief, ou de revenir avec un photographe (option Pack Pro 120€/mois mentionnée dans CLAUDE.md, à introduire après le 6e client).

8. **Acompte 245€ confirmé**. Avant de passer aux sujets contenu, vérifier que l'acompte a été encaissé (espèces / virement / chèque). Si non encaissé : signaler à Mike "Tu peux encaisser maintenant ?" en pause discrète. Pas de production sans acompte.

9. **Domaine acheté sur le compte du patron**. **Jamais** le compte de Mike (cf principe non-négociable #7 du CLAUDE.md). Mike fait acheter le domaine devant lui sur OVH/Gandi avec la carte du patron, lui rembourse les 12€ en espèces. Note les identifiants DNS uniquement.

10. **Tout ce qui n'est pas dans le brief n'est pas dans le site**. Si le patron ajoute des demandes par SMS le lendemain, c'est en option payante hors-devis. Le brief signé = périmètre figé.

---

## Resources

- `references/questionnaire.md` : les 12 sujets détaillés avec les questions exactes à poser dans l'ordre
- `templates/brief-vide.md` : template Markdown vierge à pré-remplir
- `templates/settings-from-brief.yml` : squelette settings YAML avec placeholders à remplacer

---

## Exemple d'invocation

```
Mike : Lance le brief pour Le Saint-Hilaire à Chartres.
       Signature retenue : élégante.
       Dominante : vert sombre (le logo est vert forêt).
```

Le skill démarre la session interactive. Mike entre les réponses du patron au fur et à mesure, le skill reformule et valide. À la fin du 12e sujet, le skill génère `briefs/le-saint-hilaire/brief.md` et `briefs/le-saint-hilaire/settings.yml`. Mike repart avec les 2 fichiers prêts pour la prochaine étape (production silencieuse via `site-from-brief`).
