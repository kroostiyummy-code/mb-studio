# Contexte projet — MB Studio

> Ce fichier est lu automatiquement par Claude Code à chaque session. Il contient le contexte stratégique et opérationnel pour que toute future session démarre alignée.

## Le porteur de projet

- **Mike**, foodtruckeur à Chartres (28)
- **Non-développeur** : pilote MB Studio en side-project
- Objectif : **transition foodtruck → MB Studio à temps plein** (12-18 mois)
- Vision long terme : agence locale, mais **démarre seul**

## Le projet

MB Studio = micro-agence web locale, niche **restaurants/commerce de bouche à Chartres** ayant un site eatbu.com.

Lire `README.md` pour l'offre complète et `BRAND.md` pour l'identité visuelle.

## Principes non-négociables

1. **Honnêteté radicale** : aucune fausse promesse (pas de "garantie 1ère page Google", pas de "support 24/7", pas de "modifs illimitées")
2. **Process simple** : Mike est non-dev → tout doit être pilotable sans connaissance technique avancée
3. **0€ d'hébergement par site client livré** (Astro + Cloudflare Pages)
4. **Édition autonome** par le client (Decap CMS) → c'est l'argument de vente
5. **Chaque client = ambassadeur potentiel** (footer signé, commission 100€, photo Instagram)

## Stack technique imposée

- **Sites clients** : Astro + Decap CMS + Cloudflare Pages
- **Vitrine MB Studio** : même stack (cohérence)
- **Pas de Next.js** (SSR inutile, coût Vercel imprévisible)
- **Pas de WordPress** (maintenance + sécu + hébergement payant = antagonique au pitch)

## Skills (outillage Claude Code interne)

Le repo héberge les skills MB Studio dans `skills/` au format SKILL.md (compatible Claude Code).

| Skill | Statut | Rôle |
|---|---|---|
| `audit-eatbu` | En cours | Audit gratuit en porte-à-porte (5 min, sur tablette) |
| `maquette-flash` | À venir | Maquette validable en 1h depuis brief court |
| `refonte-eatbu` | À venir | Plan de refonte complet (scrape contenu + setup GMB + Schema.org) |
| `site-from-brief` | À venir | Génération site complet depuis brief structuré |

**Ordre de construction** :
1. `audit-eatbu` (débloque la prospection)
2. Test terrain : 5 visites restos, valider hypothèse prix (médiane ≥ 500€)
3. `maquette-flash` (transforme audit en proposition)
4. `refonte-eatbu` + `site-from-brief` (quand 1er client signé)
5. **Vitrine MB Studio** (en dernier, quand 2-3 cas clients livrés)

## Anti-patterns à refuser

- Ajouter Next.js, React SSR, framework lourd
- Proposer WordPress
- Promettre du SEO garanti
- Ajouter des dépendances payantes (CMS payant, hébergement payant)
- Coder le vitrine avant d'avoir des cas clients réels
- Parler "agence" / "équipe" / "nous" (Mike est solo, c'est sa force)
- Utiliser du jargon tech dans les supports clients

## État du projet (mai 2026)

- Stratégie figée (offre, prix, process, stack, anti-promesses)
- Repo squelette en place
- Skill `audit-eatbu` en construction
- **Prochain jalon Mike** : 5 visites terrain restos chartrains pour valider hypothèse prix (médiane ≥ 500€)
- Statut juridique : à régulariser (ajout activité secondaire BIC service à la micro foodtruck) **avant 1ère facture**

## Conventions de commit

Format conventionnel court, en français, sans emoji :

```
feat(audit-eatbu): ajoute le scoring Lighthouse mobile
fix(brand): corrige hex de la couleur ocre terre cuite
docs(readme): clarifie tarifs des paliers
chore(repo): met à jour .gitignore
```

## Branche de développement

Toutes les modifications vont sur `claude/merchant-outreach-site-zUe07` jusqu'à fusion vers `main`.
