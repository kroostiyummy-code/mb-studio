# Playbook — Audit Eatbu

> Référence interne du skill `audit-eatbu`. Liste des défauts typiques observables sur un site eatbu de restaurant, et la **formulation patron-friendly** à utiliser dans le rapport. **Vouvoiement par défaut sur tout l'écrit.**

## Comment utiliser ce playbook

1. Pour chaque audit, parcourir les sections ci-dessous
2. Sélectionner les défauts qui s'appliquent au site analysé
3. Choisir les **3 plus parlants** pour ce patron particulier (visible + mesurable + réparable)
4. Reformuler avec la formulation patron suggérée

---

## Catégorie 1 — Performance / vitesse

### Site lent au chargement (> 3 secondes)
- **Comment mesurer** : `curl -w "%{time_total}\n" -o /dev/null -s [URL]` ou via WebFetch en chronométrant
- **Formulation patron** : *"Votre site met X secondes à s'ouvrir. Au-delà de 3 secondes, la moitié des gens partent avant même de voir votre carte."*
- **Source du chiffre 50%** : étude Google/SOASTA 2017 (à utiliser avec mesure)

### Images trop lourdes (> 500 KB pour la photo principale)
- **Comment mesurer** : récupérer la taille des `<img>` principaux via HEAD HTTP ou WebFetch
- **Formulation patron** : *"Votre photo de [plat/façade] pèse X Mo. C'est 10 fois trop. Sur le téléphone d'un client en 4G, elle peut mettre 5 secondes à s'afficher."*

### Pas de cache navigateur
- **Comment mesurer** : analyser headers `Cache-Control`, `ETag`
- **Formulation patron** : *"Quand un client revient sur votre site, tout se recharge à zéro. Ça consomme sa data et ralentit son ouverture."*

---

## Catégorie 2 — Mobile (le plus critique en resto)

### Site non responsive ou cassé sur mobile
- **Comment détecter** : analyser présence balise `<meta viewport>`, classes responsive dans le HTML
- **Formulation patron** : *"75% de vos visiteurs sont sur mobile. Sur mon téléphone, votre site déborde / votre menu est illisible / le bouton de réservation est à moitié coupé."*
- **Bonus** : montrer concrètement sur la tablette en activant la vue mobile

### Boutons trop petits au toucher
- **Comment détecter** : tailles `<button>` ou `<a>` < 44px
- **Formulation patron** : *"Vos boutons sont trop petits pour être cliqués au doigt. Je viens d'essayer 3 fois pour cliquer sur 'réserver'."*

### Numéro de téléphone non cliquable
- **Comment détecter** : présence/absence de `tel:` dans les `<a>`
- **Formulation patron** : *"Quand quelqu'un voit votre numéro sur son téléphone, il devrait pouvoir cliquer dessus pour appeler. Là il doit le recopier à la main, donc 9 fois sur 10 il abandonne."*

---

## Catégorie 3 — Référencement local (SEO)

### Pas de balise Schema.org Restaurant
- **Comment détecter** : chercher `application/ld+json` ou `itemtype="http://schema.org/Restaurant"` dans le HTML
- **Formulation patron** : *"Quand quelqu'un cherche 'restaurant italien Chartres' sur Google, votre resto devrait s'afficher avec votre menu, vos prix et votre note. Aujourd'hui, Google ne sait pas lire ces infos sur votre site."*

### Title et meta description génériques ou absents
- **Comment détecter** : analyser `<title>` et `<meta name="description">`
- **Formulation patron** : *"Le titre que Google affiche pour votre resto, c'est '[contenu actuel]'. C'est ce que voit chaque personne qui vous cherche. C'est trop générique / vide / mal formulé."*

### Aucune mention "Chartres" sur la page
- **Comment détecter** : compter occurrences de "Chartres" / "Eure-et-Loir" dans le texte
- **Formulation patron** : *"Sur votre site, le mot 'Chartres' n'apparaît qu'une seule fois (en bas dans l'adresse). Google a du mal à comprendre que vous êtes un resto chartrain."*

### Pas de H1 ou H1 mal optimisé
- **Comment détecter** : analyser `<h1>`
- **Formulation patron** : *"Le grand titre principal de votre page, celui que Google lit en premier, c'est juste '[contenu]'. Il devrait dire qui vous êtes, où, et ce que vous faites."*

---

## Catégorie 4 — Google My Business (la plus impactante)

### Pas de fiche GMB du tout
- **Formulation patron** : *"Vous n'apparaissez pas sur Google Maps quand on cherche votre resto. C'est urgent : 70% de vos futurs clients passent par là."*

### Fiche GMB existe mais incomplète
- **Comment détecter** : recherche manuelle, vérifier photos, catégorie, horaires, description
- **Formulation patron** : *"Votre fiche Google Maps existe mais il manque [photos / horaires / catégorie / description]. C'est gratuit à remplir et ça change votre ranking."*

### Pas de catégorie principale ou catégorie générique
- **Formulation patron** : *"Votre fiche Google dit juste 'restaurant'. Si vous mettez 'restaurant italien' ou 'pizzeria', vous remontez dans les bonnes recherches."*

### Aucun post GMB depuis > 3 mois
- **Formulation patron** : *"Vous n'avez pas posté sur votre fiche Google depuis [date]. Google considère que votre resto est moins actif que les autres. Un post par semaine suffit."*

### Photos absentes ou < 5
- **Formulation patron** : *"Vous n'avez que [X] photos sur votre fiche Google. Les restos qui ont 20+ photos reçoivent 35% de visites en plus."*
- **Source 35%** : étude Google Business Profile (à mentionner avec mesure réelle)

### Avis non répondus
- **Formulation patron** : *"Vous avez [X] avis Google et vous n'avez répondu à aucun. Répondre montre que vous êtes présent et booste votre note dans les recherches."*

---

## Catégorie 5 — Contenu et conversion

### Pas de carte téléchargeable ou consultable
- **Formulation patron** : *"Quand quelqu'un cherche votre carte, il doit cliquer 3 fois. Et elle est en image, donc Google ne peut pas la lire."*

### Pas de bouton de réservation visible
- **Formulation patron** : *"Quelqu'un qui veut réserver doit chercher comment. Pas de bouton clair en haut de page = des résa qui partent ailleurs."*

### Pas d'horaires clairement visibles dès la home
- **Formulation patron** : *"Vos horaires sont enterrés dans la page contact. C'est l'info n°1 que cherchent vos clients avant de venir."*

### Pas d'embed Google Maps
- **Formulation patron** : *"Pas de plan sur votre site = votre client ouvre Maps dans un autre onglet, et il y reste (et il voit aussi vos concurrents)."*

### Pas de lien vers Instagram/Facebook
- **Formulation patron** : *"Si vous postez des photos sur Insta, vos visiteurs site devraient pouvoir vous suivre en 1 clic. Là c'est pas évident."*

---

## Catégorie 6 — Esthétique et confiance

### Design daté (template eatbu visible)
- **Formulation patron** : *"Votre site ressemble à 200 autres sites eatbu. Un client qui voit ça pense 'banal' avant même de lire votre carte."*

### Photos de stock évidentes
- **Formulation patron** : *"Cette photo de [pizza/burger générique] vient d'une banque d'images. Vos clients le sentent. Une vraie photo de vos plats vaut 10 photos pro de stock."*

### Fautes d'orthographe
- **Formulation patron** : *"J'ai noté [X] fautes d'orthographe sur votre page d'accueil. Petit détail mais ça compte pour la confiance."*
- **Attention** : à dire avec tact, jamais de manière humiliante

### Pas de témoignages clients
- **Formulation patron** : *"Aucun avis de client sur votre site. Vous pouvez importer vos avis Google directement, ça rassure le visiteur qui hésite."*

---

## Catégorie 7 — Indépendance et coût (l'angle eatbu-spécifique)

### Adresse web "X.eatbu.com" au lieu d'un domaine propre

C'est le défaut **universel** à tous les clients eatbu et probablement le plus impactant en argumentaire commercial. Trois angles pour le formuler ; **choisir celui qui colle au profil patron en face**.

**Angle 1 — Crédibilité / image (recommandé pour patrons traditionnels et soucieux d'image) :**
> *"Votre adresse web, c'est `[nom].eatbu.com`. Quand un client tape ça dans son navigateur, il comprend tout de suite que vous louez votre site chez quelqu'un. Un resto comme le vôtre, avec [X années d'existence / vos récompenses / votre place sur la rue], mérite sa propre adresse — `[nom]-chartres.fr`, par exemple."*

**Angle 2 — Argent qui s'envole (pour patrons sensibles au coût) :**
> *"Vous payez eatbu chaque année — sans doute autour de 140€ — pour avoir le droit d'utiliser leur plateforme. Sur 5 ans, c'est 700€ pour louer un site que vous ne contrôlez pas. Un site à vous, hébergement compris à vie, c'est moins cher au final et c'est le vôtre."*

**Angle 3 — Confiance Google (pour patrons qui se plaignent du référencement) :**
> *"Google fait davantage confiance à un site qui a son propre nom de domaine — `restaurant-machin.fr` — qu'à un sous-site d'une plateforme. C'est l'un des facteurs derrière vos résultats Google."*

**Règle d'usage** : ne PAS mentionner les 3 angles dans le même audit. Choisir UN seul angle, le plus pertinent au profil détecté pendant la conversation porte-à-porte. À l'écrit (audit envoyé sans visite), prendre l'angle 1 qui passe le mieux à froid.

### Abonnement annuel récurrent, contenu non-portable
- **Formulation patron** : *"Si demain vous décidez de quitter eatbu, votre site disparaît et le contenu reste chez eux. Aucune portabilité. Un site à vous, vous le gardez à vie, même si je disparais."*

### Édition limitée / dépendance à un outil
- **Formulation patron** : *"Pour modifier votre menu, vous devez passer par leur interface — pas toujours évident, pas modifiable depuis votre téléphone. Un site moderne se modifie en 30 secondes, même depuis votre comptoir entre deux clients."*

---

## Les 3 leviers de gain (côté MB Studio)

À utiliser dans la section "3 leviers que je peux activer pour vous". Choisir les 3 plus impactants selon les défauts détectés.

| Levier (jargon interne) | Formulation patron |
|---|---|
| Nom de domaine propre | "Une adresse web à votre nom (`restaurant-machin-chartres.fr`), plus crédible et meilleure pour Google" |
| Schema.org Restaurant | "Apparaître dans Google Maps avec votre menu et vos prix visibles directement" |
| GMB optimisée | "Booster votre fiche Google Maps : photos, posts, catégories — c'est 70% de votre trafic" |
| Site mobile-first | "Un site qui marche parfaitement sur tous les téléphones, pas seulement sur ordi" |
| Vitesse < 1.5s | "Site qui s'ouvre en moins de 1,5 seconde — Google adore et vos clients aussi" |
| CMS autonome | "Vous modifiez vos plats, vos horaires, vos photos en 30 secondes, depuis votre téléphone si vous voulez" |
| Bouton resa visible | "Bouton 'Réserver' en haut de chaque page, qui appelle ou envoie un mail directement" |
| Photos optimisées | "Vos vraies photos de plats, allégées pour s'afficher en 1 seconde" |
| Réponse aux avis | "Répondre à vos avis Google chaque semaine pour montrer que vous êtes présent (inclus dans le pack mensuel optionnel)" |

---

## Les pièges à éviter dans le rapport

| Piège | Pourquoi c'est dangereux | Alternative |
|---|---|---|
| "Votre site est moche" | Vexant, jugement gratuit | "Votre design est daté par rapport aux nouveaux sites de votre catégorie" |
| "Votre site est nul en SEO" | Jargon + jugement | "Google a du mal à bien classer votre site dans les recherches locales" |
| Citer un concurrent par son nom | Crée du conflit local | "Un resto chartrain comparable" |
| Promettre la 1ère place Google | Mensonge | "Améliorer votre positionnement local" |
| Évoquer ses avis négatifs | Sujet sensible face à face | Garder pour soi, parler oralement si pertinent |
| "Vous allez perdre vos clients" | Anxiogène | "Vous pouvez récupérer X clients par mois en plus" |
| Tutoyer à l'écrit | Trop familier pour un premier contact | Vouvoyer toujours à l'écrit, basculer au tu à l'oral si le patron le fait |

---

## Données externes à valider avant usage

Les chiffres ci-dessous sont mentionnés dans les formulations. Toujours **vérifier qu'ils sont pertinents** ou les retirer si non sourçables :

- "50% des gens partent si > 3s" → Google/SOASTA 2017
- "75% du trafic resto = mobile" → varie, vérifier sur Plausible si données dispos
- "70% du trafic local vient de GMB" → estimation, à formuler "la majorité"
- "35% de visites en plus avec 20+ photos GMB" → Google Business Profile insights
- "140€/an eatbu" → tarif estimatif, à confirmer avec un client réel

**Si on doute, on retire le chiffre.** Mieux vaut une affirmation qualitative honnête qu'un chiffre douteux.
