# Gates — les murs du tunnel

Logique exhaustive des gates (verrous de progression). Le skill `pilote-client` consulte ce fichier pour décider s'il autorise ou refuse le passage d'une étape à la suivante. **Une gate bloquante ne se contourne JAMAIS depuis le skill.**

---

## Gates bloquantes (le skill REFUSE d'avancer)

### GATE 1 — Acompte encaissé (étape 3 → 4)

| | |
|---|---|
| Champ carnet | `gates.acompte_encaisse` |
| Condition pour passer | `== true` |
| Si `false` | Le skill REFUSE de lancer la production. Message : *"Pas de production tant que l'acompte 245€ n'est pas encaissé. C'est non négociable, c'est ce qui te protège. Relance le patron, on reprend dès que c'est fait."* |
| Pourquoi | Protège Mike financièrement. Un site produit sans acompte = risque d'impayé total + travail perdu. |
| Contournement | Mike PEUT éditer le YAML à la main, mais le skill ne le proposera JAMAIS et l'en dissuade activement s'il le demande. |

### GATE 2 — Audit livraison vert (étape 5 → 6)

| | |
|---|---|
| Champ carnet | `gates.audit_livraison_vert` |
| Condition pour passer | `== true` (= 0 🔴 bloquant dans `clients/{slug}/audit-livraison/audit-interne.md`) |
| Si `false` | Le skill REFUSE la livraison. Message : *"{N} bloquants à régler avant de prévenir le patron. Les voici : {liste tirée de l'audit interne}. Corrige, relance `audit-livraison`, on continue après."* |
| Pourquoi | Protège la réputation MB Studio. Livrer un site avec un bug visible chez le patron = catastrophe de crédibilité au pire moment. |
| Mise à jour | Passe `true` automatiquement quand le skill relit `audit-interne.md` et compte 0 section 🔴 BLOQUANT. |

---

## Gates non bloquantes (le skill NOTE mais n'arrête pas)

### GATE 3 — Solde encaissé (étape 6)

| | |
|---|---|
| Champ carnet | `gates.solde_encaisse` |
| Bloquant ? | **NON.** |
| Logique | Le skill demande "Solde 245€ encaissé ? (oui/non)". Si non : note l'impayé **en rouge** dans `notes`, alerte Mike au prochain lancement, MAIS la formation Decap et la mise en ligne se font quand même. |
| Pourquoi non bloquant | Ton MB Studio = confiance. On ne prend JAMAIS le site en otage pour un solde qui traîne. Principe non négociable. |

### GATE 4 — Capture eatbu faite (rappel étape 3)

| | |
|---|---|
| Champ carnet | `gates.capture_eatbu_faite` |
| Bloquant ? | NON, mais rappel insistant AVANT le brief. |
| Logique | Avant de lancer `brief-client`, le skill demande : *"As-tu fait la capture eatbu ? (étape 0 de brief-client). Si non, fais-la maintenant, 30 secondes."* Sert au "avant/après" de `audit-livraison`. Si Mike dit non et refuse → noter, continuer, prévenir que la comparaison avant/après sera impossible à la livraison. |

### Gates informatives (cochées au brief, non bloquantes mais tracées)

- `gates.domaine_achete_compte_patron` — coché à l'étape 3. Si `false` à l'étape 4 : alerte forte (le domaine DOIT être sur le compte du patron, principe #7), mais ne bloque pas la prod technique (le domaine peut être branché plus tard à l'étape 6).
- `gates.acces_gmb_gestionnaire` — coché à l'étape 3. Si `false` : `gmb-setup` (étape 4) ne pourra pas tourner → le skill le signale et reporte gmb-setup, sans bloquer le reste de la prod.

---

## Ordre d'évaluation des gates par étape

| Transition | Gates vérifiées | Bloquante ? |
|---|---|---|
| 0 → 1 | resto choisi | oui (rien à piloter sinon) |
| 1 → 2 | audit + 3 maquettes prêtes | oui |
| 2 → 3 | réponse patron == "oui" | oui (sinon archive ou attente) |
| 3 → 4 | **`acompte_encaisse == true`** | **OUI — GATE 1** |
| 4 → 5 | build local OK + gmb-setup fait | oui (build cassé = stop) |
| 5 → 6 | **`audit_livraison_vert == true`** | **OUI — GATE 2** |
| 6 → 7 | `dates.livraison_reelle` notée | oui (solde NON bloquant) |
| 7 → fin | rapport J+30 remis | oui |

---

## Règle d'or des gates

Une gate bloquante n'est pas une punition, c'est une **protection de Mike**. Le skill l'explique toujours en une phrase rassurante (« c'est ce qui te protège »), jamais en reproche. Le ton reste celui d'un copilote qui couvre les arrières de Mike, pas d'un contrôleur.
