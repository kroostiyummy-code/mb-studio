# Playbook — Audit Eatbu

> Référence interne du skill `audit-eatbu`. Liste des défauts typiques observables sur un site eatbu de restaurant, et la **formulation patron-friendly** à utiliser dans le rapport.

## Comment utiliser ce playbook

1. Pour chaque audit, parcourir les sections ci-dessous
2. Sélectionner les défauts qui s'appliquent au site analysé
3. Choisir les **3 plus parlants** pour ce patron particulier (visible + mesurable + réparable)
4. Reformuler avec la formulation patron suggérée

---

## Catégorie 1 — Performance / vitesse

### Site lent au chargement (> 3 secondes)
- **Comment mesurer** : `curl -w "%{time_total}\n" -o /dev/null -s [URL]` ou via WebFetch en chronométrant
- **Formulation patron** : *"Ton site met X secondes à s'ouvrir. Au-delà de 3 secondes, la moitié des gens partent avant même de voir ta carte."*
- **Source du chiffre 50%** : étude Google/SOASTA 2017 (à utiliser avec mesure)

### Images trop lourdes (> 500 KB pour la photo principale)
- **Comment mesurer** : récupérer la taille des `<img>` principaux via HEAD HTTP ou WebFetch
- **Formulation patron** : *"Ta photo de [plat/façade] pèse X Mo. C'est 10 fois trop. Sur le téléphone d'un client en 4G, elle peut mettre 5 secondes à s'afficher."*

### Pas de cache navigateur
- **Comment mesurer** : analyser headers `Cache-Control`, `ETag`
- **Formulation patron** : *"Quand un client revient sur ton site, tout se recharge à zéro. Ça consomme sa data et ralentit son ouverture."*

---

## Catégorie 2 — Mobile (le plus critique en resto)

### Site non responsive ou cassé sur mobile
- **Comment détecter** : analyser présence balise `<meta viewport>`, classes responsive dans le HTML
- **Formulation patron** : *"75% de tes visiteurs sont sur mobile. Sur mon téléphone, ton site déborde / ton menu est illisible / le bouton de réservation est à moitié coupé."*
- **Bonus** : montrer concrètement sur la tablette en activant la vue mobile

### Boutons trop petits au toucher
- **Comment détecter** : tailles `<button>` ou `<a>` < 44px
- **Formulation patron** : *"Tes boutons sont trop petits pour être cliqués au doigt. Je viens d'essayer 3 fois pour cliquer sur 'réserver'."*

### Numéro de téléphone non cliquable
- **Comment détecter** : présence/absence de `tel:` dans les `<a>`
- **Formulation patron** : *"Quand quelqu'un voit ton numéro sur son téléphone, il devrait pouvoir cliquer dessus pour appeler. Là il doit le recopier à la main, donc 9 fois sur 10 il abandonne."*

---

## Catégorie 3 — Référencement local (SEO)

### Pas de balise Schema.org Restaurant
- **Comment détecter** : chercher `application/ld+json` ou `itemtype="http://schema.org/Restaurant"` dans le HTML
- **Formulation patron** : *"Quand quelqu'un cherche 'restaurant italien Chartres' sur Google, ton resto devrait s'afficher avec ton menu, tes prix et ta note. Aujourd'hui, Google ne sait pas lire ces infos sur ton site."*

### Title et meta description génériques ou absents
- **Comment détecter** : analyser `<title>` et `<meta name="description">`
- **Formulation patron** : *"Le titre que Google affiche pour ton resto, c'est '[contenu actuel]'. C'est ce que voit chaque personne qui te cherche. C'est trop générique / vide / mal formulé."*

### Aucune mention "Chartres" sur la page
- **Comment détecter** : compter occurrences de "Chartres" / "Eure-et-Loir" dans le texte
- **Formulation patron** : *"Sur ton site, le mot 'Chartres' n'apparaît qu'une seule fois (en bas dans l'adresse). Google a du mal à comprendre que tu es un resto chartrain."*

### Pas de H1 ou H1 mal optimisé
- **Comment détecter** : analyser `<h1>`
- **Formulation patron** : *"Le grand titre principal de ta page, celui que Google lit en premier, c'est juste '[contenu]'. Il devrait dire qui tu es, où, et ce que tu fais."*

---

## Catégorie 4 — Google My Business (la plus impactante)

### Pas de fiche GMB du tout
- **Formulation patron** : *"Tu n'apparais pas sur Google Maps quand on cherche ton resto. C'est urgent : 70% de tes futurs clients passent par là."*

### Fiche GMB existe mais incomplète
- **Comment détecter** : recherche manuelle, vérifier photos, catégorie, horaires, description
- **Formulation patron** : *"Ta fiche Google Maps existe mais il manque [photos / horaires / catégorie / description]. C'est gratuit à remplir et ça change ton ranking."*

### Pas de catégorie principale ou catégorie générique
- **Formulation patron** : *"Ta fiche Google dit juste 'restaurant'. Si tu mets 'restaurant italien' ou 'pizzeria', tu remontes dans les bonnes recherches."*

### Aucun post GMB depuis > 3 mois
- **Formulation patron** : *"Tu n'as pas posté sur ta fiche Google depuis [date]. Google considère que ton resto est moins actif que les autres. Un post par semaine suffit."*

### Photos absentes ou < 5
- **Formulation patron** : *"Tu n'as que [X] photos sur ta fiche Google. Les restos qui ont 20+ photos reçoivent 35% de visites en plus."*
- **Source 35%** : étude Google Business Profile (à mentionner avec mesure réelle)

### Avis non répondus
- **Formulation patron** : *"Tu as [X] avis Google et tu n'as répondu à aucun. Répondre montre que tu es présent et booste ta note dans les recherches."*

---

## Catégorie 5 — Contenu et conversion

### Pas de carte téléchargeable ou consultable
- **Formulation patron** : *"Quand quelqu'un cherche ta carte, il doit cliquer 3 fois. Et elle est en image, donc Google ne peut pas la lire."*

### Pas de bouton de réservation visible
- **Formulation patron** : *"Quelqu'un qui veut réserver doit chercher comment. Pas de bouton clair en haut de page = des résa qui partent ailleurs."*

### Pas d'horaires clairement visibles dès la home
- **Formulation patron** : *"Tes horaires sont enterrés dans la page contact. C'est l'info n°1 que cherchent tes clients avant de venir."*

### Pas d'embed Google Maps
- **Formulation patron** : *"Pas de plan sur ton site = ton client ouvre Maps dans un autre onglet, et il y reste (et il voit aussi tes concurrents)."*

### Pas de lien vers Instagram/Facebook
- **Formulation patron** : *"Si tu postes des photos sur Insta, tes visiteurs site devraient pouvoir te suivre en 1 clic. Là c'est pas évident."*

---

## Catégorie 6 — Esthétique et confiance

### Design daté (template eatbu visible)
- **Formulation patron** : *"Ton site ressemble à 200 autres sites eatbu. Un client qui voit ça pense 'banal' avant même de lire ta carte."*

### Photos de stock évidentes
- **Formulation patron** : *"Cette photo de [pizza/burger générique] vient d'une banque d'images. Tes clients le sentent. Une vraie photo de tes plats vaut 10 photos pro de stock."*

### Fautes d'orthographe
- **Formulation patron** : *"J'ai noté [X] fautes d'orthographe sur ta page d'accueil. Petit détail mais ça compte pour la confiance."*
- **Attention** : à dire avec tact, jamais de manière humiliante

### Pas de témoignages clients
- **Formulation patron** : *"Aucun avis de client sur ton site. Tu peux importer tes avis Google directement, ça rassure le visiteur qui hésite."*

---

## Les 3 leviers de gain (côté MB Studio)

À utiliser dans la section "3 leviers que je peux activer pour toi". Choisir les 3 plus impactants selon les défauts détectés.

| Levier (jargon interne) | Formulation patron |
|---|---|
| Schema.org Restaurant | "Apparaître dans Google Maps avec ton menu et tes prix visibles directement" |
| GMB optimisée | "Booster ta fiche Google Maps : photos, posts, catégories — c'est 70% de ton trafic" |
| Site mobile-first | "Un site qui marche parfaitement sur tous les téléphones, pas seulement sur ordi" |
| Vitesse < 1.5s | "Site qui s'ouvre en moins de 1,5 seconde — Google adore et tes clients aussi" |
| CMS autonome | "Tu modifies tes plats, tes horaires, tes photos en 30 secondes, depuis ton téléphone si tu veux" |
| Bouton resa visible | "Bouton 'Réserver' en haut de chaque page, qui appelle ou envoie un mail directement" |
| Photos optimisées | "Tes vraies photos de plats, allégées pour s'afficher en 1 seconde" |
| Réponse aux avis | "Répondre à tes avis Google chaque semaine pour montrer que tu es présent (inclus dans le pack mensuel optionnel)" |

---

## Les pièges à éviter dans le rapport

| Piège | Pourquoi c'est dangereux | Alternative |
|---|---|---|
| "Ton site est moche" | Vexant, jugement gratuit | "Ton design est daté par rapport aux nouveaux sites de ta catégorie" |
| "Ton site est nul en SEO" | Jargon + jugement | "Google a du mal à bien classer ton site dans les recherches locales" |
| Citer un concurrent par son nom | Crée du conflit local | "Un resto chartrain comparable" |
| Promettre la 1ère place Google | Mensonge | "Améliorer ton positionnement local" |
| Évoquer ses avis négatifs | Sujet sensible face à face | Garder pour soi, parler oralement si pertinent |
| "Tu vas perdre tes clients" | Anxiogène | "Tu peux récupérer X clients par mois en plus" |

---

## Données externes à valider avant usage

Les chiffres ci-dessous sont mentionnés dans les formulations. Toujours **vérifier qu'ils sont pertinents** ou les retirer si non sourçables :

- "50% des gens partent si > 3s" → Google/SOASTA 2017
- "75% du trafic resto = mobile" → varie, vérifier sur Plausible si données dispos
- "70% du trafic local vient de GMB" → estimation, à formuler "la majorité"
- "35% de visites en plus avec 20+ photos GMB" → Google Business Profile insights

**Si on doute, on retire le chiffre.** Mieux vaut une affirmation qualitative honnête qu'un chiffre douteux.
