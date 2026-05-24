---
name: gmb-setup
description: "Optimise la fiche Google Business Profile (GBP, ex-GMB) du patron pendant la production silencieuse du site (étape 3bis du process commercial, en parallèle de site-from-brief). Mike a été ajouté comme gestionnaire à l'étape 2 du brief — ce skill lui donne la procédure exacte à suivre dans `business.google.com` pour transformer une fiche pauvre en fiche pro (catégories, description, 12+ photos, horaires précis, attributs, FAQ, premier post hebdo, réponses aux avis existants). Output : capture avant/après pour le rapport de livraison + planning des posts hebdo. MANDATORY TRIGGERS: 'gmb setup', 'gmb-setup', 'optimise la fiche google de'. STRONG TRIGGERS: 'fiche google de [resto] à optimiser', 'lance le setup GMB pour'. Ne pas déclencher pour : optimisation d'une fiche dont Mike n'est pas gestionnaire (étape 2 du brief obligatoire avant), ou optimisation après livraison (utiliser monthly-report)."
---

# GMB Setup

Skill MB Studio pour **transformer la fiche Google Business du patron pendant la production silencieuse**. Tourne en parallèle de `site-from-brief` (chez Mike, 5-10 jours).

À la fin de ce skill, la fiche GMB est :
- Catégorisée précisément
- Décrite en 750 caractères qui ressortent dans les recherches locales
- Garnie de 12+ photos de qualité
- Garnie d'horaires précis (jours fermés inclus, fériés exceptionnels)
- Équipée d'attributs (terrasse, accessibilité, paiements, etc.)
- Avec une FAQ pré-remplie
- Avec un 1er post hebdo publié
- Avec les avis existants répondus (positifs ET négatifs)

C'est la moitié cachée du Pack Solo 490€ : le patron pense payer pour le site, il reçoit aussi une fiche GMB pro. C'est ce qui crée l'effet "wow" à la livraison.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Lance le setup GMB pour Le Saint-Hilaire"
- "GMB setup {slug}"
- "Optimise la fiche Google de [resto]"

**Mauvais cas d'usage (ne pas déclencher) :**
- Mike n'a pas été ajouté comme gestionnaire (étape 2 du brief manquée) → revenir au patron, finaliser l'ajout
- Optimisation après livraison déjà faite (utiliser `monthly-report` pour le suivi)
- Fiche GMB inexistante (cas rare, le patron n'en a jamais créé) → en créer une ensemble au brief, étape spéciale à ajouter dans `brief-client`

---

## Inputs requis

Demander à Mike au démarrage :

> "OK GMB setup. Donne-moi :
> 1. Le slug du client (pour les captures avant/après)
> 2. L'URL de la fiche GMB ou le nom du resto + ville
> 3. Tu confirmes que tu es ajouté comme gestionnaire ?"

---

## Process en 9 étapes

### Étape 1 — Audit initial (capture AVANT)

Avant toute modification, capturer l'état de départ de la fiche :

1. Aller sur `https://business.google.com/` connecté avec le compte Mike (gestionnaire)
2. Sélectionner la fiche du client
3. Faire **3 captures d'écran** :
   - Vue principale (catégorie + photos + note)
   - Vue Photos (combien de photos déjà uploadées par le patron ?)
   - Vue Profil (description + horaires + attributs)
4. Sauvegarder dans `.audit-{slug}/gmb-avant/`
5. Noter dans un fichier `audit-gmb.md` :
   - Catégorie actuelle
   - Note + count d'avis
   - Nb de photos
   - Présence d'une description (oui/non)
   - Horaires renseignés (oui/non/partiel)
   - Attributs renseignés (oui/non)
   - FAQ existante (oui/non)
   - Posts récents (date du dernier post)

Cet audit servira de comparaison avant/après dans le rapport de livraison (impressionne le patron).

### Étape 2 — Catégorie principale + secondaires

La catégorie principale est l'élément SEO le plus important de la fiche.

1. Ouvrir l'onglet "Modifier le profil" → section "À propos"
2. **Catégorie principale** : choisir la plus spécifique possible
   - ❌ Mauvais : "Restaurant"
   - ✅ Bon : "Pizzeria", "Crêperie", "Bistrot", "Restaurant gastronomique", "Foodtruck", "Restaurant français", "Brasserie"
3. **Catégories secondaires** (max 9, mais 3-5 c'est mieux) : compléter avec des variantes pertinentes
   - Ex pour un bistrot : "Restaurant français", "Bar", "Bistrot français", "Restaurant traditionnel"
4. **Heuristique** : la catégorie principale doit correspondre à ce que le patron répondrait à "Vous faites quel type de cuisine ?". Les secondaires sont les filtres Google que les clients utilisent.

### Étape 3 — Description (750 caractères)

La description est lue par Google pour le SEO local ET affichée aux visiteurs.

1. Onglet "Modifier le profil" → "Description"
2. Écrire une description de **600-750 caractères max** (Google coupe au-delà) qui répond à 3 questions :
   - **Qui** : nom + chef/famille + ville
   - **Quoi** : type de cuisine + spécialités signatures
   - **Pourquoi venir** : ce qui différencie (fait maison, produits locaux, ambiance, prix, halal, vegan…)

3. Structure type :

   > "{Nom du resto} est un {type de resto} situé {quartier/ville}, ouvert depuis {année}. Le chef {Nom} propose une cuisine {style} avec des produits {origine, ex: 'frais du marché des Halles'}. Spécialités : {3-4 plats signatures}. {Élément différenciant : ambiance / fait maison / halal / etc.}. {Information pratique : terrasse, parking, réservation conseillée…}."

4. **Mots-clés à intégrer naturellement** :
   - Type de cuisine (au moins 2 fois)
   - Ville (au moins 1 fois)
   - 1-2 spécialités signatures
   - Pas de "meilleur" / "incomparable" / hyperbole (Google pénalise et le patron déteste)

5. **Tester la longueur** : copier-coller dans un compteur de caractères (ex: `https://wordcounter.net/`), viser 650-750 caractères pour saturer l'espace alloué.

Voir `references/exemples-descriptions.md` pour 5 exemples concrets selon signature/type de resto.

### Étape 4 — Photos (objectif 12+ photos pertinentes)

L'algorithme Google pousse fortement les fiches avec **12+ photos** réparties sur plusieurs catégories.

Catégories de photos à couvrir :

| Catégorie GMB | Nb cible | Quoi prendre |
|---|---|---|
| **Logo** | 1 | Logo officiel carré (transparence acceptée) |
| **Couverture** | 1 | Photo grand format (1080×608 min) — la "vitrine" |
| **Intérieur** | 3-4 | Salle, tables dressées, comptoir, bar |
| **Extérieur** | 2-3 | Façade jour, façade soir, terrasse si présente |
| **Plats** | 4-6 | Plats signatures, mise en scène nette, **lumière naturelle** |
| **Équipe** | 1-2 | Photo du chef ou de l'équipe (en cuisine ou en salle) |
| **Atmosphère** | 1-2 | Photos d'ambiance (service en cours, terrasse pleine, etc.) |

Procédure :

1. Onglet "Photos" → "Ajouter des photos"
2. Uploader les photos par catégorie (Google demande de tagger chaque photo)
3. **Réutiliser les photos du brief** : Mike a déjà optimisé les photos pour le site dans `clients/{slug}/public/images/`. Réutiliser celles-là sur GMB (cohérence visuelle entre site et fiche).
4. Si manque de photos : demander à Mike de faire 4-6 photos rapides au resto la prochaine fois qu'il y passe (sinon attendre la livraison pour combler)

### Étape 5 — Horaires précis

Onglet "Modifier le profil" → "Horaires" :

1. **Heures d'ouverture régulières** : remplir pour chaque jour de la semaine (Lun-Dim)
   - Format : HH:MM-HH:MM pour chaque créneau
   - Si midi + soir : 2 créneaux
   - Si fermé : laisser vide / marquer "Fermé"

2. **Heures spéciales** (jours fériés, fermetures annuelles)
   - 14 juillet, 25 décembre, 1er janvier : noter les horaires spéciaux ou la fermeture
   - Fermeture estivale (août souvent) : programmer en avance

3. **Cohérence avec le site** : les horaires GMB doivent matcher exactement ceux du `settings.yml` du site (sinon Google détecte une incohérence et baisse le ranking)

### Étape 6 — Attributs (caractéristiques du resto)

Onglet "Modifier le profil" → "Attributs" :

Cocher tous les attributs applicables. Les plus impactants pour le SEO local :

**Accessibilité** :
- [ ] Entrée accessible en fauteuil roulant
- [ ] Toilettes accessibles
- [ ] Parking accessible

**Services** :
- [ ] Sur place
- [ ] À emporter
- [ ] Livraison
- [ ] Drive-in

**Options** :
- [ ] Terrasse
- [ ] Wifi gratuit
- [ ] Réservation conseillée
- [ ] Climatisation
- [ ] Accepte les chiens

**Régimes alimentaires** :
- [ ] Options végétariennes
- [ ] Options végétaliennes
- [ ] Options sans gluten
- [ ] Halal
- [ ] Casher

**Paiements** :
- [ ] Espèces
- [ ] Carte bancaire
- [ ] Paiement sans contact
- [ ] Tickets restaurants
- [ ] Chèques

Demander au patron au brief s'il y a des cas particuliers (ex: "accepte les groupes", "musique live le vendredi"). Sinon, cocher uniquement ceux qu'on connaît avec certitude.

### Étape 7 — FAQ (Questions et réponses)

L'onglet FAQ est sous-utilisé par 90% des restos. Le remplir donne un avantage SEO immédiat.

1. Onglet "Q&R" sur la fiche publique (côté visiteur)
2. **Pré-publier 5-8 questions probables** en tant que gestionnaire (Mike pose la question, attribue au "Propriétaire" — soi-même — et répond)

Questions types à pré-publier :

- "Acceptez-vous les réservations ?" → "Oui, par téléphone au {tel} ou en ligne sur notre site {domaine}.fr"
- "Avez-vous une terrasse ?" → "Oui, notre terrasse {nb places} couverts est ouverte de mai à septembre"
- "Êtes-vous halal / vegan / sans gluten ?" → réponse selon le brief
- "Y a-t-il un parking à proximité ?" → "{Réponse spécifique au resto}"
- "Quels sont vos plats signatures ?" → "{3 plats les plus mis en avant}"
- "Faites-vous de la livraison ?" → réponse selon le brief (Uber Eats / Deliveroo / propre flotte / non)
- "Peut-on venir en groupe ?" → "Oui jusqu'à {N} personnes, sur réservation au {tel}"
- "Acceptez-vous les tickets restaurants ?" → réponse selon le brief

### Étape 8 — Premier post hebdomadaire

Onglet "Ajouter une mise à jour" → "Ajouter une nouveauté"

Publier le **premier post hebdo** qui sera la base du rythme (1 post/semaine minimum).

Modèles selon le contexte (voir `references/post-templates.md` pour 10 modèles) :

- **Plat du jour** (le plus simple, à faire le lundi matin) : photo + 2 phrases + "Réservez au {tel}"
- **Nouvelle saison** (octobre, mai, etc.) : "Nouvelle carte d'automne dispo dès ce soir"
- **Événement** : "Soirée jazz le 25 octobre, réservation conseillée"
- **Promotion** (rare) : "Menu midi à 16,50€ du mardi au vendredi"
- **Coulisse** : photo équipe en cuisine + "Notre matinée a commencé à 6h ce matin pour préparer ça..."

Règles d'or des posts :

- **Format court** (max 300 caractères dans le texte principal)
- **Photo obligatoire** (les posts sans photo sont 5× moins vus)
- **CTA clair** à la fin (téléphone / réservation / horaire)
- **Pas de hashtags** (inutile sur GMB contrairement à Instagram)

### Étape 9 — Réponses aux avis existants

C'est l'étape la plus chronophage mais la plus impactante pour la note moyenne et le SEO.

1. Onglet "Avis"
2. Trier par "Plus récents"
3. **Répondre à TOUS les avis non répondus**, en commençant par les positifs (les négatifs demandent plus de soin)

#### Pour un avis positif 5★

Format type :

> "Merci {Prénom} pour ce retour 5 étoiles ! Heureux que {détail de l'avis : la sauce / le service / l'ambiance} vous ait plu. À très bientôt, {Nom du resto}."

Personnaliser **chaque réponse** (Google et les visiteurs détectent les copier-coller).

#### Pour un avis négatif 1-3★

Plus délicat. Règles :

- **Toujours répondre dans les 48h** (un négatif sans réponse est 3× plus impactant)
- **Reconnaître le problème** sans être trop défensif
- **Proposer de revenir** ou de discuter en privé
- **Garder un ton calme**, jamais agressif

Format type :

> "Bonjour {Prénom}, merci pour ce retour qui nous aide à progresser. Nous sommes désolés que {problème} n'ait pas été à la hauteur de vos attentes. {Action prise : 'Nous avons sensibilisé l'équipe' / 'Le plat est désormais préparé différemment'}. Si vous souhaitez nous redonner une chance, nous serions heureux de vous accueillir à nouveau. {Nom du resto}."

#### Avis sans commentaire (juste une étoile)

Pas de réponse nécessaire, mais Google compte un avis avec réponse comme plus engageant. Réponse minimale :

> "Merci pour votre note {Prénom}. À très bientôt, {Nom du resto}."

### Étape finale — Capture APRÈS + récap

1. Faire les 3 captures équivalentes à l'audit initial → `.audit-{slug}/gmb-apres/`
2. Générer un mini-rapport `audit-gmb.md` comparant avant/après :

```markdown
# Optimisation GMB — {NOM_RESTO}

## Avant (audit du {DATE})
- Catégorie : {ANCIENNE}
- Photos : {N_AVANT}
- Description : {OUI/NON}
- FAQ : {N_AVANT}
- Posts récents : {DATE_DERNIER_POST}

## Après (le {DATE})
- Catégorie : {NOUVELLE} (plus spécifique)
- Photos : {N_APRÈS} ({+M} nouvelles, par catégorie)
- Description : 720 caractères avec mots-clés locaux
- FAQ : {N_APRÈS} questions/réponses pré-publiées
- Posts : 1er post publié, planning hebdo programmé

## Ce que ça change pour vous
- Vous remontez dans les recherches "{type de cuisine} {ville}"
- Vous apparaissez sur les filtres "Halal / Terrasse / etc." selon vos attributs
- Vos avis négatifs sont tous répondus avec un ton professionnel
- Votre fiche est désormais activée pour les statistiques mensuelles (cf monthly-report)
```

Ce rapport est remis au patron à la livraison avec les chiffres avant/après en page 2 (la page 1 c'est le rendu du site).

---

## Format d'output

Le skill produit :

1. **Fiche GMB optimisée** (modifications faites en direct dans business.google.com)
2. **Captures avant/après** dans `.audit-{slug}/gmb-avant/` et `gmb-apres/`
3. **Rapport `audit-gmb.md`** dans `briefs/{slug}/` avec les chiffres comparés
4. **Planning des posts hebdo** : Mike note dans son calendrier les sujets des 4 prochaines semaines

---

## Règles d'or

1. **Mike est gestionnaire, pas propriétaire.** Toujours. Le patron reste seul propriétaire de sa fiche GMB. À tout moment, le patron peut retirer Mike via `business.google.com` → Personnes → Supprimer.

2. **Ne JAMAIS supprimer un avis** (même négatif). Google interdit la suppression d'avis (sauf cas extrême : insulte, spam évident, hors-sujet manifest). Si avis frauduleux, signaler via "Signaler" sans supprimer.

3. **Ne JAMAIS inventer d'attributs** non vérifiés. Si Mike ne sait pas si le resto accepte les tickets restaurants : demander au patron, pas cocher au hasard. Un attribut incorrect = client déçu = avis négatif.

4. **Cohérence site ↔ fiche.** Tous les éléments factuels (téléphone, adresse, horaires) doivent matcher EXACTEMENT entre le site et la fiche GMB. Google détecte les incohérences NAP (Name-Address-Phone) et baisse le ranking.

5. **Réponse aux avis = 100% des cas, jamais 50%.** Si Mike commence à répondre aux avis, il répond à TOUS les avis non répondus. Un avis sans réponse au milieu d'avis répondus crée un mauvais signal.

6. **Pas de réponse automatique générique.** Chaque réponse doit reprendre au moins 1 détail spécifique de l'avis (le plat mentionné, le moment de visite, le serveur). Sinon, les visiteurs détectent le copier-coller.

7. **Programmer le rythme post-livraison.** À la livraison, présenter au patron le planning des 4 posts hebdo suivants (1 par semaine) et lui montrer comment créer le 5e lui-même. Le Pack Suivi mensuel 50€/mois inclut 1 post/semaine fait par Mike (4 posts/mois).

8. **Mesurer l'impact dans 30 jours.** Le skill `monthly-report` (à venir) ira chercher les chiffres GMB Insights J+30 et présentera la progression au patron (visites de profil, clics téléphone, demandes itinéraire, etc.).

---

## Resources

- `references/checklist-gmb.md` : checklist exhaustive des 30+ points à vérifier (catégories, photos, attributs, etc.)
- `references/post-templates.md` : 10 modèles de posts hebdo prêts à adapter
- `references/exemples-descriptions.md` : 5 exemples de descriptions selon signature/type de resto

---

## Exemple d'invocation

```
Mike : Lance le setup GMB pour Le Saint-Hilaire. Je suis gestionnaire depuis le brief.
```

Le skill exécute les 9 étapes :
1. Audit initial avec captures avant
2. Met à jour la catégorie principale (Restaurant français au lieu de Restaurant)
3. Rédige une description de 720 caractères avec mots-clés Tours
4. Upload 8 photos additionnelles depuis le brief (total : 14 photos)
5. Complète les horaires (incluant fermetures annuelles d'août)
6. Coche 12 attributs (terrasse, wifi, accessibilité, etc.)
7. Pré-publie 6 questions/réponses
8. Publie le 1er post hebdo (plat du marché de la semaine + photo)
9. Répond aux 12 avis non répondus (8 positifs en 5 min, 4 plus délicats en 20 min)

Capture après, rapport comparatif généré, à présenter à la livraison.
