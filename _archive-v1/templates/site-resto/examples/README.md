# Fixtures de test — `examples/`

Trois jeux de settings prêts à l'emploi pour **dogfooder le template** avec des cas représentatifs des familles de resto ciblées par MB Studio.

| Fixture | Signature | Mode | Dominante | Use case |
|---|---|---|---|---|
| `kroosti-foodtruck.yml` | Fast-food | foodtruck | `#8b0e0e` rouge profond | Cas zéro MB Studio (le foodtruck de Mike) |
| `gastronomique-elegant.yml` | Gastro | fixe | `#1a4d3a` vert sombre forêt | Bistronomique / table raffinée |
| `bistrot-tradition.yml` | Traditionnel | fixe | `#7d3c1a` brun terre cuite | Bistrot familial / terroir |

## Comment activer une fixture

Le contenu de chaque fixture est conçu pour remplacer **intégralement** le fichier `src/content/settings/site.yml`.

**Sur Windows PowerShell** :

```powershell
Copy-Item -Path "examples\gastronomique-elegant.yml" -Destination "src\content\settings\site.yml" -Force
```

**Sur Unix/macOS** :

```bash
cp examples/gastronomique-elegant.yml src/content/settings/site.yml
```

Le serveur dev hot-reload automatiquement. Visite `http://localhost:4321` pour voir le résultat.

## À noter

- Les **photos** (hero + galerie) ne sont **pas** dans les fixtures — elles restent inchangées dans `public/images/` et `src/content/galerie/galerie.yml`. Pour un test totalement isolé du resto, il faudrait aussi swap ces fichiers, mais pour valider le rendu visuel des palettes/typos/structures, le contenu de Kroosti convient.
- Le **menu** (`src/content/menu/sections/*.yml`) n'est pas non plus dans les fixtures. On teste donc la structure du template, pas la cohérence sémantique du menu.
- Les fixtures servent aussi de **point de départ** pour les futurs skills `maquette-flash` et `site-from-brief` : copier la fixture la plus proche du brief, puis remplacer les champs un par un.
