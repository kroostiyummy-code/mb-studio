# Format des listes de prospects (décision Mike 2026-05-17)

> **Règle gravée.** Le scan produit **3 listes SÉPARÉES** — `liste-eatbu`,
> `liste-autre-site`, `liste-sans-site` — chacune en `.md` **et** en `.txt`
> lisible (ou `.docx` si pandoc dispo). **Jamais** de classement global mélangé,
> **jamais** de « Top 3 toutes listes » dans les livrables. Chaque liste s'ouvre
> par un bloc « 📋 Critères de cette liste » et annonce son tri.

---

## En-tête de CHAQUE liste

```
# {Titre de la liste}

**Chartres — rayon {km} km — {date}** · {N} restaurants

## 📋 Critères de cette liste

- **Ce qui définit cette catégorie :** {définition en français simple}

- **Angle stratégique (pourquoi / comment pitcher ce type) :** {l'angle de vente}

- **Tri de cette liste :** {critère de tri annoncé explicitement}

---
```

### Tri par liste (annoncé en tête, non négociable)

| Liste | Tri |
|---|---|
| `liste-eatbu` | du site **le plus mauvais au moins mauvais** (sous-score « ce qu'on peut lui apporter » décroissant) |
| `liste-autre-site` | idem — du site **le plus faible** d'abord |
| `liste-sans-site` | par **nombre d'avis Google décroissant** (popularité = resto établi + capacité à payer) |

---

## Bloc fiche (un par resto, libellés français)

```
### {N}. {Nom} — {Cuisine} — ⭐ {note Google} / {nb avis} avis

**Adresse :** {rue}, {cp} {ville} · **Téléphone :** {tél ou inconnu}
**Présence web actuelle :** {Site eatbu loué — url | Site perso — url | Aucun site à lui — seulement une page {plateforme} | Aucune présence web}
**Vitesse du site actuel :** {LCP} s pour s'afficher sur mobile (score vitesse {perf}/100)   ← uniquement si applicable (eatbu / autre-site)
**Ce qu'on peut lui apporter :** {valeur}/100
**Probabilité qu'il accepte :** {proba}/100 — **Tier {A|B|C}**

**Les 3 arguments concrets à lui dire :**
1. {argument 1 — la pire métrique mesurée, chiffrée, traduite en conséquence business}
2. {argument 2}
3. {argument 3}

> ℹ️ {mention « données partielles » si note/avis/fiche non mesurés}
> ⚠️ {mention « vitesse non mesurée » si Lighthouse indisponible}
**Drapeau rouge :** {drapeau ou "aucun"}

---
```

Le « Top 3 arguments » est piochée dans `references/argument-library.md` selon
la **pire métrique mesurée** sur CE resto (1er = le plus douloureux et prouvable).
Les notes manuelles de Mike vivent dans `prospects/restaurants.yml`
(`notes_mike`), jamais dans ces fiches régénérables.
