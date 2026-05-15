# Checklist de validation visuelle avant new-client

Après le build local réussi, avant d'invoquer `new-client` pour pousser sur GitHub et déployer, **valider visuellement** le rendu sur `localhost:4321`. Cette checklist garantit qu'on n'envoie pas un site cassé en prod.

---

## Validation desktop (1440 px)

Lancer `http://localhost:4321` dans le navigateur et vérifier :

### Hero
- [ ] La photo hero charge et est nette (pas de pixelisation)
- [ ] Le nom du resto est lisible (contraste OK avec la photo en arrière-plan)
- [ ] Si `prix_appel` est défini : il s'affiche bien dans le hero
- [ ] Les tags overlay (En service, etc.) sont visibles et lisibles

### Histoire
- [ ] Le statement (huge headline) est lisible et la couleur accent appliquée sur le dernier mot
- [ ] Le body texte est lisible (pas de débordement, contraste OK)
- [ ] Les `**mots emphase**` apparaissent en couleur accent
- [ ] La timeline 2 dates s'affiche correctement (Lancement / Encore là en YYYY)

### Avis Google (si applicable)
- [ ] Si la note est ≥ 4.0 ET count ≥ 20 : le bloc s'affiche
- [ ] Si la note est < 4.0 OU count < 20 : le bloc est **absent du HTML** (vérifier via inspecteur)
- [ ] Le badge Google avec logo coloré est visible
- [ ] Les 5 étoiles sont en doré Google (#FBBC04)

### Réservation
- [ ] Le bouton téléphone géant est visible et cliquable
- [ ] L'animation wiggle de l'icône téléphone se déclenche (~toutes les 2.4s)
- [ ] Le numéro de téléphone est au bon format
- [ ] Les 3 perks (Évitez la queue, etc.) sont alignés sous le bouton

### Menu
- [ ] Le combo banner (si actif) est visible avec ombre brutaliste 6×6
- [ ] Toutes les sections du menu sont affichées dans le bon ordre
- [ ] Chaque item a un prix avec `€` en exposant (style `.cur`)
- [ ] Les allergènes sont en pills sous la description

### Exigence (si applicable)
- [ ] Le headline 3 lignes est correct, avec les emphases bien rendues
- [ ] La checklist numérotée (01/02/03/...) est lisible
- [ ] La bannière qualité finale (si présente) est visible

### Galerie (si applicable)
- [ ] Grille 4 colonnes en desktop, photos chargent en lazy-load
- [ ] Clic sur une thumbnail ouvre le lightbox `<dialog>`
- [ ] Boutons prev/next + flèches clavier ←→ fonctionnent
- [ ] ESC ferme le lightbox

### Localisation
- [ ] **Mode fixe** : adresse + grille horaires hebdo + 2 CTAs (Itinéraire / Appeler) + iframe Maps (si URL fournie)
- [ ] **Mode foodtruck** : grille 7 jours × 2 créneaux × lieux + légende ouvert/fermé + CTA téléphone
- [ ] Tous les horaires affichés correspondent au brief

### Réseaux (si applicable)
- [ ] Uniquement les réseaux renseignés s'affichent (pas de ligne vide pour un réseau absent)
- [ ] Les icônes Insta/FB/TikTok/Snap sont correctement rendues
- [ ] Les handles extraits des URLs sont corrects

### Footer
- [ ] Le nom du resto en gros + ville en accent
- [ ] Les liens du footer fonctionnent (Accueil, Carte, Nous trouver, Mentions légales)
- [ ] Le copyright avec l'année courante

### Sticky call-bar (mobile uniquement)
- [ ] Sur mobile (resize navigateur < 900px) : la barre fixe en bas avec "Appeler" + "Réserver"
- [ ] Sur desktop : la barre est `display: none`

---

## Validation mobile (375 px)

Redimensionner le navigateur à 375×812 (taille iPhone) et vérifier :

- [ ] La hero photo prend toute la largeur, le headline reste lisible
- [ ] Le menu reste lisible (les noms d'items ne débordent pas)
- [ ] La grille horaires reste utilisable (grille foodtruck = 2 colonnes lisibles)
- [ ] Le sticky call-bar apparaît bien en bas
- [ ] Aucun élément ne dépasse en largeur (vérifier `overflow-x: hidden` du body)

---

## Validation par signature

### Brutaliste
- [ ] Fond dominante (rouge profond ou couleur logo)
- [ ] Texte cream sur fond dominante
- [ ] Accent jaune acide (par défaut)
- [ ] Grain texture visible
- [ ] Ombres brutalistes 6×6 sur les boutons/cartes

### Élégante
- [ ] Fond cream lisse (pas de grain)
- [ ] Texte slate sur fond cream
- [ ] Accent doré champagne
- [ ] Hairlines 1px partout
- [ ] Italiques sur les sous-libellés

### Tradition
- [ ] Fond ivoire jauni + grain papier
- [ ] Texte noir, emphases en dominante
- [ ] Accent rouille brique
- [ ] Petites capitales sur certains titres
- [ ] Motifs ❦ entre certaines sections (si encore des stubs)

---

## Validation SEO (Schema.org)

Ouvrir l'inspecteur, onglet "Sources" ou "Éléments", chercher `<script type="application/ld+json">` :

- [ ] `@type: "FoodEstablishment"` présent
- [ ] `name`, `description`, `telephone`, `address` corrects
- [ ] `openingHoursSpecification` rempli (depuis horaires ou horaires_foodtruck)
- [ ] `priceRange: "€"` si `prix_appel` défini
- [ ] `image` pointe vers la photo hero
- [ ] Si foodtruck : `areaServed` avec villes uniques
- [ ] `sameAs` rempli avec les réseaux sociaux renseignés

---

## Test des liens

Cliquer sur chaque lien externe pour vérifier qu'il ouvre la bonne page :

- [ ] Lien téléphone → ouvre l'app téléphone avec le bon numéro
- [ ] Lien réseaux sociaux → ouvre Insta/FB/etc. avec le bon profil
- [ ] Lien avis Google → ouvre la fiche Google avec les avis
- [ ] Lien itinéraire (mode fixe) → ouvre Google Maps avec l'adresse en destination
- [ ] Lien mentions légales → ouvre la page `/mentions-legales` du site

---

## Performance (optionnel mais recommandé)

Lancer Lighthouse dans Chrome DevTools (mode "Mobile", catégories Performance + SEO + Accessibility) :

- [ ] **Performance** : score ≥ 90 (objectif : 95+)
- [ ] **SEO** : score ≥ 95
- [ ] **Accessibility** : score ≥ 90
- [ ] **LCP** : < 2.5s
- [ ] **CLS** : < 0.1

Si un score est < 90 : identifier la cause (probablement une photo non optimisée) et corriger avant `new-client`.

---

## En cas de problème détecté

1. **Petit problème visuel** (ex: emphase manquante sur un mot, prix mal formaté) : éditer directement le fichier YAML dans `clients/{slug}/src/content/` puis vérifier le hot-reload
2. **Problème de schéma** (Astro affiche une erreur) : voir `references/menu-from-brief.md` pour les règles de mapping
3. **Photo manquante ou cassée** : voir `references/images-optimization.md`
4. **Problème majeur** (build cassé, layout cassé) : ne pas pousser sur GitHub. Revenir à Mike pour clarification.

---

## Validation finale

Avant d'invoquer `new-client {slug}`, **dire à voix haute** au mode dev :

> "Le site charge sans erreur, le rendu visuel correspond au brief, les photos sont optimisées, les liens externes marchent. C'est bon pour la prod."

Si tu hésites sur une de ces 4 conditions : ne pousse PAS encore. Le coût d'un revert post-go-live est 10× supérieur à 10 minutes de vérif locale.
