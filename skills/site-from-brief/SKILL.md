---
name: site-from-brief
description: "Génère un site Astro complet à partir d'un brief client signé (étape 3 du process commercial : production silencieuse). Prend en input `briefs/{slug}/brief.md` + `briefs/{slug}/settings.yml` (produits par le skill brief-client), produit un dossier `clients/{slug}/` complet et prêt à être transformé en repo Git par le skill new-client. Charge le template `site-resto/`, coule les settings, génère les fichiers de menu, optimise les photos, personnalise README + incident-response, et fait un test build local pour valider. MANDATORY TRIGGERS: 'site from brief', 'site-from-brief', 'génère le site depuis le brief'. STRONG TRIGGERS (avec contexte client) : 'lance la production de [resto]', 'transforme le brief en site', 'crée le site Astro de'. Ne pas déclencher pour : nouveau site sans brief (utiliser maquette-flash à la place), modification d'un site déjà déployé (édition directe du repo client), ou prospect non signé."
---

# Site From Brief

Skill MB Studio pour transformer **un brief signé en site Astro complet, prêt à pousser**.

C'est le cœur de l'étape 3 du process commercial (production silencieuse, 5-10 jours chez Mike). Le skill prend les artefacts produits par `brief-client` (le brief narratif + le settings YAML), les couple au template `site-resto/`, génère tout le reste (menu, galerie, page mentions légales personnalisée), optimise les photos, et fait un test build local.

L'output est un dossier `clients/{slug}/` **qui build sans erreur** et **qui visualise le site final du resto** sur `localhost:4321`. La suite (création du repo Git + setup Cloudflare Pages + déploiement) est gérée par le skill `new-client`.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Lance la production de Le Saint-Hilaire, le brief est dans briefs/le-saint-hilaire/"
- "Site from brief pour {slug}"
- "Transforme le brief en site"

**Mauvais cas d'usage (ne pas déclencher) :**
- Pas de brief.md disponible → utiliser `brief-client` d'abord
- Maquette de prospection (sans brief signé) → utiliser `maquette-flash`
- Modification d'un site déjà déployé → éditer directement le repo client
- Brief signé mais acompte 245€ pas encore encaissé → ATTENDRE l'encaissement (règle d'or absolue, cf process.md)

---

## Inputs requis

Le skill assume que les 2 fichiers suivants existent dans `briefs/{slug}/` :

1. `briefs/{slug}/brief.md` — document narratif structuré (produit par brief-client)
2. `briefs/{slug}/settings.yml` — settings YAML prêt à coller (produit par brief-client)

Optionnel mais recommandé :

3. `briefs/{slug}/photos/` — dossier contenant les photos transférées par le patron au brief (hero + galerie). Si absent, Mike fournit les chemins manuellement quand le skill demande.

**Si l'un des 2 fichiers requis manque** : arrêter le skill et afficher
> "Brief introuvable. Utilise `brief-client` d'abord pour produire `briefs/{slug}/brief.md` et `briefs/{slug}/settings.yml`."

---

## Process en 8 étapes

### Étape 1 — Inputs et vérification acompte

1. Vérifier que `briefs/{slug}/brief.md` et `briefs/{slug}/settings.yml` existent
2. Lire le brief.md et chercher la section "## 10. Acompte 245€"
3. **Si l'acompte n'est pas marqué encaissé** : afficher
   > "L'acompte 245€ n'est pas marqué encaissé dans le brief. Confirme avant que je commence la production : tu l'as bien reçu en espèces / virement / chèque ?"
   
   Mike doit confirmer explicitement avant de passer à l'étape 2.

### Étape 2 — Scaffolding du dossier client

1. Créer le dossier `clients/{slug}/` à la racine du repo MB Studio (déjà ignoré par `.gitignore`)
2. **Copier le template `site-resto/` complet** dedans, en EXCLUANT :
   - `node_modules/` (sera réinstallé par `npm install`)
   - `dist/` (sera regénéré au build)
   - `.astro/` (cache)
   - `examples/` (fixtures de dev, pas utiles pour un site client)

Commande type (PowerShell) :
```powershell
Copy-Item -Path "templates\site-resto\*" -Destination "clients\{slug}\" -Recurse -Exclude @("node_modules", "dist", ".astro", "examples")
```

3. **Nettoyer les contenus de démo du cas zéro (Kroosti)** qui vivent DANS le template (hors `examples/`, donc copiés par le scaffold) et ne sont PAS écrasés par les étapes suivantes :
   - Supprimer `clients/{slug}/src/content/menu/sections/principale.yml` (menu Kroosti — sinon il coexiste avec les sections générées à l'étape 4)
   - Supprimer `clients/{slug}/public/images/foodtruck.jpg` (photo Kroosti — sinon une image d'un autre resto est livrée)
   - `site.yml` et `galerie.yml` contiennent aussi du Kroosti mais sont écrasés aux étapes 3 et 5 — vérifier qu'ils l'ont bien été avant le build.

   > Apprentissage terrain (dry-run La Casa, 2026-05) : sans ce nettoyage, le 1ᵉʳ build sortait le menu ET une photo Kroosti dans le site client. Étape rendue systématique.

### Étape 3 — Injection du settings

1. Copier `briefs/{slug}/settings.yml` vers `clients/{slug}/src/content/settings/site.yml`
2. **Remplacer dans le fichier** :
   - Les éventuels placeholders `{{XXX}}` qui n'auraient pas été remplis au brief → demander à Mike de fournir la valeur
3. Vérifier que les champs obligatoires sont présents et valides selon `src/content.config.ts` (schema Zod)

### Étape 4 — Génération du menu

Parser la section "## 3. Carte" du brief.md :

1. Pour chaque sous-section "### Section N — {NOM_SECTION}", créer un fichier `clients/{slug}/src/content/menu/sections/{slug-section}.yml`
2. Format du fichier généré :

```yaml
ordre: {N}
nom_section: "{NOM_SECTION}"
items:
  - nom: "{NOM_PLAT}"
    description: "{DESCRIPTION}"
    prix: "{PRIX_SANS_EURO}"
    allergenes: [{LISTE_OU_VIDE}]
```

3. Si la section "Combo / Formule" est active dans le brief, le champ `settings.combo` est déjà rempli (vérifier au passage)
4. Voir `references/menu-from-brief.md` pour les règles de mapping détaillées

### Étape 5 — Génération de la galerie + optimisation photos

1. Parser la section "## 6. Photos transférées" du brief.md
2. Pour chaque photo listée :
   - Récupérer le fichier source (dans `briefs/{slug}/photos/` ou via chemin fourni par Mike)
   - **Optimiser** : redimensionner à max 1600px de large, garder l'aspect ratio, qualité 85%
   - Convertir en WebP si possible (sauf si le navigateur cible nécessite JPEG)
   - Copier dans `clients/{slug}/public/images/`
3. Identifier la **photo hero** (marquée "Hero" dans le brief) et la nommer `hero.jpg` (ou `hero.webp`)
4. Générer `clients/{slug}/src/content/galerie/galerie.yml` avec la liste des photos restantes (description + légende du brief)

   **Format obligatoire** — le loader Astro `file()` exige une clé racine `galerie:` (idem `site.yml` avec `site:`) :
   ```yaml
   galerie:
     photos:
       - { src: "/images/plat-1.jpg", alt: "Description SEO", legende: "Légende courte" }
       - ...
   ```
   Sans la clé racine, le build échoue avec une erreur de schéma. Apprentissage du dry-run Al Badea (2026-05).

5. **Auto-décision toggle galerie** :
   - Si galerie ≥ 4 photos : `sections.galerie: true` dans settings
   - Si galerie < 4 photos : `sections.galerie: false` + noter dans le récap final que la galerie sera activée quand le patron uploadera plus de photos via Decap

### Étape 6 — Personnalisation des fichiers contextuels

#### `clients/{slug}/README.md`
Remplacer le README générique du template par un README client :

```markdown
# Site web — {NOM_RESTO}

Site Astro hébergé sur Cloudflare Pages. Édité par {NOM_PATRON} via Decap CMS.

## URLs
- **Site en production** : https://{domaine-acheté}.fr (à compléter après go-live)
- **Admin Decap** : https://{domaine}.fr/admin/
- **Repo GitHub** : https://github.com/kroostiyummy-code/{slug}-site

## Coordonnées patron
- Nom : {NOM_PATRON}
- Téléphone : {TEL_DISPLAY}
- Email : {EMAIL_PATRON}

## Coordonnées MB Studio (en cas d'incident)
- Mike : 07 49 59 24 62 (téléphone pro)
- Email : mike@mb-studio.fr
- Lire `incident-response.md` pour les procédures de dépannage Mike-friendly

## Stack technique
- Astro 5 + Decap CMS + Cloudflare Pages
- Signature : {signature}
- Mode : {fixe | foodtruck}
- Domaine acheté le : {DATE} sur compte {OVH | Gandi} du patron

## Brief de référence
Le brief signé est dans `briefs/{slug}/brief.md` du repo `mb-studio`.

Pour toute évolution hors-garantie : devis MB Studio à 50€/h ou Pack Suivi 50€/mois.
```

#### `clients/{slug}/incident-response.md`
Le template a déjà `incident-response.md` à la racine. Ajouter au TOUT DÉBUT du fichier (avant "D'abord respirer 10 secondes") un encart spécifique au client :

```markdown
## Coordonnées spécifiques à ce client

- **Nom du resto** : {NOM_RESTO}
- **Patron à contacter** : {NOM_PATRON}, {TEL_DISPLAY}
- **Domaine** : {domaine}.fr (sur compte {OVH | Gandi} du patron)
- **Repo GitHub** : `kroostiyummy-code/{slug}-site`
- **Cloudflare Pages** : `https://dash.cloudflare.com/...` (à compléter après new-client)
- **Date de livraison** : {DATE}
- **Fin de garantie technique 30j** : {DATE+30}

---
```

#### `clients/{slug}/public/admin/config.yml`
Remplacer `USER/REPO` (placeholder du template) par `kroostiyummy-code/{slug}-site`. Cette URL sera réelle après le passage de `new-client`.

### Étape 7 — Test build local

1. `cd clients/{slug}`
2. `npm install` (réinstalle les deps)
3. `npm run build`
4. Si erreur :
   - Identifier la cause (champ manquant ? format YAML ? photo introuvable ?)
   - Afficher l'erreur à Mike + suggérer la correction
   - **Arrêter le skill** — Mike corrige le brief ou les photos, puis relance
5. Si succès :
   - Lancer `npm run dev` en background sur localhost:4321
   - Faire une capture Chrome headless du rendu desktop pour valider visuellement

### Étape 8 — Récap final pour Mike

Afficher un récap structuré :

```
✅ Production terminée pour {NOM_RESTO}

📁 Dossier généré : clients/{slug}/
   ├── src/content/settings/site.yml        ✓ injecté depuis brief
   ├── src/content/menu/sections/           ✓ {N} sections, {M} items
   ├── src/content/galerie/galerie.yml       ✓ {P} photos optimisées
   ├── public/images/                       ✓ photos copiées et optimisées
   ├── README.md                            ✓ personnalisé client
   ├── incident-response.md                 ✓ encart coordonnées ajouté
   └── public/admin/config.yml              ✓ repo GitHub mis à jour

🔨 Build : succès ({N} pages générées, {M} ms)
🌐 Aperçu local : http://localhost:4321

⚠️ À valider visuellement avant new-client :
   - Rendu desktop : capture sauvée dans .audit-{slug}/preview-desktop.png
   - Hero photo bien centrée
   - Menu lisible
   - Auto-hide galerie : {ACTIVÉ avec P photos / DÉSACTIVÉ — patron uploadera plus tard}

📋 Prochaine étape :
   → Invoque `new-client {slug}` pour créer le repo GitHub et déployer sur Cloudflare Pages
```

---

## Format d'output

Le skill produit :

1. **Dossier `clients/{slug}/`** complet et buildable
2. **Aperçu local** sur `http://localhost:4321` (serveur dev tournant en background)
3. **Capture screenshot desktop** dans `.audit-{slug}/preview-desktop.png` pour validation visuelle
4. **Récap textuel** structuré en sortie console

**Aucun push Git** côté MB Studio. C'est `new-client` qui gère la création du repo client et le push initial.

---

## Règles d'or

1. **Jamais inventer un champ manquant.** Si le brief.md a un trou (histoire vide, photo manquante, etc.), arrêter et demander à Mike de compléter — pas de Lorem Ipsum, pas de "Bienvenue dans notre restaurant".

2. **Optimiser systématiquement les photos.** Le poids des images est le n°1 facteur de PageSpeed. Une photo non optimisée à 5 Mo peut plomber le LCP de 3 secondes. Resize 1600px max + qualité 85% + WebP quand possible = obligatoire.

3. **Tester le build avant de dire "fait".** Un site qui ne build pas n'est pas un site. Si `npm run build` échoue, le skill ne marque PAS la production comme terminée.

4. **Personnaliser incident-response.md.** Le template a une version générique. Au moment du déploiement chez le client, on remplit les coords spécifiques (patron, repo, Cloudflare, date de livraison) pour gagner du temps en cas de support.

5. **Acompte vérifié avant production.** Règle absolue : si l'acompte 245€ n'est pas marqué encaissé dans le brief, le skill demande confirmation explicite à Mike avant de continuer. Pas de production sans cash dans la poche.

6. **Le brief est figé.** Si Mike réalise pendant la production qu'il manque un truc, c'est qu'il a mal mené le brief. Il rappelle le patron, ou attend la livraison pour ajuster. Pas d'allers-retours pendant la prod (cf process.md, étape 3 — "Communication patron pendant cette phase : un seul mail à J+5").

7. **Inclure le cadeau surprise.** Avant de marquer la production comme terminée, ajouter **un petit truc non annoncé** (favicon personnalisé, animation discrète, page 404 rigolote, etc.) — cf liste dans `process.md` section "Le cadeau surprise". Règle : 1 cadeau par livraison, pas 5.

---

## Resources

- `references/menu-from-brief.md` : règles de mapping détaillées brief.md → menu/sections/*.yml
- `references/images-optimization.md` : guide d'optimisation photos (resize, format, qualité)
- `references/pre-deploy-checks.md` : checklist des vérifications visuelles à faire après build

---

## Exemple d'invocation

```
Mike : Lance la production de Le Saint-Hilaire, le brief est dans briefs/le-saint-hilaire/.
```

Le skill exécute les 8 étapes :
1. Lit brief.md + settings.yml, confirme l'acompte
2. Scaffolde `clients/le-saint-hilaire/` depuis le template
3. Coule le settings, génère le menu (3 sections, 18 items), copie+optimise 6 photos
4. Personnalise README et incident-response avec les coords client
5. Build → succès, dev server lancé sur localhost:4321
6. Capture screenshot pour validation visuelle
7. Affiche le récap : "Production terminée, prochaine étape new-client le-saint-hilaire"

Mike valide visuellement le rendu, puis invoque `new-client le-saint-hilaire` pour pousser sur GitHub et déployer.
