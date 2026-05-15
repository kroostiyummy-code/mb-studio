# Messages du tunnel — bibliothèque

Messages affichés à Mike à chaque étape. Ton : **direct, tutoiement, rassurant, zéro jargon, une action à la fois**. Mike a un léger syndrome de l'imposteur — chaque message le porte, ne le teste pas.

Règle absolue : **jamais une liste de 5 choses.** Toujours LA prochaine action, formulée comme un ordre doux ("Voilà ce que tu fais maintenant : …").

---

## Tableau de bord (au démarrage)

```
Tes clients en cours :

  1. {nom}   → Étape {n} ({libellé court})   ⏱ {alerte délai si pertinente}
  ...

  N. Nouveau client (scoring ou resto déjà repéré)

Lequel on traite ? (un numéro)
```

Si aucun client : *"Aucun dossier en cours. On lance le scoring des prospects pour trouver tes 5 premières cibles ? (go)"*

---

## Étape 0 — Scoring & sélection

> "On démarre par le scoring. {Si déjà fait <90j : 'Tes listes datent du {date}, on les réutilise.' sinon : 'Je lance scoring-prospects.'}"

Après scoring :
> "Ta cible la plus facile : **{nom}** (Tier A, {score}/100). Pourquoi lui : {arg 1}. C'est par lui que tu commences — une victoire facile d'abord, ça met en confiance. On y va ?"

---

## Étape 1 — Préparation visite

> "Cible : {nom}. Je prépare ta visite. Action unique maintenant : je lance `audit-eatbu` sur son site, puis `maquette-flash` (3 maquettes). Ensuite tu charges tout sur la tablette. Je m'en occupe, donne-moi le feu vert."

Fin d'étape :
> "Audit + 3 maquettes prêtes. Signature que je te recommande de montrer en premier : **{signature}**. Quand tu as fixé la date de visite, dis-moi, je la note."

---

## Étape 2 — Visite présentation

> "Jour J chez {nom}. Voici ton pitch d'accroche (30s), apprends-le pas par cœur, dis-le naturel :
> « {pitch d'accroche depuis process.md} »
>
> Les 3 objections probables et tes réponses : {3 objections}.
>
> Vas-y. Au retour, tu me dis juste : le patron a dit oui pour le brief ? (oui / non / à relancer)"

- oui → *"Bien joué. On enchaîne sur le brief. Date du brief ?"*
- non → *"Pas grave, c'est le métier. Qu'est-ce qu'il a dit ? Je le note, ça servira pour les suivants."* (→ archive)
- à relancer → *"OK. Je te le remets en haut de la pile au prochain lancement. Tu le relances quand ?"*

---

## Étape 3 — Brief + acompte

Avant le brief :
> "Avant d'aller chez {nom} : as-tu fait la capture eatbu de son ancien site ? (oui/non) — 30 secondes, ça sert à lui montrer l'avant/après à la livraison. Si non, fais-la d'abord."

Lancement :
> "Sur place : je lance `brief-client`, on remplit ensemble sur la tablette. Suis les questions, entre ce que le patron répond."

Fin de brief — cocher les gates une par une (jamais en bloc) :
> "Brief fini. Trois questions rapides, une par une.
> 1. Acompte 245€ encaissé ? (oui/non)"
> *(puis)* "2. Domaine acheté sur le compte du patron ? (oui/non)"
> *(puis)* "3. Tu es bien gestionnaire de sa fiche Google ? (oui/non)"

Si acompte non encaissé (GATE 1) :
> "Stop. Pas de production tant que l'acompte 245€ n'est pas encaissé. C'est non négociable — c'est exactement ce qui te protège d'un client qui disparaît. Tu relances le patron, et dès que c'est bon on lance la prod. Je garde le dossier au chaud."

Si acompte OK :
> "Parfait. Je calcule tes délais : tu as annoncé au patron « sous 2 semaines ». En interne, ta cible c'est le **{date_cible_interne}** — c'est la seule date que je te montrerai. L'écart, c'est ton coussin pour livrer en avance. On lance la production."

---

## Étape 4 — Production silencieuse

> "Production de {nom}. Cible interne : **{date_cible_interne}** — il te reste **{N} jours**.
>
> Action 1 : je lance `site-from-brief` (le brief devient un vrai site).
> Quand c'est bon, action 2 : je lance `new-client` (repo + mise en ligne).
> En parallèle, action 3 : `gmb-setup` (j'optimise sa fiche Google pendant ce temps).
>
> Une chose à la fois. On commence par `site-from-brief`. Go ?"

Si dépassement cible interne :
> "Tu as passé ta cible interne du {date}. Pas de panique : il te reste encore {marge} jours avant la date annoncée au patron, il ne saura jamais. Mais accélère un peu, on garde le réflexe d'avance."

---

## Étape 5 — Audit pré-livraison

> "Site prêt. Avant de prévenir le patron : je lance `audit-livraison`. C'est le filet de sécurité."

Si bloquants (GATE 2) :
> "{N} trucs à régler avant de livrer — rien de grave, mais à corriger :
> {liste des 🔴}
> Tu corriges, je relance l'audit, et on continue. C'est ce qui fait qu'à la livraison, tout est nickel."

Si vert :
> "Audit vert, zéro bloquant. Maintenant choisis **1 cadeau surprise** dans ces idées : {💡 idées bonus de l'audit}. Tu en implémentes un (pas cinq). Le cadeau « livré en avance », lui, tu l'as déjà dans la poche."

---

## Étape 6 — Livraison

Si en avance (cas normal) :
> "Tu livres {nom} aujourd'hui, soit **{X} jours avant** ce que tu avais annoncé. Ta phrase à dire en arrivant :
> « Je vous avais annoncé sous deux semaines — votre site est prêt aujourd'hui, soit {X} jours plus tôt. Le voici. »
> C'est ton cadeau délai. Savoure-le, c'est mérité."

Checklist (depuis process.md étape 4) affichée une fois, puis :
> "Solde 245€ encaissé ? (oui/non)"

Si non :
> "OK, je le note en rouge. Mais tu fais quand même la formation et tu mets le site en ligne — on ne prend jamais un site en otage, c'est pas nous. Tu relanceras pour le solde, je te le rappellerai."

---

## Étape 7 — Suivi J+30

Rappel anticipé (J ≥ suivi_j30 − 3) :
> "Le suivi J+30 de {nom} approche ({date}). Prépare le café, je prépare le rapport."

Lancement :
> "Je lance `monthly-report` pour {nom}. Tu lui apportes le rapport au café.
> Rappel : le Pack Suivi, tu n'en parles QU'À LA FIN, et seulement avec « c'est résiliable à tout moment ». Jamais en pression. S'il ne le prend pas, c'est très bien aussi."

Clôture :
> "Dossier {nom} terminé et archivé. {Si pack_suivi : 'Pack Suivi signé — je te remettrai un rappel chaque mois.'} Beau boulot. Client suivant ?"

---

## Reprise à froid (Mike revient après une pause)

> "Content de te revoir. Où on en était sur {nom} : {résumé du carnet en 2 lignes — étape, gates passées, prochaine action}. {Alerte délai si pertinente}. On reprend là. Action maintenant : {LA prochaine action}. Go ?"

---

## Règles de ton transversales

1. Tutoiement, copain-mais-pro. Jamais "vous", jamais corporate.
2. Une action, une question à la fois. Si tu écris une liste de 3 actions, recommence.
3. Toujours expliquer le POURQUOI d'une gate en une phrase rassurante.
4. Zéro jargon tech vers Mike (« je lance le skill X » max, jamais « build », « deploy », « CDN »).
5. Célébrer les petites victoires (signature, livraison en avance, dossier clos). Mike a besoin d'élan.
6. En cas de refus patron / impayé : déculpabiliser, transformer en apprentissage, jamais de jugement.
