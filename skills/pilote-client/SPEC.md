# Spec — Skill `pilote-client`

> Document de spécification destiné au Claude qui codera ce skill (en local terminal). Spec co-écrite avec Mike en session cloud le 2026-05-15.

---

## Pourquoi ce skill existe

Mike est non-dev, avec un léger syndrome de l'imposteur. Il a besoin d'un système qui le **porte**, pas d'un document à lire. Il l'a dit lui-même : *"j'aurais préféré que ce soit automatisé pour que je n'aie limite pas le choix, comme si je passais par un tunnel"*.

`pilote-client` est le **chef d'orchestre** de toute la production. C'est le seul skill que Mike a besoin de retenir. À chaque lancement, il :
- Regarde où en est chaque client
- Dit **la seule prochaine action** à faire (jamais une liste qui noie)
- Lance le bon skill au bon moment
- **Bloque la progression** tant qu'une étape critique n'est pas validée
- Maintient automatiquement un carnet de bord par client (Mike n'écrit rien à la main)
- Suit les délais et protège la promesse "livré en avance"

**Principe directeur : Mike ne choisit pas, il suit le tunnel.** Le skill ne présente jamais 5 options. Il dit "voici ce que tu fais maintenant", Mike le fait, il revient, le skill avance.

---

## Triggers

**MANDATORY TRIGGERS :**
- "pilote"
- "pilote client"
- "où j'en suis"
- "prochaine étape"
- "on continue {nom resto}"
- "nouveau client"

**STRONG TRIGGERS (avec contexte) :**
- "qu'est-ce que je fais maintenant"
- "j'ai signé {resto}, on lance"
- "reprends le dossier {resto}"

Ce skill est le **point d'entrée par défaut** de toute session liée à un client. Si Mike dit juste "go" ou "on bosse", déclencher `pilote-client`.

---

## Au démarrage

Le skill lit tous les carnets de bord existants dans `pilote/` et présente un **tableau de bord ultra-court** :

```
Tes clients en cours :

  1. Le Saint-Hilaire   → Étape 4 (Production)   ⏱ J-3 avant cible interne
  2. La Vesuvio         → Étape 2 (Présentation faite, en attente réponse)
  3. Le Comptoir        → Étape 6 (Livraison prévue demain)

  N. Nouveau client (lancer le scoring ou démarrer un resto repéré)

Lequel on traite ?
```

Mike répond par un numéro. Le skill bascule en mode pilotage sur ce client. **Une seule question, une seule réponse, on avance.**

Si aucun client en cours → proposer directement "On lance le scoring des prospects ? (étape 0)".

---

## Le carnet de bord (état persistant, auto-maintenu)

Un fichier YAML par client : `pilote/{slug}.yml`. Créé et mis à jour **automatiquement par le skill**. Mike n'y touche jamais à la main (mais peut le lire, c'est en français clair).

```yaml
slug: le-saint-hilaire
nom_resto: "Le Saint-Hilaire"
etape_actuelle: 4              # 0 à 7
sous_etape: "site-from-brief en cours"
signature_retenue: tradition

dates:
  premier_contact: 2026-05-20
  presentation: 2026-05-22
  brief: 2026-05-24
  date_promise_patron: 2026-06-07     # brief + 14j (annoncé "sous 2 semaines")
  date_cible_interne: 2026-05-30      # brief + 6j (ce que Mike vise vraiment)
  livraison_reelle: null
  suivi_j30: null

gates:
  acompte_encaisse: true              # 245€
  domaine_achete_compte_patron: true
  acces_gmb_gestionnaire: true
  capture_eatbu_faite: true
  audit_livraison_vert: false         # bloque l'étape 6
  solde_encaisse: false               # 245€

montants:
  acompte: 245
  solde: 245
  domaine_rembourse: 12

liens:
  eatbu_origine: "https://eatbu.com/..."
  repo: null
  prod: null
  gmb: "https://business.google.com/..."

notes:
  - "2026-05-22 : patron a choisi signature Tradition, aime le bordeaux"
  - "2026-05-24 : brief OK, photos transférées, manque le menu desserts (à relancer)"
```

**Avant que le dossier `clients/{slug}/` existe** (étapes 0-3), le carnet vit dans `pilote/{slug}.yml`. **Après création du repo client** (étape 4), le skill peut soit garder dans `pilote/` soit copier dans `clients/{slug}/pilote.yml` — au choix de l'implémenteur, mais une seule source de vérité (pas deux fichiers qui divergent).

---

## Les 8 étapes du tunnel

À chaque étape, le skill : (a) annonce l'étape, (b) donne **l'action unique**, (c) lance ou demande de lancer le skill associé, (d) vérifie les gates de sortie, (e) met à jour le carnet, (f) passe à la suivante.

### Étape 0 — Scoring & sélection de la cible

- **Action :** lancer `scoring-prospects` (si pas déjà fait dans les 90 derniers jours, sinon réutiliser les listes).
- Le skill aide Mike à choisir UNE cible dans le tier A : "Commence par le n°1 de `prospects-avec-site-eatbu.md`. Pourquoi lui : {top 3 arguments}. C'est ta cible la plus facile."
- **Gate de sortie :** Mike a choisi un resto → créer `pilote/{slug}.yml`, `etape_actuelle: 1`.

### Étape 1 — Préparation de la visite (chez Mike)

- **Action :** lancer `audit-eatbu` sur le resto cible, puis `maquette-flash` (3 maquettes).
- Le skill rappelle : imprimer/charger sur tablette l'audit + les 3 maquettes.
- **Gate de sortie :** audit + 3 maquettes prêtes → `etape_actuelle: 2`, noter `dates.premier_contact` quand Mike confirme la date de visite.

### Étape 2 — Visite présentation (terrain)

- **Action :** le skill affiche le pitch d'accroche (30s) depuis `process.md` + les réponses aux 3 objections les plus probables. Mike y va.
- Au retour, le skill demande : **"Le patron a dit oui pour le brief ? (oui / non / à relancer)"**
  - **oui** → `dates.presentation` notée, `etape_actuelle: 3`
  - **non** → carnet archivé en `pilote/archive/`, note la raison (alimente l'apprentissage)
  - **à relancer** → reste étape 2, note la date de relance, le skill le rappellera au prochain lancement
- **Gate de sortie :** réponse positive du patron.

### Étape 3 — Brief + acompte + accès (terrain)

- **Rappel automatique AVANT la visite :** "As-tu fait la capture eatbu ? (étape 0 de brief-client). Si non, fais-la maintenant, ça ne prend pas 30s." → gate `capture_eatbu_faite`.
- **Action :** lancer `brief-client` (mode interactif, sur tablette chez le patron).
- À la fin du brief, le skill coche les gates une par une en posant la question à Mike :
  - "Acompte 245€ encaissé ? (oui/non)" → `gates.acompte_encaisse`
  - "Domaine acheté sur le compte du patron ? (oui/non)" → `gates.domaine_achete_compte_patron`
  - "Tu es gestionnaire GMB ? (oui/non)" → `gates.acces_gmb_gestionnaire`
- **Calcul automatique des délais :** dès que `dates.brief` est posée, le skill calcule :
  - `date_promise_patron = brief + 14j` → **c'est la date que Mike annonce au patron** ("votre site sera prêt sous 2 semaines, je vous préviens dès qu'il est en ligne")
  - `date_cible_interne = brief + 6j` → **c'est la seule date que le skill montrera à Mike ensuite**
- **GATE BLOQUANTE :** `acompte_encaisse` DOIT être `true` pour passer à l'étape 4. Si non → le skill refuse d'avancer : *"Pas de production tant que l'acompte n'est pas encaissé. C'est non négociable, c'est ce qui te protège. Relance le patron."*

### Étape 4 — Production silencieuse (chez Mike)

- **Action séquencée par le skill, dans l'ordre :**
  1. Lancer `new-client` (crée le repo GitHub `{slug}-site`, Cloudflare Pages, domaine) → remplit `liens.repo`, `liens.prod`
  2. Lancer `site-from-brief` (transforme le brief en site Astro) 
  3. **En parallèle**, rappeler : lancer `gmb-setup` (optimisation fiche Google pendant la prod silencieuse)
- Le skill affiche en permanence : **"Cible interne : {date_cible_interne} — il te reste {N} jours."** Jamais la date promise (pour garder le réflexe d'avance).
- Si `J > date_cible_interne` : le skill alerte doucement *"Tu es passé ta cible interne. Pas de panique, tu as encore {marge} jours avant la date promise au patron. Mais accélère."*
- **Gate de sortie :** build local OK + `gmb-setup` fait → `etape_actuelle: 5`.

### Étape 5 — Audit pré-livraison (chez Mike)

- **Action :** lancer `audit-livraison` (mode client).
- Le skill lit le résultat. **GATE BLOQUANTE :** s'il reste des 🔴 BLOQUANTS dans `audit-interne.md`, le skill refuse la livraison : *"{N} bloquants à régler avant de prévenir le patron. Les voici : {liste}. Corrige, relance l'audit, on continue après."*
- Quand l'audit passe au vert (0 bloquant) → `gates.audit_livraison_vert: true`.
- Le skill rappelle : **choisis 1 cadeau surprise** dans les "💡 Idées bonus" de l'audit, implémente-le. (Le cadeau délai — livraison anticipée — est déjà acquis structurellement.)
- **Gate de sortie :** `audit_livraison_vert: true` → `etape_actuelle: 6`.

### Étape 6 — Livraison + formation + solde (terrain)

- Le skill détecte si on est **en avance** sur `date_promise_patron`. Si oui (cas normal), il fournit la phrase à dire :
  > *"Je vous avais annoncé sous 2 semaines, votre site est prêt aujourd'hui — soit {X} jours plus tôt. Le voici."*
  C'est le cadeau délai formalisé.
- **Action :** le skill affiche la checklist de livraison (depuis `process.md` étape 4) : démo du site, formation Decap (édition menu/horaires/photos), remise du `rapport-mise-en-service.md`, remise de l'archive repo si demandée.
- **GATE :** "Solde 245€ encaissé ? (oui/non)" → `gates.solde_encaisse`. Le skill rappelle que la formation Decap se fait MÊME si le solde traîne (ne pas prendre le site en otage, ce n'est pas le ton MB Studio), mais note l'impayé en rouge dans le carnet.
- **Gate de sortie :** `dates.livraison_reelle` notée → `etape_actuelle: 7`. Le skill planifie automatiquement `dates.suivi_j30 = livraison_reelle + 30j`.

### Étape 7 — Suivi J+30

- Le skill rappelle au prochain lancement quand `J ≥ suivi_j30 - 3` : *"Le suivi J+30 du {resto} approche ({date}). Prépare le café."*
- **Action :** lancer `monthly-report` (1er rapport mensuel).
- Le skill rappelle le timing du pitch Pack Suivi : **uniquement à la fin, avec l'angle "résiliable à tout moment"** (jamais poussé, principe non-négociable).
- **Gate de sortie :** rapport remis. Client passe en `pilote/termines/{slug}.yml`. Si Pack Suivi signé → note `pack_suivi: true`, le skill replanifie un rappel mensuel récurrent.

---

## Garde-fous critiques (les "murs" du tunnel)

1. **Gate acompte (étape 3→4) :** impossible de lancer la production sans `acompte_encaisse: true`. Protège Mike financièrement. Non contournable par le skill (Mike peut forcer en éditant le YAML à la main, mais le skill ne le proposera jamais et l'en dissuadera).

2. **Gate audit (étape 5→6) :** impossible de livrer avec des bloquants ouverts. Protège la réputation.

3. **Une seule action affichée à la fois.** Le skill ne liste jamais 5 choses à faire. Il dit LA prochaine. Quand elle est faite, il donne la suivante. C'est le principe "tunnel".

4. **La date promise au patron n'est jamais montrée à Mike comme objectif.** Seule `date_cible_interne` est affichée pendant la production. Sinon Mike se relâche et perd l'effet cadeau.

5. **Le skill ne prend jamais le site en otage** pour un solde impayé. Il note l'impayé, il alerte Mike, mais la formation et la mise en ligne se font. Ton MB Studio = confiance.

6. **Pas de pression commerciale sur le Pack Suivi.** Le skill applique le principe non-négociable : jamais en début de relation, seulement à J+30, avec "résiliable à tout moment".

7. **Multi-clients sans confusion.** Le skill gère N clients en parallèle, chacun avec son carnet. Au démarrage il montre le tableau de bord global, jamais il ne mélange deux dossiers.

8. **Reprise à froid.** Si Mike revient après 2 semaines sans rien faire, le skill lit le carnet et reprend exactement où on en était, en rappelant le contexte ("Tu en étais à : brief fait, acompte encaissé, production pas commencée. Cible interne dans 2 jours. On lance new-client maintenant.").

---

## Resources à créer pendant l'implémentation

- `skills/pilote-client/SKILL.md` — le skill lui-même (suivre cette spec)
- `skills/pilote-client/templates/carnet-vide.yml` — squelette du carnet de bord
- `skills/pilote-client/references/gates.md` — la liste exhaustive des gates et leur logique de blocage
- `skills/pilote-client/references/messages-tunnel.md` — bibliothèque des messages affichés à Mike à chaque étape (ton direct, tutoiement, rassurant, anti-jargon)
- `pilote/` — dossier racine des carnets de bord actifs (créer `.gitkeep`, ajouter au repo ; les carnets eux-mêmes sont commités pour ne jamais perdre l'état)
- `pilote/archive/` — prospects qui n'ont pas signé (apprentissage)
- `pilote/termines/` — clients livrés et suivis

---

## Articulation avec les autres skills

`pilote-client` **n'implémente aucune logique métier** des autres skills. Il les **orchestre**. Il appelle, dans l'ordre :

```
scoring-prospects → audit-eatbu → maquette-flash → brief-client
   → new-client → site-from-brief → gmb-setup → audit-livraison
   → (livraison manuelle terrain) → monthly-report
```

Si un skill n'existe pas encore au moment où le tunnel y arrive, `pilote-client` le signale clairement (*"L'étape suivante a besoin du skill X qui n'est pas encore codé. Dis-le à ton terminal Claude."*) plutôt que d'échouer silencieusement.

---

## Décisions Mike validées en session du 2026-05-15

- Délai : **annonce "sous 2 semaines" (brief + 14j), vise brief + 6-7j** en interne. La date promise n'est jamais montrée à Mike comme objectif pendant la prod.
- Format : **pas un document passif, un skill-tunnel interactif** + carnet de bord auto-maintenu par client (Mike n'écrit rien à la main).
- Principe : **Mike ne choisit pas, il suit.** Une action à la fois, gates bloquantes sur acompte et audit.
- La livraison anticipée est un cadeau surprise **structurel** (acquis par design du buffer), formalisé par une phrase fournie à l'étape 6.

---

## Hors-scope (ne PAS implémenter dans ce skill)

- Refaire la logique des skills orchestrés (pilote-client appelle, il ne réimplémente pas)
- Facturation / comptabilité (le carnet note les montants pour mémoire, ce n'est pas un logiciel compta)
- Notifications push / rappels par SMS automatiques (Mike lance le skill quand il bosse ; les rappels sont affichés au lancement, pas envoyés)
- Gestion d'équipe / multi-utilisateurs (Mike est solo, c'est sa force ; revisiter si MB Studio scale avec des associés)
- Synchronisation cloud du carnet (le carnet est versionné dans Git, c'est la sauvegarde)
