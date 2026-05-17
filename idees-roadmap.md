# Idées en réserve — MB Studio

> Fichier de parking pour les idées stratégiques sorties en cours de session.
> À retravailler à froid, pas à chaud. Aucune décision prise sur ces sujets tant que pas explicitement validés dans `CLAUDE.md` ou `process.md`.

---

## Service "Boost réputation Google" (proposé par Mike, mai 2026)

### Le problème observé
Beaucoup de restos audités ont :
- Note < 4.0/5
- Ou peu d'avis (< 20)
- Ou les deux

C'est le facteur n°1 qui bloque leur visibilité dans le Local Pack Google. Les patrons en sont conscients mais ne savent pas comment activer le levier sans :
- Payer des faux avis (contraire à la déontologie Mike + risque de bannissement Google)
- Quémander des avis maladroitement
- Avoir un outil pour systématiser la demande au bon moment

### Pistes brainstormées par Mike
- **QR code imprimé** posé au comptoir / sur les tables / sur les tickets → renvoie directement vers le formulaire d'avis Google
- **Carte NFC** (cheap, ~1€ pièce) : le client tape avec son téléphone → ouverture instantanée de la page d'avis Google
- **Carte de fidélité physique** avec QR code d'avis intégré (cumul perks restos + collecte d'avis en même temps) — Mike note que c'est plus pertinent pour fast-food que pour gastro
- **Système d'enregistrement par téléphone** — l'idée n'est pas claire, à creuser (avis vocal ? rappel automatique ?)
- **Suggestions d'améliorations** dérivées des avis existants (lire les avis négatifs, identifier les pain points, suggérer 2-3 actions concrètes au patron)

### Pourquoi c'est puissant pour MB Studio
- Coût matériel ridicule (NFC + impression QR = <50€ par client)
- Valeur perçue énorme (le patron voit ses étoiles monter, mesurable concrètement chaque mois)
- Récurrence naturelle → justifie le Pack Suivi 50€/mois
- Différenciant fort vs concurrents (personne ne le fait dans la zone Chartres)
- Cohérent avec le pitch "votre site visible Google" (la note Google = le rang Google)

### Garde-fous (principe d'honnêteté radicale)
- ❌ Ne jamais promettre "X étoiles en Y mois"
- ❌ Ne jamais facturer pour des avis faux ou achetés
- ❌ Ne jamais inciter à supprimer/contester des avis légitimes (même négatifs)
- ✅ Ne facturer que les **outils** qui facilitent la collecte (QR, NFC, suggestions)
- ✅ Le patron reste 100% propriétaire de sa fiche (principe #7)

### Décisions à prendre (plus tard, à froid)
- [ ] Format : add-on au Pack Solo (~150€ one-shot) OU inclus dans Pack Suivi (50€/mois) OU pack séparé "Réputation +"
- [ ] Que faire des restos qui ont déjà 4.5/5 et 200 avis ? Pas la cible.
- [ ] Comment mesurer le ROI patron (avant/après) → probablement via le `monthly-report` skill
- [ ] Qui imprime quoi : Mike imprime/commande les NFC OU fournit un PDF à imprimer chez le patron ?
- [ ] Risque Google : vérifier que les QR codes directs vers "leave a review" ne sont pas considérés comme du gating (Google a un guideline anti-incitation, à lire)

---

## Reprise sélection prospects après changement de tunnel (noté 2026-05-16)

- **La Casa Tropical** avait été retenu via l'**ancien tunnel** de sélection → **à refaire** avec le nouveau flux (`scoring-prospects` → `pilote-client`). Ne pas le traiter comme acquis.
- Quand on reprendra la sélection prospects : **réinjecter les infos vues en session** (notamment **API Google Places** comme source de données prospects, en plus d'Overpass OSM / PageSpeed / Wayback déjà prévus dans `skills/scoring-prospects/SPEC.md`). À intégrer à la spec scoring quand on la code.

## Structure data prospects + veille concurrentielle (figé 2026-05-16)

**Liste prospects = ressource centrale vivante.** Source de vérité unique
`prospects/restaurants.yml` (voir `prospects/README.md`). Vues régénérées, jamais
éditées main : `prospects/restaurants.csv` (vue plate claire pour infographie / Sheets)
+ snapshots datés `prospects/{ville}-{date}/`. Les outils écrivent `scan`/`scoring`,
`pilote-client` écrit `tunnel`, Mike garde `notes_mike` + `mike_override` (jamais
écrasés). SPEC `scoring-prospects` mise à jour en conséquence (Étape 7 = sync + vues).

**Veille concurrentielle** = `veille-concurrentielle.md` (fichier vivant, on empile).
Carburant explicite des 2 leviers : nouveautés outils/API → enrichissent le scan ;
standards qui bougent + objections récurrentes → font évoluer le tunnel. À brancher
sur le café mensuel du `monthly-report`. Décision à prendre plus tard : en faire un
skill dédié `/veille` ou rester en routine manuelle assistée.

## Add-on payant "Module Commande/Réservation" (court-list validée 2026-05-16)

**Modèle décidé (principe) :** on n'héberge/ne maintient jamais la caisse du patron. Le
patron souscrit l'outil **dans son propre compte** (il paie l'abo, il possède — cohérent
principe #7), Mike **intègre** au site (bouton/lien/widget, maintenance ≈ 0) et facture un
**forfait installation one-shot** en add-on du Pack Solo. Bon filtre = "est-ce que ça
m'ajoute du travail récurrent / une responsabilité intenable solo non-dev ?" (pas "est-ce
que ça coûte de l'argent" — l'argent investi par le patron est OK si ça rapporte).

**Court-list à maîtriser (2 outils + 1 entrée 0€) :**
- **Réservation** : *Guestonline* (~77€/mois patron, 0 commission, indépendant) en défaut ;
  *Zenchef* (~129€/mois) en alternative "plus gros". Éviter TheFork par défaut (commission
  par couvert + dépendance place de marché = moins "propriétaire").
- **Commande / Click&Collect** : *Collectly* (49,99€/mois HT patron, 0% commission, marque
  blanche, résiliable, live <24h) à tester en premier. Alternatives 0% : Clickeat,
  Deliver by Linkeo.
- **Entrée 0€** (resto pas prêt à payer) : formulaire de commande → mail/WhatsApp/tel,
  intégré par Mike au template. Pas de paiement en ligne mais honnête et gratuit.

**TODO avant de vendre / figer dans process.md :**
- [ ] Tester une vraie mise en place Guestonline + Collectly (compte de test) — valider
  intégration réelle dans le template (bouton/widget) + temps de mise en place.
- [ ] Re-vérifier prix/fonctions auprès des éditeurs (ça bouge — honnêteté radicale).
- [ ] Figer le **prix du forfait installation** (piste évoquée : +150–250€ one-shot).
- [ ] Décider : add-on Pack Solo seul, ou aussi proposé dans Pack Suivi.
- [ ] Une fois testé+tranché → graver offre + objection dans `process.md`.
