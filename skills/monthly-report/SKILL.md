---
name: monthly-report
description: "Génère le rapport mensuel patron (1 page A4 lisible en 30 secondes) en agrégeant 4 sources : Umami (analytics site), GMB Insights (visites profil + clics téléphone), Google Search Console (mots-clés Google) et PageSpeed Insights (vitesse + Core Web Vitals). Étape 5 du process commercial (J+30 puis récurrent pour le Pack Suivi 50€/mois). Output : `briefs/{slug}/rapports/{YYYY-MM}.md` formaté pour impression A4 + 2 actions concrètes recommandées. MANDATORY TRIGGERS: 'monthly report', 'monthly-report', 'rapport mensuel de'. STRONG TRIGGERS: 'génère le rapport mensuel pour [resto]', 'fais le rapport J+30 de', 'cafe mensuel avec [resto]'. Ne pas déclencher pour : rapport ad hoc en milieu de mois, rapport agrégé multi-clients (à venir plus tard)."
---

# Monthly Report

Skill MB Studio pour générer **le rapport mensuel 1 page** que Mike remet au patron lors du café mensuel (étape 5 du process commercial, puis tous les mois si Pack Suivi).

L'objectif : **prouver la valeur du site** en 30 secondes de lecture, avec des chiffres concrets et **2 actions à activer** pour le mois suivant. C'est ce qui justifie l'abonnement 50€/mois.

L'output est conçu pour être **imprimé sur 1 page A4** (ou montré sur tablette en portrait). Pas un dashboard de 12 graphiques — un résumé exploitable.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Génère le rapport mensuel pour Le Saint-Hilaire, RDV café demain"
- "Monthly report {slug}" (le mois en cours)
- "Fais le rapport J+30 de {slug}" (premier rapport, post-livraison)

**Mauvais cas d'usage (ne pas déclencher) :**
- Rapport ad hoc en milieu de mois (le rapport est mensuel par définition)
- Site livré il y a < 30 jours (pas assez de data pour être pertinent)
- Patron sans Pack Suivi et déjà reçu son rapport J+30 (ne pas surcharger)

---

## Inputs requis

Demander à Mike au démarrage :

> "OK rapport mensuel. Donne-moi :
> 1. Le slug du client (pour le dossier `briefs/{slug}/rapports/`)
> 2. Le mois cible (YYYY-MM, par défaut le mois précédent)
> 3. C'est le 1er rapport (J+30 post-livraison) ou un récurrent (Pack Suivi) ?"

---

## Process en 6 étapes

### Étape 1 — Collecte des chiffres bruts

Pour chaque source, récupérer les chiffres du mois cible. Voir `references/data-sources.md` pour la procédure détaillée d'accès à chaque source.

#### Source 1 — Umami (analytics site)

- Visiteurs uniques
- Pages vues totales
- Top 5 pages les plus consultées
- Sources de trafic (Direct, Google Search, Facebook, Instagram, autres)
- Pays (devrait être 95%+ France pour un resto chartrain)
- Appareils (mobile vs desktop — généralement 70/30 pour un resto)

Si Mike n'a pas encore branché Umami sur le site client : noter "Umami pas installé" et utiliser des fallbacks (Cloudflare Web Analytics par défaut, gratuit, déjà actif).

#### Source 2 — GMB Insights

Aller sur `business.google.com` → fiche client → onglet "Statistiques" → période = mois cible.

- Vues de profil (combien de personnes ont vu la fiche)
- Recherches (combien ont cherché le resto explicitement)
- Recherches de découverte (combien ont trouvé via une catégorie)
- Clics sur le téléphone
- Clics sur l'itinéraire
- Clics sur le site web

#### Source 3 — Google Search Console

Aller sur `search.google.com/search-console` → propriété du site client → Performances → période = mois cible.

- Clics totaux (depuis Google Search)
- Impressions totales (combien de fois le site est apparu dans Google)
- Position moyenne (1 à 100, plus bas = meilleur)
- Top 5 requêtes (mots-clés qui ont amené des visites)

Si pas encore configuré : utiliser le 1er rapport J+30 pour le configurer ensemble côté Mike (5 min de setup).

#### Source 4 — PageSpeed Insights

Lancer `https://pagespeed.web.dev/` sur l'URL du site client (mode Mobile).

- Score Performance (sur 100)
- LCP (Largest Contentful Paint, en secondes)
- CLS (Cumulative Layout Shift)
- INP (Interaction to Next Paint, en ms)

#### Source 5 (bonus) — Avis Google du mois

Compter les nouveaux avis publiés ce mois-ci + variation de la note moyenne.

### Étape 2 — Comparaison vs mois précédent

Si ce n'est pas le 1er rapport, comparer chaque KPI au mois précédent :

| KPI | Mois cible | Mois -1 | Variation |
|---|---|---|---|
| Visiteurs uniques | X | Y | +Z% ou -Z% |
| Clics téléphone GMB | X | Y | +/- |
| Position moyenne Google | X.X | Y.Y | meilleure / moins bonne |
| Score PageSpeed | X/100 | Y/100 | stable / + / - |

Mettre une **flèche** ↗ pour amélioration, ↘ pour régression, ↔ pour stable.

### Étape 3 — Identification des 2 actions à recommander

Le rapport doit **toujours** proposer 2 actions concrètes pour le mois suivant. Voir `references/action-priorisation.md` pour la matrice de choix.

Critères de sélection des actions :

1. **Impact mesurable** : l'action peut être vérifiée dans le rapport du mois suivant
2. **Faisable par le patron** (sans Mike) : pour rester dans la simplicité
3. **Adaptée aux faiblesses du mois** : si la position Google chute → action SEO ; si le PageSpeed se dégrade → action perf ; si pas d'avis ce mois → action engagement

10 actions types (à piocher dans `references/action-priorisation.md`) :

- "Publier 1 post GMB par semaine sur les 4 prochaines semaines"
- "Demander 5 avis Google à vos meilleurs clients ce mois"
- "Ajouter 3-5 photos récentes (plats du moment, terrasse, équipe)"
- "Répondre aux 3 avis non répondus dans les 48h"
- "Mettre à jour vos horaires si vous avez des changements saisonniers"
- "Ajouter votre menu en photo HD dans la fiche GMB"
- "Activer/désactiver un attribut détecté incorrect"
- "Programmer un post sur l'événement à venir (Saint-Valentin, fête des mères, etc.)"
- "Inviter 2 amis foodies à laisser un avis (jamais 'famille proche' qui pollue les avis)"
- "Modifier la description si elle ne mentionne pas {keyword sous-utilisé}"

### Étape 4 — Génération du rapport

Remplir le template `templates/rapport-mensuel.md.tpl` avec les chiffres collectés.

Format imposé :
- **1 page A4** maximum (police 11pt, marges 2cm)
- **Un en-tête** avec nom du resto + mois + date d'envoi
- **Bloc "Ce mois en chiffres"** : 4-5 KPIs les plus parlants, avec flèches de comparaison
- **Bloc "Ce qui a marché"** : 2-3 phrases factuelles sur le positif du mois
- **Bloc "Ce qu'on peut améliorer"** : 1-2 phrases sur les faiblesses identifiées
- **Bloc "Actions pour le mois prochain"** : 2 actions concrètes en bullets
- **Bloc "Le mot de Mike"** : 1-2 phrases personnelles (anecdote, conseil, encouragement)

Sauver dans `briefs/{slug}/rapports/{YYYY-MM}.md`.

### Étape 5 — Génération de la version imprimable (optionnel)

Convertir le markdown en PDF imprimable A4 :

```powershell
# Via pandoc si installé :
pandoc briefs/{slug}/rapports/{YYYY-MM}.md -o briefs/{slug}/rapports/{YYYY-MM}.pdf --pdf-engine=wkhtmltopdf
```

Ou via Chrome headless en mode print :

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
& $chrome --headless --disable-gpu --print-to-pdf="briefs/{slug}/rapports/{YYYY-MM}.pdf" "file:///{path}/briefs/{slug}/rapports/{YYYY-MM}.html"
```

(Conversion préalable markdown → HTML via pandoc ou via le composant Astro de rendu markdown).

### Étape 6 — Récap pour Mike

Afficher un récap pour préparer le café mensuel :

```
✅ Rapport mensuel généré pour {NOM_RESTO} ({MOIS})

📁 Fichiers :
   - briefs/{slug}/rapports/{YYYY-MM}.md   (source)
   - briefs/{slug}/rapports/{YYYY-MM}.pdf  (imprimable)

📊 Chiffres clés du mois :
   - Visiteurs uniques : {X} ({↗+Y% / ↘-Y% / ↔ stable} vs mois -1)
   - Clics téléphone GMB : {X}
   - Position Google moyenne : {X.X}
   - Score PageSpeed : {X}/100

🎯 Les 2 actions recommandées :
   1. {ACTION_1}
   2. {ACTION_2}

🗣 Points à mentionner au café :
   - {Anecdote / observation à partager oralement, pas mise dans le rapport}
   - {Question à poser au patron : "Vous avez senti une différence depuis le post du 15 ?")
   - Si pas encore Pack Suivi : opportunité de proposer ("Ce genre de rapport, c'est ce que je vous remettrais chaque mois si vous prenez le Pack Suivi à 50€/mois.")

💡 Demande d'introduction (cf process.md étape 5) :
   "Vous avez un confrère à qui je pourrais montrer la même chose ?
    Commission 100€ si signature."
```

---

## Format d'output

Le skill produit :

1. **Fichier markdown** `briefs/{slug}/rapports/{YYYY-MM}.md` (source, modifiable)
2. **Fichier PDF imprimable** `briefs/{slug}/rapports/{YYYY-MM}.pdf` (1 page A4) — si pandoc ou Chrome disponible
3. **Récap textuel** structuré pour préparer le café mensuel

---

## Règles d'or

1. **1 page maximum**. Si le rapport dépasse 1 page, élaguer. Le patron ne lira pas 3 pages. Tout ce qui ne tient pas en page 1 est élagué ou décale au rapport suivant.

2. **Pas de jargon tech**. Test : si une phrase contient "Core Web Vitals", "CLS", "LCP", "schema.org", "Lighthouse", reformuler.
   - ❌ "Votre LCP est à 2.3s, en dessous du seuil de 2.5s recommandé par Google"
   - ✅ "Votre site charge en 2,3 secondes — c'est plus rapide que 90% des restos"

3. **Chiffres bruts arrondis**. Pour un patron, "428 visiteurs" est moins lisible que "430 visiteurs". Arrondir aux dizaines pour les centaines, aux centaines pour les milliers.

4. **2 actions, jamais 5**. Loi de l'attention en café : 2 actions = applicables. 5 actions = aucune ne sera faite.

5. **Toujours 1 chiffre positif au début**. Même un mois difficile a un chiffre positif (le score PageSpeed, le nombre d'impressions Google qui monte, etc.). Le patron doit commencer la lecture par du positif.

6. **Les 2 actions sont faisables PAR LE PATRON, pas par Mike**. Sinon le patron pense que Mike est inutile. Action = "Publier 1 post par semaine", pas "Je vais publier 1 post par semaine pour vous".

7. **Le mot de Mike est personnel**. 1-2 phrases qui montrent que Mike connaît le patron et son métier. Pas "Bonne continuation cordialement" générique.

8. **Le rapport prépare la conversation, ne la remplace pas**. Au café, le patron pose des questions, Mike les utilise pour creuser le Pack Suivi ou identifier des prochains besoins.

---

## Resources

- `references/data-sources.md` : procédure détaillée d'accès aux 4 sources (Umami, GMB Insights, Search Console, PageSpeed)
- `references/action-priorisation.md` : matrice de choix des 2 actions selon les faiblesses du mois
- `references/kpi-baseline.md` : ce qui compte vraiment pour un resto (et ce qu'on doit ignorer)
- `templates/rapport-mensuel.md.tpl` : template markdown 1 page A4 prêt à remplir

---

## Exemple d'invocation

```
Mike : Génère le rapport mensuel pour le-saint-hilaire, café avec le patron demain à 11h.
```

Le skill exécute les 6 étapes :
1. Collecte des chiffres : Umami (218 visiteurs), GMB (45 clics téléphone), Search Console (top requête "restaurant tours quai d'anjou" position 7), PageSpeed (97/100)
2. Compare vs mois précédent : visiteurs +18%, clics téléphone +25%, position Google +3 places
3. Identifie 2 actions : "Demander 5 avis Google" + "Ajouter 3 photos plats d'automne"
4. Génère le rapport markdown + PDF
5. Récap pour préparer le café : chiffres clés, actions, points oraux, opportunité Pack Suivi

Mike imprime le PDF, va au café avec, présente en 5 minutes, ouvre la discussion.
