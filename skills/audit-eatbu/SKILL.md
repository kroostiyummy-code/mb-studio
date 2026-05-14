---
name: audit-eatbu
description: "Audit gratuit en 5 minutes d'un site eatbu existant et de la fiche Google My Business associée, pour usage en porte-à-porte commercial chez les restaurateurs chartrains. Sortie unique : 1 page tablette montrable face au patron, avec 3 problèmes concrets et 3 opportunités de gain. MANDATORY TRIGGERS: 'audit eatbu', 'audite ce site eatbu', 'fais-moi un audit pour'. STRONG TRIGGERS (with restaurant context): 'analyse le site de [nom resto]', 'qu'est-ce qui va pas sur ce site', 'prépare-moi une démo pour'. Ne pas déclencher pour : audits techniques généraux, audits non-eatbu, ou audits qui ne ciblent pas un commerçant local."
---

# Audit Eatbu

Skill MB Studio pour produire un audit éclair (5 minutes) d'un site eatbu de restaurant chartrain et de sa fiche Google My Business, dans le but de **convertir un patron en client lors d'une visite porte-à-porte**.

L'output est conçu pour être **affiché sur tablette devant le patron**, pas envoyé en PDF. Lisible en 30 secondes, scannable, percutant. Trois problèmes concrets, trois opportunités, un appel à action.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Audit eatbu : https://restaurant-le-georges.eatbu.com"
- "Prépare-moi une démo pour le restaurant Le Saint-Hilaire à Chartres"
- "J'ai rendez-vous demain chez La Vesuvio, audite leur site"

**Mauvais cas d'usage (ne pas déclencher) :**
- Audit technique général d'un site (utiliser un outil dédié)
- Site non-eatbu (les problèmes structurels diffèrent)
- Resto hors zone Chartres/Eure-et-Loir (non prioritaire)
- Demande d'analyse approfondie sur 50 pages (ce skill est compact, max 1 page tablette)

---

## Inputs requis

L'utilisateur doit fournir au minimum **l'un** des deux :

1. **URL du site eatbu** (format `https://*.eatbu.com` ou `https://eatbu.com/restaurants/...`)
2. **Nom du restaurant + ville** (ex: "Le Pichet, Chartres") → le skill cherche alors le site et la fiche GMB

Si rien n'est fourni, demander en une seule phrase courte :
> "Donne-moi l'URL du site eatbu OU le nom du resto + sa ville."

---

## Process en 5 étapes

### Étape 1 — Récupération des données

Pour chaque audit, collecter ces données via les outils disponibles (`WebFetch`, `WebSearch`, `Bash` pour curl) :

**Sur le site eatbu :**
- Statut HTTP, temps de réponse
- HTML de la page d'accueil
- Présence/absence de : Schema.org Restaurant, balises `<meta description>`, `<title>` optimisé localement, `<img alt>`, formulaire contact, lien menu téléchargeable, embed Google Maps
- Taille des images principales (en KB)
- Présence de HTTPS valide
- Mentions de réseaux sociaux

**Sur Google My Business (recherche `nom_resto + ville`) :**
- Présence d'une fiche
- Note moyenne et nombre d'avis
- Catégorie principale renseignée
- Photos présentes (oui/non, nombre approximatif)
- Horaires renseignés
- Site web renseigné dans la fiche (et lequel)
- Date du dernier post GMB visible (ancien / récent / aucun)

### Étape 2 — Analyse comparative locale (1 concurrent)

Identifier **un** concurrent direct à Chartres dans la même catégorie (via `WebSearch "restaurant [type] chartres"`). Comparer rapidement sur 3 axes :
- Vitesse perçue (le concurrent charge-t-il plus vite ?)
- Présence Schema.org
- Activité GMB récente (posts, photos)

But : donner un point de comparaison concret au patron (« Le resto X juste à côté est plus rapide et a 3 posts récents sur Google »).

### Étape 3 — Sélection des 3 problèmes critiques

Parmi tous les défauts détectés, choisir **les 3 plus parlants pour un non-tech**. Critères de sélection :

- **Visible** : le patron peut le voir lui-même sur sa tablette ou son téléphone
- **Mesurable** : un chiffre, un délai, un comparatif
- **Réparable par MB Studio** : ne pas pointer un problème qu'on ne sait pas résoudre

Voir `references/playbook.md` pour la liste complète des problèmes typiques eatbu et comment les formuler.

### Étape 4 — Sélection des 3 opportunités de gain

Trois leviers concrets que MB Studio peut activer. Toujours formulés en **bénéfice patron**, pas en jargon tech :

- ✗ "Implémentation de Schema.org Restaurant"
- ✓ "Tu apparaîtras dans les recherches type 'restaurant italien Chartres' avec ton menu et tes prix directement dans Google"

### Étape 5 — Génération de l'output (template tablette)

Remplir le template `templates/audit-tablette.md` avec les données collectées. Voir la section **Format d'output** ci-dessous.

---

## Format d'output (imposé)

**Toujours** suivre cette structure exacte. Une seule page. Pas de préambule. Pas de conclusion.

```markdown
# Audit gratuit — [Nom du restaurant]

**Site analysé :** [URL eatbu]
**Date :** [date du jour]

## Ce qui va

- [1 à 3 points positifs courts, pour ne pas être négatif à 100%]

## 3 choses qui te coûtent des clients

### 1. [Titre court et concret]
[1-2 phrases en langage patron. Pas de jargon. Mention d'un chiffre quand possible.]

### 2. [Titre court et concret]
[Idem]

### 3. [Titre court et concret]
[Idem]

## 3 leviers que je peux activer pour toi

### 🎯 [Levier 1]
[Bénéfice patron en 1 phrase. Ex: "Apparaître dans Google Maps pour 'restaurant italien Chartres' avec ton menu visible directement."]

### 🎯 [Levier 2]
[Idem]

### 🎯 [Levier 3]
[Idem]

## Ce que je propose

**Pack Resto Chartres — 490€ (tarif lancement)**

- Nouveau site rapide, beau, modifiable par toi
- Setup complet de ta fiche Google
- Livré en 10 jours
- Paiement unique, jamais d'abonnement
- Tu n'es pas content après la maquette ? 100% remboursé.

**Prochaine étape :** je te prépare une maquette personnalisée gratuite sous 7 jours. Tu valides ou pas, sans engagement.
```

### Règles de format strictes

- **Une page max** quand affichée sur tablette en portrait (police 14-16pt)
- **Aucun emoji autre que 🎯** (et seulement sur les leviers)
- **Aucune mention** de : "stack", "framework", "Lighthouse score", "Core Web Vitals", "Schema.org" (langage patron uniquement)
- **Toujours** finir par la même CTA (maquette gratuite sous 7 jours)
- **Jamais** plus de 3 problèmes ni plus de 3 leviers (loi de l'attention en porte-à-porte)
- **Le prix 490€ apparaît textuellement** comme tarif lancement (pas 690€ ni 890€)

---

## Règles d'or

1. **Pas de chiffres inventés.** Si on n'a pas pu mesurer un truc (ex: pas accès aux Core Web Vitals), on ne dit pas "ton site est lent" sans preuve. On dit "j'ai mesuré le chargement de ta page d'accueil à X secondes".

2. **Pas de comparaison agressive nominative.** On ne nomme pas le concurrent dans le rapport ("Le Pichet est plus rapide que toi"). On peut dire "un autre resto chartrain dans ta catégorie charge en 2x moins de temps".

3. **Toujours 1-3 points positifs au début.** Sinon le patron se braque dans les 5 premières secondes. Même si le site est catastrophique, trouver 1 chose ("ton menu est bien à jour", "ta photo de façade est belle").

4. **Langage patron uniquement.** Test : si la phrase contient un mot anglais (hors noms propres) ou un sigle (SEO, CMS, HTTP), la reformuler.

5. **Audit = ouvre-porte, pas devis.** Le but n'est pas de tout résoudre dans le rapport. Le but est de provoquer la phrase "et donc tu ferais quoi à ma place ?". À ce moment, on enchaîne sur la maquette gratuite.

6. **Données sensibles GMB.** Si on détecte des avis négatifs récents, NE PAS les mentionner dans le rapport (sujet vexant en face-à-face). Garder pour soi, en parler oralement si pertinent.

7. **Si le site eatbu est inaccessible** (404, timeout, redirect cassé) : c'est en soi un problème majeur à mettre en problème #1. Le patron ne le sait probablement pas.

---

## Modes

Pour la v1, **un seul mode : `default`**. Pas de mode `deep`, pas de mode `pdf`, pas de mode `email`.

Si l'utilisateur demande "audit complet" ou "audit détaillé" → répondre que ce skill produit un audit terrain compact, et que pour un audit technique approfondi il faudra un autre skill (à venir).

---

## Resources

- `references/playbook.md` : checklist des défauts typiques eatbu et formulations patron-friendly
- `templates/audit-tablette.md` : template Markdown vierge à remplir

---

## Exemple d'invocation

```
Mike : Audit eatbu : https://lavesuvio-chartres.eatbu.com — j'y vais demain à 15h.
```

Le skill exécute les 5 étapes et retourne le rapport rempli, prêt à être affiché sur tablette ou copié dans Notion/Google Docs pour la visite.
