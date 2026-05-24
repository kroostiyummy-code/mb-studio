# Input Agent 3 v2 — Al Badea (Prompt Stitch v2)

Voici les éléments pour produire le prompt Stitch v2 d'Al Badea selon la **doctrine Aération Terra**.

---

## 1. Fiche restaurant (Agent 1) — chargée automatiquement

Le script charge `tests/outputs/al-badea/agent-1.md`. Tu disposes de la fiche complète.

## 2. Copywriting (Agent 2) — chargé automatiquement

Le script charge `tests/outputs/al-badea/agent-2.md`. Tu disposes du YAML copy complet.

## 3. Combinaison anti-jumeau confirmée

```yaml
da: "Mediterraneen_Solaire"
pack_typo: "Bistrot_Classic"  # Libre Caslon Text + Work Sans
structure_hero: "Editorial_Photo_Equipe"
spine: "VENIR"
ton: "Chaleureux_populaire"
```

## 4. Instructions Mike — RÉVISÉES selon doctrine Aération Terra

### 4.1 — Référence principale : Terra Chartres (terrachartres.com)

C'est **la référence d'aération** pour ce site. Mike a explicitement demandé :

> *"Je veux surtout le rendu aéré de Terra sur tous mes sites. On ne doit pas se sentir étouffé et avoir la flemme de lire ou scroller. Au contraire on se sent bien et on a envie d'aller au restaurant découvrir l'univers."*

**Métrique succès** : "Envie de découvrir le restaurant", pas "site moderne".

### 4.2 — Performance 3 secondes max

**NON-NÉGOCIABLE.** Tous les sites MB Studio chargent en moins de 3 secondes sur 4G mobile.

Contraintes spécifiques pour Al Badea :
- 6 photos maximum sur toute la page (Stitch en met souvent 10+)
- Toutes en WebP < 200 Ko
- Pas de Google Maps iframe (screenshot + lien)
- Pas de carrousel JS lourd
- Pas d'autoplay video
- Lazy loading partout sauf hero

### 4.3 — Touches rouge harissa dosées

Couleur exacte : `#B53527` (rouge harissa profond).

**1 à 3 emplacements MAXIMUM** dans le site :
1. ✅ Un mot accent du headline (subtilement, pas comme l'ancien Al Badea qui était trop fort)
2. ✅ La couleur du bouton CTA principal
3. ✅ Optionnel : fine ligne séparatrice entre 2 sections (1px, opacity 60%)

⚠️ **PAS** de fond de section harissa, **PAS** de plusieurs titres en harissa, **PAS** de bordures harissa partout.

### 4.4 — Éléments culturels tunisiens DOSÉS

**Maximum 2 éléments culturels** :

1. **Petit drapeau tunisien dans le header** (20-24px, à côté du nom "Al Badea")
2. **Photo Sidi Bou Said** (stock OK) dans la section ambiance OU dans la section terroir si elle est incluse

**Frise losanges** : OPTIONNELLE. Si incluse, 1 seule fois entre deux sections, 1px, opacity 60%, espacée — pas surchargée.

### 4.5 — Headline avec bicolore SUBTIL

Le headline d'Agent 2 est :

> "Le couscous qui fait
> revenir les gens."

**Bicolore subtil suggéré** : le mot "revenir" en accent harissa `#B53527`, le reste en bleu Sidi Bou Said `#1B4F8A`.

⚠️ **PAS** comme l'ancien Al Badea où c'était massif et plein de mots en rouge. Juste 1 mot, subtil.

### 4.6 — Structure 7 sections (Al Badea n'a pas besoin de section Terroir)

Pour Al Badea, les 7 sections sont :

1. **HERO** — Photo couscous + headline bicolore + CTAs
2. **L'ESPRIT** — 1 photo ambiance + paragraphes courts
3. **RASSURANCE** — 3 cards discrètes (Fait maison · Halal · Sur place & à emporter)
4. **LES INCONTOURNABLES** — 6 plats typographiques
5. **CE QU'ON ENTEND** — Avis fond bleu Sidi Bou Said
6. **VENIR** — Adresse, horaires, téléphone, map screenshot
7. **FOOTER** — Baseline mémoire + coords + credit MB Studio

⚠️ **PAS** de section "Soirées" ou "Privatisation" (Mike a refusé).
⚠️ **PAS** de section "Terroir" pour Al Badea (resto populaire, pas besoin de section ville).

### 4.7 — Section RASSURANCE (nouveau vs Agent 3 v1)

À ajouter entre l'ESPRIT et LES INCONTOURNABLES. Format ultra-discret :

3 cards horizontales (desktop) ou empilées (mobile) :
1. 🌿 **Fait maison**
2. 🌙 **Halal**
3. 🍽️ **Sur place & à emporter**

Style : icônes monochromes (terre cuite `#C0704A`), label Work Sans Medium 14px, fond identique au fond de section, **PAS** de bordures, **PAS** d'ombres, **PAS** de cards colorées.

### 4.8 — Section AVIS avec fond bleu Sidi Bou Said

Citations exactes (5) :
1. "Le couscous est exactement comme à la maison."
2. "Les bricks arrivent encore brûlantes."
3. "Les portions sont vraiment généreuses pour le prix."
4. "On revient régulièrement — c'est toujours bon."
5. "Le meilleur restaurant tunisien de Chartres, sans discussion."

**SANS** attribution inventée. Pas de "Marie B." ou autre prénom.

### 4.9 — Section VENIR

Adresse EXACTE : "9 Rue de la Porte Cendreuse, 28000 Chartres"
(PAS "12 Rue des Oliviers, 75000 Paris" comme Stitch a halluciné la dernière fois)

Téléphones tap-to-call :
- "02 37 28 25 05" → tel:0237282505
- "07 66 21 54 53" → tel:0766215453

Map : screenshot statique (PAS iframe) + lien Google Maps cliquable.

### 4.10 — Footer avec baseline mémoire

Baseline exacte (texte d'Agent 2) :
> "Une assiette généreuse, une brick brûlante,
> et l'envie de revenir dès le lendemain."

Copyright : "© 2026 Al Badea — Chartres" (PAS 2024)
Credit : "Site créé par MB Studio · Chartres" (petit, discret)

**PAS** de "Heritage in every grain" en anglais.

## 5. Fidelity Check obligatoire

Le prompt doit inclure une section finale qui rappelle à Stitch les données NON-NÉGOCIABLES :

**Restaurant** : Al Badea (pas Saveurs de Tunis, ancien nom)
**Adresse** : 9 Rue de la Porte Cendreuse, 28000 Chartres
**Téléphone 1** : 02 37 28 25 05
**Téléphone 2** : 07 66 21 54 53
**Note Google** : 4.6 sur 151 avis (PAS 4.8 ou autre)
**Horaires** : Tous les jours 12h-15h + 18h-00h

**Prix CONFIRMÉS** :
- Fricassé Tunisien : 4€
- Brick Tunisienne : 5€
- Ojja Merguez : 13€
- Tajine à l'Agneau : 16,50€
- Couscous Royal : 19€
- Couscous (gamme) : à partir de 14,50€

**INTERDICTIONS** explicites pour Stitch :
- Pas de Salade Mechouia (plat inventé la dernière fois)
- Pas de bouton "RESERVE" (le restaurant ne propose pas de réservation)
- Pas de menu en anglais (HERITAGE/AMBIANCE/MENU/LOCATION = NON)
- Pas d'attribution d'avis (pas de prénom fictif)
- Pas de "passion", "authentique seul", "expérience unique", "savoureux"

## 6. Format de sortie attendu

Tu produis **un seul prompt en anglais**, copier-collable dans Stitch.

Suis exactement le format de ton system prompt (Agent 3 v2), avec :
- Section LANGUAGE REQUIREMENT en début ET en fin
- Section AÉRATION TERRA en début (les 10 principes)
- Section CULTURAL IDENTITY (drapeau + frise dosés)
- Section FIDELITY CHECK avant CONTENT
- Section CONTENT avec tout le copy d'Agent 2 en français
- Section FINAL REMINDERS

Le prompt doit faire moins de 8000 mots pour ne pas être tronqué par Stitch.

Vas-y.
