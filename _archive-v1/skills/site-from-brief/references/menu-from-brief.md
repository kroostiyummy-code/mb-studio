# Mapping brief.md → menu/sections/*.yml

Règles précises pour transformer la section "## 3. Carte" du brief en fichiers YAML de menu, exploitables par le composant `Menu.astro` du template.

---

## Structure source dans brief.md

```markdown
## 3. Carte

### Combo / Formule mise en avant

- **Activé :** oui
- **Étiquette :** ★ COMBO
- **Composition :** RIZ + CROQ + BOISSON
- **Prix :** 13,90 €

### Sections du menu

#### Section 1 — Plats principaux (ordre 1)

| Plat | Description | Prix | Allergènes |
|---|---|---|---|
| Riz Kroosti | Poulet pané maison, riz basmati premium, sauce Yummy maison. | 10 | Gluten, Lait |
| Croq Kroosti | Blanc de poulet, cheddar fondant, chapelure japonaise. | 2,50 | Gluten, Lait |

#### Section 2 — Boissons (ordre 2)

| Plat | Description | Prix | Allergènes |
|---|---|---|---|
| Canettes 33cl | Coca-Cola · Sprite · Fanta. Bien fraîches. | 2 | — |
```

---

## Règles de transformation

### Combo

Si la section "Combo / Formule" a `Activé: oui` :
- **Ne pas créer un fichier menu pour ça** — le combo est dans `settings.combo` (déjà géré par brief-client)
- Juste vérifier que `settings.combo.active: true` est bien présent

Si `Activé: non` :
- Vérifier que `settings.combo` est absent du settings.yml (sinon le supprimer)

### Sections du menu → fichiers YAML

Pour chaque sous-section "#### Section N — {NOM_SECTION} (ordre N)" :

1. **Nom de fichier** : slug du nom de section en kebab-case
   - "Plats principaux" → `plats-principaux.yml`
   - "Boissons" → `boissons.yml`
   - "Cave des vignerons" → `cave-des-vignerons.yml`

2. **Contenu YAML** :

```yaml
ordre: N
nom_section: "{NOM_SECTION_TEL_QUEL}"
items:
  - nom: "{NOM_PLAT}"
    description: "{DESCRIPTION_SANS_POINT_FINAL_AUTOMATIQUE}"
    prix: "{PRIX_TEL_QUEL_AVEC_VIRGULE_FRANCAISE}"
    allergenes:
      - "{ALLERGENE_1}"
      - "{ALLERGENE_2}"
```

### Normalisation des champs

| Champ source | Normalisation |
|---|---|
| `Nom du plat` | Garder tel quel, avec les majuscules/minuscules comme dans le brief |
| `Description` | Garder tel quel, **conserver le point final si présent** (cohérence typographique) |
| `Prix` | Format string, virgule française : `10` reste `"10"`, `12,50` reste `"12,50"` (NE PAS convertir en `12.50`) |
| `Allergènes` | Si cellule = `—` ou vide → `allergenes: []`. Sinon split par virgule et trim chaque allergène |

### Cas particuliers

#### Plat sans allergène explicite
Si la cellule allergènes est vide ou contient `—` / `aucun` / `N/A` :
```yaml
allergenes: []
```

#### Description multi-lignes ou avec sauts de ligne
Si le patron a une description longue (rare mais possible) :
```yaml
description: |
  Première phrase.
  Deuxième phrase qui continue.
```

#### Plat avec variation de prix (ex: "12€ ou 18€ selon taille")
Garder le format texte tel quel :
```yaml
prix: "12 ou 18"
```
Le composant Menu rendra `12 ou 18€` (le € est ajouté par le composant via `.cur`).

#### Section avec 0 item
Si le patron a annoncé une section mais sans la remplir au brief (rare) :
- **Ne pas créer le fichier YAML** vide
- Noter dans le récap final pour rappel à la livraison

---

## Ordre d'apparition

Le champ `ordre` détermine l'ordre d'affichage dans la page (`menuSections.sort((a,b) => a.data.ordre - b.data.ordre)` dans `Menu.astro`).

Ordre logique standard pour un resto :
1. Entrées (si présent)
2. Plats principaux
3. Desserts
4. Boissons (ou Cave des vignerons pour gastro)

Si le brief a numéroté les sections (`ordre 1`, `ordre 2`), respecter strictement cette numérotation. Sinon, appliquer l'ordre logique standard et noter dans le récap.

---

## Validation après génération

Après création des fichiers `menu/sections/*.yml`, vérifier que :

1. **Le schéma Zod passe** : démarrer le dev server et vérifier qu'aucune erreur "InvalidContentEntryDataError" n'apparaît
2. **L'ordre numérique est continu** : 1, 2, 3, 4 (pas de saut, pas de doublon)
3. **Chaque item a au minimum** nom + description + prix
4. **Les prix sont des strings**, pas des nombres (le schema Zod attend `z.string()`)

Si l'une de ces validations échoue, arrêter le skill et demander à Mike de corriger la section "## 3. Carte" du brief.md.

---

## Exemple complet

### Brief.md (source)

```markdown
#### Section 1 — Entrées (ordre 1)

| Plat | Description | Prix | Allergènes |
|---|---|---|---|
| Velouté de châtaignes | Crème de châtaignes du Limousin, huile de noisette, croûtons maison. | 8 | Gluten, Fruits à coque, Lait |
| Œuf parfait | Œuf basse température, mousseline d'oignon doux, lard fumé. | 9 | Œuf, Lait |
```

### Fichier généré `clients/{slug}/src/content/menu/sections/entrees.yml`

```yaml
ordre: 1
nom_section: "Entrées"
items:
  - nom: "Velouté de châtaignes"
    description: "Crème de châtaignes du Limousin, huile de noisette, croûtons maison."
    prix: "8"
    allergenes:
      - "Gluten"
      - "Fruits à coque"
      - "Lait"
  - nom: "Œuf parfait"
    description: "Œuf basse température, mousseline d'oignon doux, lard fumé."
    prix: "9"
    allergenes:
      - "Œuf"
      - "Lait"
```
