# Input Agent 3 — Al Badea (Prompt Stitch)

Voici les éléments pour produire le prompt Stitch final qui générera le design Al Badea.

---

## 1. Fiche restaurant validée (Agent 1) — déjà chargée automatiquement

L'output complet d'Agent 1 est chargé en amont par le script. Tu disposes de :
- L'identité publique complète
- Les forces apparentes
- Les plats signatures
- La fiche d'âme sur 10 axes
- La combinaison anti-jumeau validée
- Les anti-directions (Axe 9)

---

## 2. Copywriting validé (Agent 2) — déjà chargé automatiquement

L'output complet d'Agent 2 est chargé en amont par le script. Tu disposes de :
- Le YAML settings complet avec tout le copy français à utiliser TEL QUEL
- La section `notes_pour_agent_3` qui contient :
  - L'atmosphère visuelle clé
  - Les références visuelles à suivre
  - Les anti-références
  - La palette suggérée (codes hex précis)
  - La typographie suggérée

**Utilise ces éléments comme base.** Tu peux les affiner si nécessaire en t'appuyant sur la doctrine MB Studio, mais ne contredis pas les choix validés.

---

## 3. Combinaison anti-jumeau confirmée par Mike

```yaml
da: "Mediterraneen_Solaire"
pack_typo: "Bistrot_Classic"  # Libre Caslon Text + Work Sans
structure_hero: "Editorial_Photo_Equipe"  # photo dominante + texte côté
spine: "VENIR"
ton: "Chaleureux_populaire"
```

---

## 4. Instructions spécifiques Mike pour le prompt Stitch

### 4.1 — Sur la palette finale

L'Agent 2 a proposé :
- Primaire : `#1B4F8A` (Bleu Sidi Bou Said)
- Secondaire / accent : `#C0704A` (Terre cuite)
- Fond : `#F5F0E8` (Blanc cassé)
- Complémentaire : `#EDE0C8` (Crème naturelle)

**Conserve exactement ces codes hex** dans ton prompt Stitch.

Précise dans le prompt :
- Le **bleu Sidi Bou Said** est l'**identité visuelle forte** (à utiliser sur le headline, certains accents, certaines bordures)
- La **terre cuite** est la **couleur d'action** (CTAs, hover states, accents secondaires)
- Le **blanc cassé** est le **fond dominant** (sections principales)
- La **crème** est la **respiration** entre sections (alternance subtile blanc cassé / crème)

### 4.2 — Sur la photographie

C'est **un point critique** pour ce projet. Tu insistes dans le prompt sur :

- **Style photo cible** : documentaire chaleureux, pas commercial. Lumière naturelle de midi (warm, directe), assiettes vues de dessus (90°) ou en 3/4 (45-60°). Pas de fond noir, pas de fond marbré, pas de chichi.
- **Anti-stock photography absolu** : Stitch ne doit JAMAIS utiliser des photos génériques de couscous "Shutterstock". Si l'image n'existe pas, mieux vaut un placeholder texturé que du stock photo générique.
- **Photo Hero** : assiette généreuse (idéalement couscous), vue plongeante ou 45°, lumière de jour, fond simple (table en bois ou nappe). **Pas de mise en scène cinématographique** comme pour Anamour.

### 4.3 — Sur la typographie

**Libre Caslon Text** pour les headlines :
- Tailles : 56-72px sur mobile, 96-128px sur desktop
- Italic possible sur certains titres de section (effet éditorial doux)
- Poids : Regular ou Bold selon contexte

**Work Sans** pour le body :
- Sizes : 16-18px body desktop, 14-15px caption
- Regular pour body, Medium pour labels CTAs

Précise dans le prompt que ces fonts sont **gratuites Google Fonts** (Stitch les chargera sans problème).

### 4.4 — Sur la structure du site

Le site doit avoir **6 sections principales** (pas plus, pas moins) :

1. **HERO** — Editorial photo + texte côté
2. **AMBIANCE** ("Ici, ça partage les plats.")
3. **CARTE** ("Les incontournables") avec les 6 plats signatures
4. **AVIS** ("Ce qu'on entend souvent en sortant")
5. **VENIR** ("À deux pas de la cathédrale")
6. **FOOTER** avec baseline mémorable + signature MB Studio

⚠️ **Section "soirees" : ABSENTE.** Pas applicable à Al Badea.

### 4.5 — Sur le mobile-first

Le téléphone est l'écran prioritaire. La majorité des restaurateurs et leurs clients consultent depuis mobile. Précise :
- Test du design à **375px en premier**
- Les CTAs sont **toujours accessibles au pouce** (zone basse de l'écran sur mobile)
- Le **tap-to-call** est obligatoire sur tous les numéros de téléphone
- L'adresse est cliquable et ouvre Google Maps
- Pas d'animations qui ralentissent le scroll mobile

### 4.6 — Sur le détail signature

Pour atteindre le standing 10K€ perçu, choisis **UN détail signature visible** pour Al Badea. Suggestion (à intégrer dans le prompt) :

> **Détail signature suggéré** : un grain de pellicule subtil (film grain) sur les photos hero et ambiance, donnant un côté "polaroid de famille" plutôt que "shooting publicitaire". Cohérent avec l'esprit documentaire/authentique du lieu.

Tu peux proposer une alternative si tu trouves mieux, mais **un seul détail signature**, pas plusieurs.

### 4.7 — Sur les anti-références à intégrer

Reprends et étoffe les anti-références d'Agent 2 :
- Pas de fond noir lounge (= Anamour)
- Pas de moucharabieh / zellige / décor "mille et une nuits"
- Pas d'esthétique fast-food (rouge/jaune néon)
- Pas de marbre, pas de blanc pur froid
- Pas d'animations complexes (scroll-jacking, parallax intense)
- Pas d'esthétique SaaS B2B (Stripe, Linear, Notion)
- **Spécifique Al Badea** : pas d'iconographie kebab/shawarma générique (cuisine tunisienne ≠ cuisine kebab)

---

## 5. Format de sortie attendu

Tu produis **un seul prompt en anglais**, copier-collable dans Stitch en un seul bloc.

Suis exactement la structure définie dans `agents/agent-3-prompt-stitch.md` :

1. PROJECT TYPE
2. LANGUAGE REQUIREMENT — CRITICAL (instruction "All visible copy in French")
3. THE PHILOSOPHY ("Atmosphere first..." + sensation finale en français)
4. THE PLACE — Atmosphere
5. THE PLACE — What it is NOT
6. VISUAL DIRECTION (références, palette, typo, photo style)
7. QUALITY BENCHMARK — Perceived value €10,000+
8. STRUCTURE — Mobile-first (les 6 sections détaillées avec le copy français exact)
9. TECHNICAL REQUIREMENTS
10. CONTENT — All visible copy (FRENCH, USE EXACTLY) — copie complète du YAML d'Agent 2
11. FINAL REMINDERS

**Important :**
- Le prompt est **intégralement en anglais** SAUF :
  - La sensation finale citée en français entre guillemets
  - Tout le copy de l'Agent 2 dans la section CONTENT et dans la structure (en français, à utiliser tel quel par Stitch)
- L'instruction **"All visible website copy MUST be in French — do not translate"** doit apparaître **deux fois** : en début (LANGUAGE REQUIREMENT) et en fin (FINAL REMINDERS)
- Le prompt complet doit faire **moins de 8000 mots** pour ne pas être tronqué par Stitch
- À la fin du prompt, ajoute une ligne `---END OF BRIEF---` pour signaler la fin nette

Vas-y.
