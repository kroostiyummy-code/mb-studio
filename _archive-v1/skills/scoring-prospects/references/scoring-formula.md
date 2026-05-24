# Formule de scoring — architecture normalisée (Rapport_classement, Mike 2026-05-18)

Source unique de vérité, étape 6. `[verbatim]` = du Rapport_classement ;
`[SPEC]` = décision de spec assumée (pas une impro de l'outil).

Principe : chaque composante est normalisée dans **[0,1]** ; une donnée
**inconnue → 0,50** (jamais 0) et compte comme **non observée** (baisse la
Confidence). Classement **global unique** trié `final ↓ puis confidence ↓`.
`source_list` (eatbu/autre/sans) = filtre/pitch only, pas un tri séparé.

## Normalisation [verbatim]

```
clip(x)            = min(max(x, 0), 1)
inv_score(x,g,p)   = clip((g - x) / (g - p))
log_cap(n,cap)     = clip(log(1+n) / log(1+cap))
rating_norm(r)     = clip((r - 4.0) / 0.7)
```

## Composantes

**business_proof** [verbatim] = `0.55·rating_norm(rating) + 0.45·log_cap(user_rating_count, 300)`
— observé si rating ET user_rating_count présents, sinon 0,50 (non observé).

**presence_gap** [verbatim] : aucun site `1.00` · plateforme/réseau/livraison
seul `0.90` · eatbu `0.80` · SaaS/subdomain (wixsite, sitew, grubkit, jimdo,
wordpress.com, business.site, godaddysites…) `0.65` · vrai domaine propre
`0.35` · inconnu `0.50`. Toujours observé (bucket connu).

**performance_gap** [verbatim] : pas de site `0.60` · sinon
`inv_score(mobile_perf, 85, 40)` · inconnu `0.50`. Observé si pas-de-site ou
(site + Lighthouse perf connu).

**conversion_gap** [verbatim] :
```
present_conversion = 0.20·has_tel_link + 0.15·has_map_link
                   + 0.25·has_primary_cta + 0.20·has_menu_link
                   + 0.10·address_on_page + 0.10·hours_on_page
conversion_gap = pas de site 0.90 · sinon 1 - present_conversion
               · fetch échoué/inconnu 0.50
has_primary_cta = lien/bouton dont le texte ⊃ {réserver, commander,
                  reservation, order, booking}
```
Observé si pas-de-site ou (site + DOM récupéré).

**seo_gap** [verbatim] :
```
seo_checks = moyenne([title_present_&_longueur_ok, meta_desc_present_&_ok,
  h1_present, canonical_present, robots_indexable, sitemap_present,
  schema_localbusiness_or_restaurant, ville_ou_categorie_dans_title_ou_h1])
seo_gap = pas de site 0.90
        · si seo_score connu : 0.60·(1-seo_checks) + 0.40·inv_score(seo,85,50)
        · sinon 0.50
```
[SPEC] `robots_indexable` & `sitemap_present` = 2 GET (`/robots.txt`,
`/sitemap.xml`) sur le même fetch ; **sous-signal non récupérable = 0 dans
seo_checks ET baisse la Confidence**. Observé si pas-de-site ou (site + DOM
récupéré + seo_score Lighthouse connu).

**local_profile_gap** [verbatim] :
```
profile_checks = moyenne([website_on_profile, phone_on_profile,
  hours_on_profile, photos_count>=10, rating_present, review_count_present])
local_profile_gap = 1 - profile_checks · inconnu 0.50
```
[SPEC] signaux Places non persistés au cache (hours_on_profile,
photos_count) = 0 dans profile_checks ET baisse la Confidence. Observé si
Places a répondu (rating/avis présents).

**digital_deficit** [verbatim] = `moyenne([presence_gap, performance_gap, conversion_gap])`
**reputation_misalignment** [verbatim] = `business_proof × digital_deficit`

## Valeur apportable /100 [verbatim]

```
V = 25·presence_gap + 20·performance_gap + 20·conversion_gap
  + 15·seo_gap + 10·local_profile_gap + 10·reputation_misalignment
```

## Probabilité d'acceptation /100 [verbatim]

**switchability** : aucun site `1.00` · plateforme seule `0.90` · eatbu `0.85`
· SaaS/subdomain `0.75` · vrai site faible `0.55` · vrai site déjà très
correct `0.20` · inconnu `0.50`. [SPEC] faible vs correct : `mobile_perf < 60`
→ faible (0.55), sinon correct (0.20) ; site sans Lighthouse → inconnu 0.50.

**contactability** [verbatim] = `0.50·phone_known + 0.25·(email_known | neutre 0.5) + 0.25·(form | IG/FB DM | neutre 0.5)`.

**timing** [verbatim] : aucun site `0.80` · eatbu `0.65` · autre-site défaut
`0.50` · site très récent < 6 mois (Wayback) → écrase à `0.15`.
[SPEC] valeurs discrètes (le « score continu si âge connu » n'est pas formulé).

**independence_class** [verbatim] : indép mono-site `1.0` · petit groupe `0.7`
· hôtel/multi-enseignes `0.4` · chaîne `0`.
**complexity_class** [verbatim] : vitrine 1-5 pages `1.0` · résa/commande
seule `0.7` · multi-établ/menu complexe `0.4`.
[SPEC, résolu par les cas-test d'acceptation] : chaînes déjà exclues → quand
le resto **a un site** à inspecter, défaut `independence=1.0`,
`complexity=1.0` (observable proxy). Quand **pas-de-site** (rien à inspecter),
ces deux comptent comme **non observés → 0.50** (cohérent « inconnu = 0.50 »,
et baisse la Confidence). C'est la seule lecture qui fait tomber les 3
cas-test pile (sinon Festin d'Asie diverge de 7,5 pts).

```
P = 35·business_proof + 20·switchability + 15·contactability
  + 15·timing + 10·independence_class + 5·complexity_class
```

## Score final [verbatim]

```
final = 0.55·V + 0.45·P
```

## Confidence [verbatim principe]

`confidence = 100 · (Σ poids des composantes RÉELLEMENT observées / Σ poids total)`.
[SPEC] poids = coefficients de V `(25,20,20,15,10,10)` + P
`(35,20,15,15,10,5)` ; total = **200**. « Observée » = donnée source mesurée
(Places / Lighthouse / DOM). « Non observée » = branche inconnu/0.50/défaut.
Une composante manquante prend 0.50 dans le score (jamais 0).

## Tiers [verbatim] & bandes d'action [SPEC validé]

```
A : final >= 75 ET confidence >= 60
B : 65 <= final < 75   (inclut final>=75 mais confidence<60)
C : 55 <= final < 65
D : final < 55
```

Tri global : `final ↓ puis confidence ↓`. Bandes d'action par **rang** :
- **Priorité semaine** : top ~10 du classement global
- **Priorité mois** : ~15 suivants
- **Réserve** : le reste
- **À surveiller** : `confidence < 50` (écrase la bande), quel que soit le rang

## DOM fetch (conversion_gap + seo_checks + email/social) [SPEC]

GET homepage (suivi des redirections) + `/robots.txt` + `/sitemap.xml`, UA
identifiable, timeout court, taille HTML plafonnée, **caché**
`prospects/cache/dom/{slug}.json` TTL 30 j, uniquement buckets eatbu /
autre-site. Fetch échoué → conversion_gap = seo_gap = 0.50 + composantes non
observées (Confidence baissée). Aucune découverte Places massive ;
`restaurants.yml` reste la source de vérité unique.
