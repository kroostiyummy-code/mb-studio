# Contexte projet — MB Studio

> Ce fichier est lu automatiquement par Claude Code à chaque session. Il contient le contexte stratégique et opérationnel pour que toute future session démarre alignée.

## Le porteur de projet

- **Mike**, foodtruckeur à Chartres (28)
- **Non-développeur** : pilote MB Studio en side-project
- Objectif : **transition foodtruck → MB Studio à temps plein** (12-18 mois)
- Vision long terme : agence locale, mais **démarre seul**

## Le projet

MB Studio = micro-agence web locale, niche **restaurants/commerce de bouche à Chartres** ayant un site eatbu.com.

Lire `README.md` pour l'offre complète et `BRAND.md` pour l'identité visuelle. Les idées stratégiques en cours de réflexion (non décidées) vivent dans `idees-roadmap.md` — y aller chercher la mémoire des pistes brainstormées.

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
| `brief-client` | ✅ Fait | Questionnaire interactif en 12 sujets pour le brief en 1h chez le patron. Output : `briefs/{slug}/brief.md` narratif + `briefs/{slug}/settings.yml` prêt pour `site-from-brief`. |
| `site-from-brief` | ✅ Fait | Transforme `briefs/{slug}/` en `clients/{slug}/` : scaffolding template, injection settings, génération menu, optimisation photos, personnalisation README et incident-response, test build local. Prêt à pousser via `new-client`. |
| `new-client` | ✅ Fait | Ferme la boucle de production : crée repo GitHub `kroostiyummy-code/{slug}-site` (auto via gh CLI ou API ou fallback manuel), push initial, connecte Cloudflare Pages, configure le domaine custom. Output : site en ligne sur `https://{domaine}.fr` + admin Decap fonctionnel. |
| `audit-livraison` | Spec écrite (`skills/audit-livraison/SPEC.md`) | Audit du site juste avant livraison. Produit 2 outputs : audit interne brut (Mike-only) + rapport de mise en service valorisant (patron). Compare le nouveau site au snapshot eatbu archivé pendant le brief et à une moyenne sectorielle anonyme. À coder par le terminal Claude. |
| `gmb-setup` | ✅ Fait | Optimisation fiche Google Business pendant la production silencieuse (étape 3bis). 9 étapes : audit avant, catégorie+secondaires, description 750 char, 12+ photos, horaires précis, attributs, FAQ pré-publiée, 1er post hebdo, réponses à tous avis non-répondus. Output : captures avant/après + rapport pour livraison + planning posts hebdo. |
| `monthly-report` | ✅ Fait | Génère le rapport mensuel patron (1 page A4) en agrégeant 4 sources (Umami + GMB Insights + Search Console + PageSpeed). Étape 5 du process (J+30) puis récurrent pour Pack Suivi 50€/mois. 2 actions concrètes recommandées par rapport. Justifie l'abonnement. |
| `scoring-prospects` | Spec écrite (`skills/scoring-prospects/SPEC.md`) — **priorité 1** | Génère 3 listes triées (avec site eatbu / avec site autre / sans site) de prospects chartrains à démarcher, scoring 0-100 + tier A/B/C combinant "valeur apportée" et "probabilité d'accepter". Output : fiches markdown avec top 3 arguments à pitcher + CSV récap. Source : Overpass OSM + PageSpeed API + Wayback Machine. À coder par le terminal Claude AVANT audit-livraison. |
| `pilote-client` | Spec écrite (`skills/pilote-client/SPEC.md`) — **point d'entrée central** | Méta-skill chef d'orchestre. Pilote Mike comme un tunnel du scoring au suivi J+30 : une seule action affichée à la fois, gates bloquantes (pas de prod sans acompte, pas de livraison sans audit vert), carnet de bord auto-maintenu par client, suivi des délais avec cadeau "livraison anticipée" structurel. Orchestre tous les autres skills sans réimplémenter leur logique. |
| `relance-patron` | À venir (plus tard) | Script de relance pour patrons ayant vu la maquette sans signer |

**Ordre de construction (validé) :**

1. **Template Astro `site-resto/`** : extraire la structure de `Kroostiyummy.fr` (site déjà fait par Mike avec Claude) et en faire le template réutilisable. C'est le socle de toute la suite.
2. **Skills de production** dans l'ordre de construction : `maquette-flash` → `brief-client` → `site-from-brief` → `new-client` → `gmb-setup` → `monthly-report`. Note : à l'exécution terrain, `new-client` tourne en amont de `site-from-brief` (on crée le repo avant de générer le site dedans), mais sa construction vient après car il automatise autour du template.
3. **Supports commerciaux** : pitch porte-à-porte, réponses aux objections, bon de commande type, carte de visite (déjà dans `process.md` mais à matérialiser)
4. **`scoring-prospects`** (priorité 1 ajoutée 2026-05-15) : génère la liste triée des cibles avant la 1ère visite terrain. Maximise le taux de conversion sur les 5 premières signatures.
5. **`pilote-client`** (point d'entrée central ajouté 2026-05-15) : méta-skill tunnel qui orchestre tout le reste. À coder en dernier (il appelle tous les autres), mais c'est LE skill que Mike lancera au quotidien — il ne retient que celui-là.
6. **5 visites terrain** seulement quand 1-2-3-4-5 sont prêts (Mike veut arriver "lancé", pas "en train de se lancer")
7. **Vitrine MB Studio** construite avec le même template que les sites clients, avec Kroostiyummy.fr comme premier cas client. Pas avant le 3ème client signé.

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

## Exception scraping prospection (datée — À RÉEXAMINER)

> **Décision owner explicite — Mike, 2026-05-16.** Déroge ponctuellement au garde-fou
> #4 de `scoring-prospects/SKILL.md` (« pas de scraping Google Maps/GMB »).

**Ce qui est autorisé, strictement borné :**
- Récupération de la **note Google + du nombre d'avis** (scraping léger inclus) d'un
  resto, **uniquement** pour le scoring interne des prospects.
- **Phase de DÉMARRAGE uniquement** (constitution de la première liste de cibles).
- **Données professionnelles publiques B2B** (établissement, pas personne physique).
- Périmètre `scoring-prospects` only, niche restos agglo chartraine only.

**Ce qui reste interdit (inchangé) :**
- Publication ou diffusion de ces données hors du repo privé MB Studio.
- `prospects/` reste LOCAL, jamais commité (garde-fou #7).
- Aucun emailing/cold outreach automatisé — visites en personne uniquement.
- Aucun scraping d'autres secteurs / régions / d'autres plateformes que le strict besoin.

**Risques connus et assumés (notés ce 2026-05-16) :**
- **Conditions Google** : le scraping de la recherche/Maps Google est contraire à ses
  CGU ; risque de blocage IP / captcha. Usage maintenu volontairement faible et lent.
- **Fragilité technique** : dépend du DOM Google (peut changer, geler — cf incident
  du matin du 2026-05-16) ; le skill doit dégrader proprement (« non mesuré »), jamais
  inventer un chiffre.
- **RGPD B2B** : pour chaque donnée collectée, enregistrer **source + date de
  collecte** ; respecter un **opt-out** ; pas de conservation au-delà du besoin
  prospection ; jamais de revente/partage.

**Statut : RÈGLE À RÉEXAMINER** au 1er client signé ou au plus tard 2026-08-16
(3 mois), pour décider : on arrête, on restreint, ou on pérennise.

## État du projet (mai 2026)

- Stratégie figée : offre, prix, process complet (`process.md`), pitchs scriptés, packs définis
- Skill `audit-eatbu` ✅ écrit et testé en démo (Le Cochon Dingue)
- Template `templates/site-resto/` ✅ 12/12 composants codés en vrai, 3 signatures testées sur Kroosti + 2 fixtures non-Kroosti (gastro élégant + bistrot tradition). Dogfooding validé.
- Skill `maquette-flash` ✅ écrit (structure complète : SKILL.md + extraction-checklist + pitch-presentation). À tester en conditions réelles sur un premier resto cible.
- Skill `brief-client` ✅ écrit (SKILL.md + references/questionnaire (12 sujets détaillés) + templates/brief-vide.md + templates/settings-from-brief.yml). Mode interactif Claude pose les questions, Mike entre les réponses, sortie = brief.md + settings.yml.
- Skill `site-from-brief` ✅ écrit (SKILL.md + 3 references : menu-from-brief, images-optimization, pre-deploy-checks). Transforme un brief signé en site Astro complet (8 étapes : vérif acompte, scaffolding, injection settings, génération menu, optimisation photos, personnalisation README/incident-response, test build local, récap).
- Skill `new-client` ✅ écrit (SKILL.md). Ferme la boucle production : repo GitHub privé sous kroostiyummy-code + push initial + Cloudflare Pages + domaine custom + SMS DNS au patron. 3 options de création repo (gh CLI / API / manuel) selon setup Mike.
- Skill `gmb-setup` ✅ écrit (SKILL.md + references/post-templates.md). 9 étapes pour transformer une fiche GMB pauvre en fiche pro (catégories, description SEO, photos, attributs, FAQ, posts, réponses avis). Tourne en parallèle de site-from-brief pendant la prod silencieuse.
- Skill `monthly-report` ✅ écrit (SKILL.md + templates/rapport-mensuel.md.tpl). Génère le rapport mensuel 1 page A4 en agrégeant Umami + GMB Insights + Search Console + PageSpeed. 2 actions concrètes par rapport, format imprimable, prépare le café mensuel avec opportunité Pack Suivi. **Les 6 skills de production sont désormais complets.**
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

- [x] ~~**Protocole support patron**~~ ✅ Fait. Section "Étape 6 — Support après livraison" gravée dans `process.md` : cadre temporel (garantie 30j), engagements de délais (semaine/weekend), 5 cas typiques d'incidents avec qui fait quoi, garanties/anti-promesses pour le bon de commande, outils support à mettre en place, phrase à donner au patron à la livraison.
- [x] ~~**Fichier `incident-response.md`**~~ ✅ Fait. Créé à la racine du template `site-resto/incident-response.md` (sera dupliqué chez chaque client). Checklist Mike-friendly en français pas-tech, 5 cas typiques alignés sur le protocole support, numéros utiles, procédure "quand tout a échoué".
- [ ] **Skill `incident`** à construire plus tard : `/incident [URL client]` → Claude pull le repo, lit logs Cloudflare, diagnostique. Pas urgent mais utile dès le 2-3e client.
- [x] ~~**Decap config**~~ ✅ Fait. Champs `mode`, `google_maps_embed_url`, `horaires` (mode fixe), `horaires_foodtruck` (mode foodtruck) exposés au patron avec widgets select + list imbriqués + hints clairs.
- [x] ~~Dogfood template hors-Kroosti~~ ✅ Fait (gastro elegant + bistrot tradition validés).

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
