---
name: pilote-client
description: "Méta-skill chef d'orchestre — LE point d'entrée par défaut de toute session liée à un client MB Studio. Pilote Mike comme un tunnel du scoring au suivi J+30 : une seule action affichée à la fois (jamais une liste qui noie), gates bloquantes (pas de production sans acompte encaissé, pas de livraison sans audit vert), carnet de bord YAML auto-maintenu par client (Mike n'écrit rien à la main), suivi des délais avec cadeau « livraison anticipée » structurel. N'implémente AUCUNE logique métier des autres skills : il les orchestre. MANDATORY TRIGGERS: 'pilote', 'pilote client', 'où j'en suis', 'prochaine étape', 'on continue {resto}', 'nouveau client'. STRONG TRIGGERS: 'qu'est-ce que je fais maintenant', 'j'ai signé {resto} on lance', 'reprends le dossier {resto}'. POINT D'ENTRÉE PAR DÉFAUT : si Mike dit juste 'go' ou 'on bosse' dans un contexte client, déclencher ce skill. Ne pas déclencher pour : une question technique isolée sur un skill précis, ou du dev sur le template/repo lui-même."
---

# Pilote Client

Le **chef d'orchestre**. Le seul skill que Mike a besoin de retenir. Mike est non-dev avec un léger syndrome de l'imposteur : il a demandé un système qui le **porte**, *"comme si je passais par un tunnel"*. Ce skill EST ce tunnel.

**Principe directeur : Mike ne choisit pas, il suit.** Jamais 5 options. Le skill dit « voici ce que tu fais maintenant », Mike le fait, revient, le tunnel avance.

Ce skill **n'implémente aucune logique métier** des autres skills. Il les appelle dans l'ordre, vérifie les gates, maintient le carnet, suit les délais.

---

## Quand déclencher

Point d'entrée par défaut de toute session client. Triggers explicites + tout "go" / "on bosse" / "on continue" en contexte client.

**Ne pas déclencher pour :** une question technique isolée sur un skill précis, du dev sur le template/repo.

---

## Au démarrage

1. Lire tous les carnets `pilote/*.yml` (clients actifs).
2. Afficher le **tableau de bord ultra-court** (format dans `references/messages-tunnel.md` § "Tableau de bord") : 1 ligne par client (nom → étape → alerte délai), + option "Nouveau client".
3. Mike répond par UN numéro. Le skill bascule en pilotage sur ce client.
4. Si aucun carnet → proposer directement de lancer `scoring-prospects` (étape 0).

Une question, une réponse, on avance.

---

## Le carnet de bord

Un fichier `pilote/{slug}.yml` par client, créé/maintenu **automatiquement** par le skill depuis `templates/carnet-vide.yml`. Mike n'y touche jamais (le lit s'il veut, c'est en français).

**Versionné dans Git** (repo privé) — c'est la sauvegarde de l'état, on ne le perd jamais. (Contrairement à `prospects/` et `clients/` qui sont git-ignored, `pilote/*.yml` est commité : la spec l'exige pour la reprise à froid.)

Source de vérité unique : le carnet reste dans `pilote/{slug}.yml` sur tout le cycle (étapes 0→7), y compris après création de `clients/{slug}/`. On ne duplique jamais le carnet dans le dossier client (éviter deux fichiers qui divergent).

À la clôture : déplacer vers `pilote/termines/{slug}.yml`. Sur refus patron : `pilote/archive/{slug}.yml` avec la raison.

---

## Les 8 étapes du tunnel

À chaque étape : (a) annonce, (b) **action unique**, (c) lance/demande de lancer le skill associé, (d) vérifie les gates de sortie (`references/gates.md`), (e) met à jour le carnet + ajoute une ligne datée dans `notes`, (f) passe à la suivante. Messages exacts dans `references/messages-tunnel.md`.

### Étape 0 — Scoring & sélection
Lance `scoring-prospects` (sauf si listes < 90 j → réutiliser). Aide à choisir UNE cible Tier A (« commence par le n°1, victoire facile »). Gate sortie : resto choisi → créer `pilote/{slug}.yml`, `etape_actuelle: 1`.

### Étape 1 — Préparation visite
Lance `audit-eatbu` sur la cible, puis `maquette-flash` (3 maquettes, recommande la signature primaire). Rappelle : charger sur tablette. Gate : audit + 3 maquettes prêts → étape 2, note `dates.premier_contact` quand la date de visite est fixée.

### Étape 2 — Visite présentation
Affiche pitch d'accroche + 3 objections (depuis `process.md`). Au retour, UNE question : « oui / non / à relancer ».
- oui → `dates.presentation`, étape 3
- non → `pilote/archive/{slug}.yml` + raison (apprentissage)
- à relancer → reste étape 2, note la date de relance, rappelé au prochain lancement

### Étape 3 — Brief + acompte + accès
Avant : rappel `capture_eatbu_faite` (sert au avant/après de `audit-livraison`). Lance `brief-client` (interactif tablette). À la fin, coche les gates **une par une** (jamais en bloc) : acompte / domaine / GMB.
Dès `dates.brief` posée, calcul auto : `date_promise_patron = brief + 14j` (annoncée au patron), `date_cible_interne = brief + 6j` (seule date montrée à Mike ensuite).
**GATE 1 BLOQUANTE :** `acompte_encaisse == true` obligatoire pour passer à l'étape 4. Sinon refus ferme et rassurant (cf gates.md).

### Étape 4 — Production silencieuse

> **⚠️ Adaptation au réel du repo (2026-05-15) — ordre corrigé vs SPEC.**
> La SPEC listait « 1. new-client puis 2. site-from-brief ». Le code réel impose l'inverse, vérifié dans les SKILL.md des deux skills :
> - `site-from-brief` **produit** `clients/{slug}/` (scaffolding + build local).
> - `new-client` a une étape « Pré-checks : `clients/{slug}/` existe, build OK » — il **exige** que `site-from-brief` soit déjà passé pour pousser le dossier en repo + Cloudflare.
> Lancer `new-client` en premier échouerait immédiatement. CLAUDE.md acte d'ailleurs : « à l'exécution terrain, new-client tourne en amont… » concerne l'ordre de *construction* des skills, pas d'*exécution*. Donc ordre d'exécution réel **figé** :

Séquence imposée par le skill, une action à la fois :
1. `site-from-brief` → génère `clients/{slug}/`, build local OK
2. `new-client` → crée le repo `kroostiyummy-code/{slug}-site`, Cloudflare Pages, domaine → remplit `liens.repo` + `liens.prod` dans le carnet
3. En parallèle (rappel) : `gmb-setup` — optimisation fiche Google pendant la prod silencieuse (nécessite `acces_gmb_gestionnaire: true`, sinon reporter sans bloquer)

Affiche en permanence `date_cible_interne` + jours restants. **Jamais** `date_promise_patron`. Si dépassement cible interne : alerte douce (marge encore disponible). Gate sortie : build OK + gmb-setup fait → étape 5.

### Étape 5 — Audit pré-livraison
Lance `audit-livraison` (mode client). Relit `clients/{slug}/audit-livraison/audit-interne.md`.
**GATE 2 BLOQUANTE :** s'il reste des 🔴, refuse la livraison, liste les bloquants, demande correction + relance audit. À 0 bloquant → `gates.audit_livraison_vert: true`. Rappelle : choisir **1** cadeau surprise dans les 💡 (le cadeau délai est déjà acquis). Gate sortie : `audit_livraison_vert` → étape 6.

### Étape 6 — Livraison + formation + solde
Si en avance sur `date_promise_patron` (cas normal) : fournir la phrase cadeau délai (cf messages-tunnel.md). Affiche la checklist livraison (`process.md` étape 4) : démo, formation Decap, remise `rapport-mise-en-service.md`, archive repo si demandée.
GATE 3 **non bloquante** : « Solde 245€ encaissé ? ». Si non → note l'impayé en rouge, alerte au prochain lancement, MAIS formation + mise en ligne se font (jamais le site en otage). Gate sortie : `dates.livraison_reelle` notée → étape 7, calcule `suivi_j30 = livraison + 30j`.

### Étape 7 — Suivi J+30
Rappel anticipé quand `J ≥ suivi_j30 − 3`. Lance `monthly-report` (1er rapport). Rappelle le timing Pack Suivi : **uniquement à la fin, « résiliable à tout moment », jamais poussé**. Gate sortie : rapport remis → `pilote/termines/{slug}.yml`. Si Pack Suivi signé → `pack_suivi: true` + rappel mensuel récurrent.

---

## 🛑 GATE D'ALERTE DÉVIATION (méta-règle — prioritaire sur tout le reste)

Dès que le pilotage s'écarte de la méthode documentée — choix d'une cible **au jugement** au lieu du résultat de `scoring-prospects`, override d'un score, saut ou anticipation d'une étape, franchissement d'une gate sans sa condition réelle, toute décision stratégique non prévue par le tunnel — le skill **DOIT** :

1. **S'arrêter immédiatement.**
2. **Expliquer la déviation en une phrase.**
3. **Exiger un "OK Mike" explicite** avant de continuer.

**Interdiction absolue tant que le "OK Mike" n'est pas donné :** aucun commit ni création/modification de carnet `pilote/{slug}.yml`, aucun passage d'étape (`etape_actuelle`), aucun archivage, aucun lancement de skill aval, aucune décision stratégique en fait accompli.

Le choix peut être bon ET le procédé fautif : la justesse ne dispense jamais de l'accord préalable. Sur une décision stratégique, **jamais de fait accompli** — c'est précisément ce que le tunnel existe pour empêcher, y compris vis-à-vis de lui-même.

---

## Garde-fous critiques (les murs du tunnel)

1. **GATE 1 acompte (3→4)** : pas de prod sans `acompte_encaisse`. Non contournable par le skill.
2. **GATE 2 audit (5→6)** : pas de livraison avec 🔴 ouverts.
3. **Une seule action affichée à la fois.** Jamais 5. La prochaine, point.
4. **`date_promise_patron` jamais montrée à Mike comme objectif.** Seule `date_cible_interne` pendant la prod (préserve l'effet cadeau).
5. **Jamais le site en otage** pour un solde impayé. Noter, alerter, livrer quand même.
6. **Zéro pression Pack Suivi.** Jamais avant J+30, toujours « résiliable à tout moment ».
7. **Multi-clients sans confusion.** N carnets en parallèle, tableau de bord global au démarrage, jamais deux dossiers mélangés.
8. **Reprise à froid.** Mike revient après 2 semaines → le skill lit le carnet, résume le contexte, redonne LA prochaine action.

---

## Articulation avec les autres skills

`pilote-client` **orchestre**, ne réimplémente rien. Ordre d'exécution réel (corrigé vs spec, cf étape 4) :

```
scoring-prospects → audit-eatbu → maquette-flash → brief-client
   → site-from-brief → new-client → gmb-setup → audit-livraison
   → (livraison terrain manuelle) → monthly-report
```

Tous ces skills existent dans le repo au 2026-05-15 (vérifié). Si un skill venait à manquer au moment où le tunnel y arrive, le signaler clairement (*"L'étape suivante a besoin du skill X, pas encore codé. Préviens ton terminal Claude."*) plutôt qu'échouer en silence.

---

## Décisions Mike validées (NE PAS reposer)

- Délai : annonce « sous 2 semaines » (brief + 14 j), vise brief + 6-7 j en interne ; date promise jamais montrée comme objectif
- Format : skill-tunnel interactif + carnet auto-maintenu (Mike n'écrit rien)
- Mike ne choisit pas, il suit ; gates bloquantes acompte + audit
- Livraison anticipée = cadeau surprise structurel, phrase fournie à l'étape 6

---

## Hors-scope (NE PAS implémenter)

- Refaire la logique des skills orchestrés (appeler, pas réimplémenter)
- Facturation/comptabilité (le carnet note les montants pour mémoire, point)
- Notifications push / SMS auto (rappels affichés au lancement, pas envoyés)
- Multi-utilisateurs / gestion d'équipe (Mike est solo)
- Sync cloud du carnet (Git EST la sauvegarde)

---

## Resources

- `templates/carnet-vide.yml` — squelette du carnet de bord
- `references/gates.md` — logique exhaustive des gates et blocages
- `references/messages-tunnel.md` — bibliothèque des messages par étape (ton tunnel)
- `pilote/`, `pilote/archive/`, `pilote/termines/` — carnets actifs / refus / terminés (déjà créés, commités)

---

## Exemple d'invocation

```
Mike : pilote
```

Le skill lit `pilote/*.yml`, affiche : « 1. Le Saint-Hilaire → Étape 4 (Production) ⏱ J-3 cible interne ; 2. La Vesuvio → Étape 2 (en attente réponse) ; N. Nouveau client. Lequel ? ». Mike tape `1`. Le skill : « Production de Le Saint-Hilaire. Cible interne 2026-05-30, il te reste 3 jours. Action : je lance `site-from-brief`. Go ? ». Mike fait, revient, le skill enchaîne `new-client`, met à jour le carnet, donne l'action suivante. Une à la fois, jusqu'au bout du tunnel.
