# Que faire quand le patron m'appelle paniqué

> Fichier dupliqué dans chaque repo client. Ouvert quand le patron envoie un SMS ou appelle parce que "le site marche plus" ou "j'ai cassé un truc". Lecture cible : 30 secondes pour savoir quoi faire.

---

## D'abord : respirer 10 secondes

Aucun incident sur un site Astro + Cloudflare Pages n'est dramatique. Le code est versionné dans Git, l'historique de Decap est dans Git aussi, Cloudflare reconstruit le site à chaque push. **Rien n'est perdu, même quand le patron a "tout cassé".**

Avant de répondre au patron, lire l'incident correspondant ci-dessous. Répondre **dans la journée en semaine** (engagement de support), pas dans la seconde.

---

## Cas 1 — "Le site ne charge plus"

### Symptôme
Le patron tape son domaine, page blanche / erreur 404 / "site introuvable".

### Diagnostic en 30 secondes

1. Ouvrir le domaine du patron dans le navigateur (vérifier que je vois la même chose)
2. Aller sur `https://www.cloudflarestatus.com/` → est-ce qu'il y a une panne globale Cloudflare ?
3. Aller sur `https://dash.cloudflare.com/` → ouvrir le projet Pages du patron → onglet "Deployments" → est-ce que le dernier déploiement est en "Success" ou "Failed" ?
4. Aller sur le compte OVH/Gandi du patron (le patron a les identifiants) → vérifier que le domaine n'a pas expiré

### Action immédiate selon la cause

| Cause détectée | Action |
|---|---|
| Cloudflare panne globale | SMS au patron : "Cloudflare a une panne, ça remontera dans 1-2h. Je suis le statut." |
| Dernier déploiement Failed | Lire les logs sur Cloudflare Pages → identifier l'erreur de build → faire un `git revert` du dernier commit qui casse → push → Cloudflare rebuilde |
| Domaine expiré | SMS au patron : "Votre domaine n'a plus été renouvelé, c'est sur votre compte OVH/Gandi. Vous me le faites maintenant et le site revient en 1-2h ?" |
| Aucune cause évidente | Vérifier les DNS Cloudflare (Records → CNAME). Si tout est OK, contacter le support Cloudflare via le dash |

### Quand prévenir le patron
- Si l'incident dépasse **1h** sans cause identifiée → SMS au patron avec mise à jour
- Si causé par un de mes pushes récents → SMS d'excuse + ETA correction

---

## Cas 2 — "J'ai cassé quelque chose dans Decap"

### Symptôme
Le patron a édité un truc via `/admin/`, et maintenant le site affiche n'importe quoi ou refuse de charger une section.

### Diagnostic en 30 secondes

1. Cloner le repo client en local (`git clone` si pas déjà fait) ou `git pull` si déjà cloné
2. Vérifier l'historique : `git log --oneline -5` → identifier le dernier commit fait par Decap (commits avec message type "Update settings" ou similaire)
3. Faire `git diff HEAD~1` (ou plus loin si besoin) → comprendre ce que le patron a changé

### Action immédiate selon le cas

| Type d'erreur Decap | Action |
|---|---|
| Champ obligatoire vidé | `git revert <commit>` → push → site revient à l'état d'avant + SMS au patron : "Je l'ai remis, dans Decap allez sur [champ] et ne le laissez pas vide la prochaine fois" |
| Mauvais format de date/heure (`12h00` au lieu de `12:00`) | Éditer le fichier YAML à la main → corriger le format → commit + push + SMS pédagogique |
| Image trop lourde uploadée | Vérifier dans `public/images/` → si > 5 Mo, redimensionner + recommit + SMS : "L'image était trop grosse, je l'ai réduite. À l'avenir, redimensionnez vos photos vers 1200px de large avant d'uploader" |
| Modification YAML qui casse le schema Astro | Le build a échoué (cf Cas 1) → `git revert` |

### Quand passer au SMS pédagogique
Après chaque correction de cas 2, **toujours expliquer en 1 phrase** ce qui s'est passé. Le patron apprend, refait moins l'erreur. Ne JAMAIS dire "c'est pas grave, vous pouvez tout casser" — c'est faux et ça crée des incidents en série.

---

## Cas 3 — "Je veux rajouter [nouvelle chose]"

### Symptôme
Le patron veut une nouvelle section, un nouveau plat, une nouvelle photo de fond, etc.

### Diagnostic
**Pas un incident.** C'est une demande d'évolution.

### Action immédiate

1. Vérifier si c'est dans **la 1 modification gratuite annuelle** (incluse Pack Solo) :
   - Modification "simple" = changer un texte / ajouter 1-2 photos / activer une section optionnelle déjà prévue → OUI, dans la gratuité
   - Modification "structurelle" = nouvelle section sur-mesure / refonte / nouvelle fonctionnalité → NON, devis

2. Réponse au patron :
   - **Si gratos** : "Dans le Pack Solo vous avez 1 modification gratuite par an, je peux faire ça. Je vous la livre dans 7 jours."
   - **Si à devis** : "C'est une évolution hors-Pack. Je peux vous chiffrer ça en 24h. Avant, vous voulez voir aussi le Pack Suivi mensuel à 50€ où les modifications sont incluses ?"

3. Si Pack Suivi pertinent, mentionner ouvertement sans pousser.

### Ne jamais dire
- "Oui pas de souci je vous fais ça gratuitement" sans avoir vérifié la limite annuelle
- "C'est pas dans le contrat" (formulation froide qui braque le patron)

---

## Cas 4 — "Le site est lent" / "Google ne me remonte plus dans les résultats"

### Symptôme
Le patron a vu que son site charge en X secondes ou qu'il a perdu son classement Google.

### Diagnostic
**Pas un incident technique** dans 90% des cas. Plutôt une attente déçue ou un problème externe.

### Action immédiate

1. Tester le site sur `https://pagespeed.web.dev/` avec son URL :
   - Score > 90 → "Votre site charge en X secondes, c'est dans les meilleurs scores possibles. Je vous envoie le rapport."
   - Score 60-90 → identifier la cause (image trop lourde ? police bloquante ?) → corriger si dans la garantie 30j ou expliquer le tradeoff
   - Score < 60 → bug technique, à corriger sans frais

2. Pour le classement Google :
   - Vérifier la fiche GMB du patron → est-ce qu'elle est complète, avec photos récentes, posts récents ?
   - Vérifier la position dans Google Search Console (lié au compte Mike)
   - Expliquer au patron : "Le SEO ça dépend de votre fiche Google + vos avis + la concurrence locale, pas que du site. Je peux faire un audit complet via le Pack Suivi mensuel."

---

## Cas 5 — "Je veux récupérer mon site, je change de prestataire"

### Symptôme
Le patron veut partir.

### Action immédiate

**Aucune discussion, aucune négociation.** C'est l'engagement contractuel principe non-négociable #7 du CLAUDE.md MB Studio.

1. Sous 48h, ajouter le patron comme collaborateur sur le repo GitHub `kroostiyummy-code/{client-slug}` (Settings → Collaborators → Add people)
2. Lui envoyer un mail récapitulatif avec :
   - L'URL du repo GitHub
   - L'URL du panneau Cloudflare Pages (lui transférer la propriété en lui faisant créer un compte Cloudflare puis Settings → Members → Add member → Owner)
   - L'URL de la fiche GMB (lui retirer mon accès gestionnaire via business.google.com → Personnes)
   - Une dernière phrase : "Si vous avez besoin de quoi que ce soit pour la transition, je reste disponible. Et merci de m'avoir fait confiance."

3. Noter dans mon carnet : pourquoi il part. C'est un apprentissage précieux.

**Ne jamais** :
- Faire payer une "pénalité de sortie"
- Bloquer l'accès le temps de "discuter"
- Critiquer son nouveau prestataire
- Lui faire sentir qu'il fait une erreur

---

## Numéros utiles à avoir sous la main

- **Support Cloudflare** : via le dash `https://dash.cloudflare.com/` → bouton "Support" en bas à droite (chat ou ticket)
- **Support OVH** : 1007 (depuis France) ou via espace client
- **Support Gandi** : `support@gandi.net` ou via espace client
- **Status Cloudflare** : `https://www.cloudflarestatus.com/`
- **Status GitHub** (au cas où le repo serait inaccessible) : `https://www.githubstatus.com/`

---

## Quand TOUT a échoué et que je suis paniqué

Si je tombe sur un cas que je ne comprends pas du tout :

1. **Prendre 1 heure de pause**. Aucun incident sur un site Astro n'est résolu plus vite par la panique.
2. Ouvrir Claude Code dans le repo client : `cd ~/clients/{slug}` puis `claude` → décrire le problème en français, Claude diagnostique.
3. Si Claude ne sait pas : **dernier recours**, faire un revert du dernier commit Decap et un push manuel d'une version stable connue. Le site revient à l'état d'avant. On comprendra plus tard.

**Le site du patron est toujours réparable.** C'est le calme avec lequel je gère qui fait la différence sur la relation, pas la vitesse.
