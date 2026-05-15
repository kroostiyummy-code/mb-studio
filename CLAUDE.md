# Contexte projet — MB Studio

> Ce fichier est lu automatiquement par Claude Code à chaque session. Il contient le contexte stratégique et opérationnel pour que toute future session démarre alignée.

## Le porteur de projet

- **Mike**, foodtruckeur à Chartres (28)
- **Non-développeur** : pilote MB Studio en side-project
- Objectif : **transition foodtruck → MB Studio à temps plein** (12-18 mois)
- Vision long terme : agence locale, mais **démarre seul**

## Le projet

MB Studio = micro-agence web locale, niche **restaurants/commerce de bouche à Chartres** ayant un site eatbu.com.

Lire `README.md` pour l'offre complète et `BRAND.md` pour l'identité visuelle.

## Principes non-négociables

1. **Honnêteté radicale** : aucune fausse promesse (pas de "garantie 1ère page Google", pas de "support 24/7", pas de "modifs illimitées")
2. **Process simple** : Mike est non-dev → tout doit être pilotable sans connaissance technique avancée
3. **0€ d'hébergement par site client livré** (Astro + Cloudflare Pages)
4. **Édition autonome** par le client (Decap CMS) → c'est l'argument de vente
5. **Chaque client = ambassadeur potentiel** (footer signé, commission 100€, photo Instagram)
6. **Sous-promettre, sur-livrer** : chaque livraison contient un petit cadeau non annoncé (favicon perso, page 404 rigolote, animation discrète…) — voir `process.md` pour la liste. Promettre moins à l'oral, livrer plus à l'écran.
7. **Patron toujours propriétaire à 100%** : domaine acheté sur SON compte registrar, fiche GMB où Mike est gestionnaire (pas propriétaire), site éditable seul. Le jour où il veut partir, il garde tout sans rien transférer.
   - **Implication technique** : 1 repo Git séparé par client (jamais de mono-repo, voir Stack technique). Le bon de commande engage MB Studio à fournir au patron une archive complète de son repo sous 48h sur simple demande.
8. **Vouvoiement par défaut à l'écrit** (audit envoyé, mail, devis, support imprimé). Tutoiement possible à l'oral pendant la visite si le patron tutoie en premier.

## Stack technique imposée

- **Sites clients** : Astro + Decap CMS + Cloudflare Pages
- **Vitrine MB Studio** : même stack (cohérence)
- **1 repo Git par client** (jamais de mono-repo) — découle du principe non-négociable #7, garantit la transférabilité immédiate au patron sans extraction. Tous les repos clients vivent sous le compte GitHub MB Studio.
- **Pas de Next.js** (SSR inutile, coût Vercel imprévisible)
- **Pas de WordPress** (maintenance + sécu + hébergement payant = antagonique au pitch)

## Process opérationnel

Le process complet (5 étapes, du 1er contact au suivi mensuel) vit dans `process.md` à la racine du repo. **À lire systématiquement avant toute session liée à un client.**

Résumé : 4 visites client maximum (présentation, brief, livraison, suivi J+30), tout le reste se passe chez Mike. Pack Solo 490€ (paiement 50/50, acompte après brief). Pack Suivi mensuel optionnel 50€/mois, **jamais poussé en début de pitch**, mentionné uniquement à la fin avec emphase sur "résiliable à tout moment".

## Skills (outillage Claude Code interne)

Le repo héberge les skills MB Studio dans `skills/` au format SKILL.md (compatible Claude Code).

| Skill | Statut | Rôle |
|---|---|---|
| `audit-eatbu` | ✅ Fait | Audit gratuit pré-rempli avant visite porte-à-porte |
| `maquette-flash` | ✅ Fait | Génère les 3 maquettes (Brutaliste / Élégante / Tradition) depuis 1-4 liens publics du resto cible. Output : 3 PNG haute résolution pour la tablette, en mode "1 primaire + 2 backups". |
| `brief-client` | À construire | Questionnaire structuré pour récolter tout le contenu en 1h |
| `site-from-brief` | À construire | Génère le site Astro complet depuis le brief rempli |
| `new-client` | À construire | Automatise le scaffolding par client : création repo GitHub dédié, copie du template site-resto/, setup Cloudflare Pages, init Decap CMS, premier commit. Réduit la friction du "1 repo par client". |
| `gmb-setup` | À construire | Checklist et procédure d'optimisation de la fiche Google Business |
| `monthly-report` | À construire | Rapport mensuel : Umami + GMB Insights + PageSpeed → 1 page patron-friendly |
| `relance-patron` | À venir (plus tard) | Script de relance pour patrons ayant vu la maquette sans signer |

**Ordre de construction (validé) :**

1. **Template Astro `site-resto/`** : extraire la structure de `Kroostiyummy.fr` (site déjà fait par Mike avec Claude) et en faire le template réutilisable. C'est le socle de toute la suite.
2. **Skills de production** dans l'ordre de construction : `maquette-flash` → `brief-client` → `site-from-brief` → `new-client` → `gmb-setup` → `monthly-report`. Note : à l'exécution terrain, `new-client` tourne en amont de `site-from-brief` (on crée le repo avant de générer le site dedans), mais sa construction vient après car il automatise autour du template.
3. **Supports commerciaux** : pitch porte-à-porte, réponses aux objections, bon de commande type, carte de visite (déjà dans `process.md` mais à matérialiser)
4. **5 visites terrain** seulement quand 1-2-3 sont prêts (Mike veut arriver "lancé", pas "en train de se lancer")
5. **Vitrine MB Studio** construite avec le même template que les sites clients, avec Kroostiyummy.fr comme premier cas client. Pas avant le 3ème client signé.

**Stack de tracking installée sur chaque site client (gratuit, RGPD-friendly) :**
- Umami ou Plausible auto-hébergé sur Cloudflare (analytics sans cookie banner)
- Google Search Console (mots-clés Google)
- GMB Insights (gestion via accès gestionnaire)
- PageSpeed Insights mensuel (vitesse + Core Web Vitals)

Ces 4 sources alimentent `monthly-report` et justifient l'abonnement Suivi à 50€/mois.

## Anti-patterns à refuser

- Ajouter Next.js, React SSR, framework lourd
- Proposer WordPress
- Promettre du SEO garanti
- Ajouter des dépendances payantes (CMS payant, hébergement payant, analytics payant Google Analytics inclus)
- Parler "agence" / "équipe" / "nous" (Mike est solo, c'est sa force)
- Utiliser du jargon tech dans les supports clients
- Pousser l'abonnement Suivi mensuel en début de pitch (ça crée la peur de dépendance, ça casse la vente)
- Promettre des choses qui ne seront pas dans le bon de commande (les "cadeaux surprise" se découvrent à la livraison, ne se promettent jamais)
- Mettre un effet visuel lourd (vidéo scroll-driven, animations complexes) sur un site resto — antagonique avec "site rapide" et avec "édition autonome par le patron"

## État du projet (mai 2026)

- Stratégie figée : offre, prix, process complet (`process.md`), pitchs scriptés, packs définis
- Skill `audit-eatbu` ✅ écrit et testé en démo (Le Cochon Dingue)
- Template `templates/site-resto/` ✅ 12/12 composants codés en vrai, 3 signatures testées sur Kroosti + 2 fixtures non-Kroosti (gastro élégant + bistrot tradition). Dogfooding validé.
- Skill `maquette-flash` ✅ écrit (structure complète : SKILL.md + extraction-checklist + pitch-presentation). À tester en conditions réelles sur un premier resto cible.
- Stratégie ciblage 5 premiers clients : **Option 1 validée** = sélection manuelle par feeling terrain (accroche relationnelle + transformation visible à raconter)
- **Prochain jalon Mike** : construire le template `site-resto/` à partir de Kroostiyummy.fr, puis les 5 skills de production, AVANT toute visite terrain. Mike veut arriver "lancé".
- **Cas client zéro** : Kroostiyummy.fr (le site du foodtruck de Mike, 170 avis 5 étoiles, refait avec Claude) sert de premier cas client pour la vitrine MB Studio
- **Décisions architecture (2026-05-15)** posées en session avant le build du template :
  - 12 sections génériques validées pour `site-resto/` (voir mémoire `project-template-sections-finales`)
  - 3 signatures typo MB Studio : Brutaliste / Élégante / Tradition (voir mémoire `project-design-system-template`)
  - Sections optionnelles = composants Astro conditionnels au build, pas du CSS display:none (voir mémoire `feedback-template-architecture`)
  - 1 repo Git par client (jamais mono-repo) — confirmé conséquence directe du principe #7
- Statut juridique : à régulariser (ajout activité secondaire BIC service à la micro foodtruck) **avant 1ère facture**

## TODO bloquants avant 1er client (ne pas oublier)

- [ ] **Protocole support patron** : graver dans `process.md` une section "Support après livraison" — incidents typiques (patron casse contenu, build échoue, Cloudflare down, modif demandée), qui fait quoi, délais réalistes ("réponse dans la journée en semaine"), garantie 30j post-livraison, modifs au-delà (1 gratos/an OU Pack Suivi 50€/mois OU 50€/h). Indispensable avant de promettre quoi que ce soit oralement.
- [ ] **Fichier `incident-response.md`** à créer dans le template `site-resto/` (sera dupliqué chez chaque client). Checklist Mike-friendly : "site ne charge plus → faire ça", "patron a cassé son contenu via Decap → faire ça", "Cloudflare en panne → faire ça". À écrire en français pas-tech.
- [ ] **Skill `incident`** à construire plus tard : `/incident [URL client]` → Claude pull le repo, lit logs Cloudflare, diagnostique. Pas urgent mais utile dès le 2-3e client.
- [ ] **Decap config** à compléter pour `mode`, `horaires`, `horaires_foodtruck`, `google_maps_embed_url` avant le 1er client mode fixe qui voudrait modifier ses horaires.
- [ ] **Dogfood template hors-Kroosti** : tester avec 2-3 settings différents (gastro elegant + bistrot tradition) pour révéler bugs cachés avant d'en construire les skills par-dessus.

## Profil de Mike — ce qu'il faut garder en tête à chaque session

- **Très bon en relationnel/vente**, vit déjà du contact client direct (foodtruck à Chartres)
- **Faible en technique** par auto-évaluation, mais a déjà refait Kroostiyummy.fr avec Claude (preuve qu'il maîtrise la stack en pratique)
- Léger **syndrome de l'imposteur** : a besoin de systèmes clairs, simples, duplicables pour se sentir pro même quand il doute
- N'est **pas dev** : ne jamais lui demander de comprendre le code, lui parler en français, en bénéfices, en "ce que ça change pour le client"
- **Tutoiement entre Claude et Mike** dans les discussions internes (style direct, pair-à-pair). Le vouvoiement est réservé aux contenus destinés aux clients du resto.

## Conventions de commit

Format conventionnel court, en français, sans emoji :

```
feat(audit-eatbu): ajoute le scoring Lighthouse mobile
fix(brand): corrige hex de la couleur ocre terre cuite
docs(readme): clarifie tarifs des paliers
chore(repo): met à jour .gitignore
```

## Branche de développement

Toutes les modifications vont sur `claude/merchant-outreach-site-zUe07` jusqu'à fusion vers `main`.
