# Benchmarks sectoriels — sites eatbu chartrains

Référence anonyme utilisée à l'étape 5 du pipeline (comparaison "moyenne sectorielle" dans le rapport patron). **Aucun nom de resto ici** : uniquement des moyennes agrégées. Garde-fou : la comparaison patron est toujours anonyme.

---

## Statut de calibration

⚠️ **Valeurs initiales = estimations conservatrices**, à recalibrer au premier vrai run de `scoring-prospects` avec la clé Google PageSpeed (qui mesure pour de vrai 5-10 sites eatbu chartrains). Tant que non recalibré, le rapport patron indique "moyenne estimée du secteur" et non "mesurée".

Procédure de recalibration (à refaire tous les 6 mois) :
1. Prendre 5-10 URLs eatbu chartrains depuis `prospects/{ville}-{date}/prospects-avec-site-eatbu.md` (généré par `scoring-prospects`)
2. Pour chacune : `curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}&strategy=mobile&category=PERFORMANCE&category=ACCESSIBILITY&category=SEO&category=BEST_PRACTICES&key={KEY}"`
3. Moyenner chaque métrique, remplacer le tableau ci-dessous, dater la mesure
4. Passer le statut à "✅ mesuré le {date} sur {N} sites"

---

## Moyennes sectorielles eatbu (mobile)

| Métrique | Moyenne secteur eatbu | Source |
|---|---|---|
| Performance | 38 / 100 | estimation (eatbu = template lourd, JS bloquant, images non optimisées) |
| Accessibilité | 71 / 100 | estimation |
| SEO | 64 / 100 | estimation (pas de Schema.org Restaurant, méta pauvres) |
| Bonnes pratiques | 75 / 100 | estimation |
| LCP (mobile) | 4.2 s | estimation (souvent 3.5-5.5 s observé) |
| CLS | 0.18 | estimation |
| Poids transféré | 3 200 KB | estimation (images non compressées, sliders) |

**Pourquoi ces valeurs sont crédibles comme plancher** : eatbu sert un template mutualisé non optimisé (pas de WebP, JS de slider, pas de lazy-load systématique, pas de Schema.org). Un site Astro + images optimisées + Schema.org du template `site-resto/` est structurellement au-dessus sur les 4 axes. La marge réelle sera encore plus favorable une fois mesurée.

---

## Règle d'usage dans le rapport patron

- N'utiliser la section "Vs un autre restaurant local" du rapport patron **que si** le nouveau site bat la moyenne sur **≥ 2 métriques sur 3** affichées (vitesse, score Google, accessibilité). Sinon, omettre la section (cf garde-fou : on ne valorise que ce qui mérite de l'être).
- Toujours formuler : *"un autre restaurant local comparable"* / *"la moyenne du secteur"*. Jamais de nom.
- Tant que statut = estimation : écrire *"moyenne estimée du secteur"*. Une fois mesuré : *"moyenne mesurée sur {N} sites locaux comparables"*.
