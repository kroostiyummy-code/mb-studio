---
name: new-client
description: "Ferme la boucle de production d'un nouveau site client : prend le dossier `clients/{slug}/` produit par site-from-brief, crée un repo GitHub privé dédié sous l'organisation `kroostiyummy-code`, fait le commit + push initial, connecte le repo à Cloudflare Pages pour un déploiement automatique, et configure le domaine custom acheté au brief. Output : site en production accessible sur https://{domaine}.fr + URL admin Decap fonctionnelle. MANDATORY TRIGGERS: 'new-client', 'new client', 'déploie le site de'. STRONG TRIGGERS (avec contexte) : 'site prêt à pousser pour [resto]', 'crée le repo et déploie', 'ferme la boucle pour [resto]'. Ne pas déclencher pour : modification d'un site déjà déployé (édition directe), création d'un repo non lié à un client signé."
---

# New Client

Skill MB Studio qui transforme **un dossier local prêt** (`clients/{slug}/`, produit par `site-from-brief`) en **site web en production**, hébergé sur le domaine acheté par le patron au brief.

C'est l'étape qui transforme la production silencieuse en livraison concrète. À la fin de ce skill, le site répond sur `https://{domaine}.fr`, le patron peut visiter et voir son futur site avant le rdv de livraison.

---

## Quand déclencher ce skill

**Bons cas d'usage :**
- "Le site de Le Saint-Hilaire est prêt à pousser, lance new-client"
- "Ferme la boucle pour {slug}"
- "Crée le repo et déploie {slug}"

**Mauvais cas d'usage (ne pas déclencher) :**
- Le dossier `clients/{slug}/` n'existe pas → utiliser `site-from-brief` d'abord
- Le build local échoue (vérification de `site-from-brief` non passée) → corriger d'abord
- Modification d'un site déjà déployé → éditer directement le repo client puis `git push`
- Création d'un repo non lié à un client signé (ex: site perso de Mike) → faire manuellement, ce skill est conçu pour les clients

---

## Inputs requis

Le skill assume que :

1. **`clients/{slug}/` existe** avec un site Astro buildable (npm run build passe sans erreur)
2. **Le patron a acheté un domaine** au brief (sur son compte OVH ou Gandi) — Mike connaît le nom du domaine
3. **Mike a accès à l'organisation `kroostiyummy-code`** sur GitHub (déjà validé par le push du repo mb-studio dans la session précédente)

Demander à Mike au démarrage :

> "OK on ferme la boucle. Donne-moi :
> 1. Le slug du client (doit correspondre au dossier `clients/{slug}/`)
> 2. Le domaine final acheté par le patron (ex: `lesainthilaire.fr`)
> 3. Le registrar du patron (OVH / Gandi / autre) — pour les instructions DNS"

---

## Process en 6 étapes

### Étape 1 — Pré-checks

1. Vérifier que `clients/{slug}/` existe
2. Vérifier que le build local fonctionne :
   ```bash
   cd clients/{slug}
   npm run build
   ```
   Si erreur : arrêter le skill et demander à Mike de relancer `site-from-brief` après correction.
3. Vérifier que le `.gitignore` est bien présent (sinon copier celui du template)

### Étape 2 — Création du repo GitHub

Trois options selon le setup de Mike :

#### Option A — Via `gh` CLI (si installé)

```bash
cd clients/{slug}
gh repo create kroostiyummy-code/{slug}-site \
  --private \
  --description "Site web {NOM_RESTO} — par MB Studio" \
  --source=. \
  --remote=origin
```

#### Option B — Via API GitHub (si Mike a un PAT)

Pré-requis : Mike a un Personal Access Token GitHub dans la variable d'env `$env:GITHUB_TOKEN` (PowerShell) ou `$GITHUB_TOKEN` (Bash), avec scope `repo` et `admin:org` sur l'orga `kroostiyummy-code`.

```powershell
$body = @{
  name = "{slug}-site"
  private = $true
  description = "Site web {NOM_RESTO} — par MB Studio"
  auto_init = $false
} | ConvertTo-Json

$headers = @{
  Authorization = "Bearer $env:GITHUB_TOKEN"
  Accept = "application/vnd.github+json"
}

Invoke-WebRequest -Method POST `
  -Uri "https://api.github.com/orgs/kroostiyummy-code/repos" `
  -Headers $headers `
  -Body $body `
  -ContentType "application/json"
```

#### Option C — Manuel (fallback fiable)

1. Mike ouvre https://github.com/organizations/kroostiyummy-code/repositories/new
2. Repository name : `{slug}-site`
3. Private repo ✓
4. Description : "Site web {NOM_RESTO} — par MB Studio"
5. **NE PAS** initialiser avec README ou .gitignore (le repo doit rester vide pour le premier push)
6. Click "Create repository"
7. Confirmer au skill que le repo est créé

### Étape 3 — Init Git + premier push

```bash
cd clients/{slug}
git init -b main
git add .
git commit -m "feat: initial commit (site généré par MB Studio site-from-brief)"
git remote add origin https://github.com/kroostiyummy-code/{slug}-site.git
git push -u origin main
```

Si erreur d'auth GitHub : reproduire la procédure du repo mb-studio (cf historique des commits, "auth GitHub résolue via Git Credential Manager").

### Étape 4 — Connexion Cloudflare Pages

Deux options :

#### Option A — Via API Cloudflare (si Mike a un token)

Pré-requis : `$env:CLOUDFLARE_API_TOKEN` avec scope `Cloudflare Pages: Edit` + `Account Settings: Read`.

```powershell
$body = @{
  name = "{slug}-site"
  production_branch = "main"
  source = @{
    type = "github"
    config = @{
      owner = "kroostiyummy-code"
      repo_name = "{slug}-site"
      production_branch = "main"
      pr_comments_enabled = $true
      deployments_enabled = $true
    }
  }
  build_config = @{
    build_command = "npm run build"
    destination_dir = "dist"
    root_dir = ""
  }
} | ConvertTo-Json -Depth 10

# (Nécessite ACCOUNT_ID, à récupérer une fois dans .env de Mike)
$headers = @{
  Authorization = "Bearer $env:CLOUDFLARE_API_TOKEN"
}

Invoke-WebRequest -Method POST `
  -Uri "https://api.cloudflare.com/client/v4/accounts/$env:CLOUDFLARE_ACCOUNT_ID/pages/projects" `
  -Headers $headers `
  -Body $body `
  -ContentType "application/json"
```

#### Option B — Manuel (fallback, plus simple pour le MVP)

Donner à Mike ces instructions claires à suivre dans son navigateur :

```
1. Aller sur https://dash.cloudflare.com/
2. Onglet "Workers & Pages" dans le menu de gauche
3. Bouton "Create application" → onglet "Pages" → "Connect to Git"
4. Si premier lien GitHub : autoriser l'app Cloudflare à accéder à l'orga kroostiyummy-code
5. Sélectionner le repo `{slug}-site`
6. Click "Begin setup"
7. Project name : `{slug}-site` (laisser tel quel)
8. Production branch : `main`
9. Build settings :
   - Framework preset : Astro
   - Build command : `npm run build`
   - Build output directory : `dist`
   - Root directory : (laisser vide)
10. Click "Save and Deploy"
11. Attendre le 1er build (~2 minutes). Vérifier que le statut passe en "Success".
12. Confirmer au skill que le déploiement initial a réussi.
```

Le site est maintenant accessible sur `https://{slug}-site.pages.dev` (URL temporaire Cloudflare). On le bascule sur le vrai domaine à l'étape suivante.

### Étape 5 — Configuration du domaine custom

Sur Cloudflare Pages :

```
1. Ouvrir le projet `{slug}-site` sur Cloudflare Pages
2. Onglet "Custom domains"
3. Click "Set up a custom domain"
4. Entrer le domaine : `{domaine}.fr` (ex: lesainthilaire.fr)
5. Cliquer "Continue"
6. Cloudflare détecte que le domaine n'est pas géré par lui et propose 2 options :
   - "Use existing nameservers" (recommandé pour rester simple)
   - "Switch nameservers to Cloudflare"
7. Choisir "Use existing nameservers"
8. Cloudflare affiche 1 enregistrement CNAME à ajouter chez le registrar du patron :
   - Type : CNAME
   - Name : @ (ou rien, dépend du registrar)
   - Value : `{slug}-site.pages.dev`
```

#### Envoi des instructions DNS au patron

SMS / mail au patron avec un texte tout prêt :

```
Bonjour {NOM_PATRON},

Votre site est prêt à être mis en ligne. Il reste 1 action de votre côté
qui prendra 2 minutes :

Connectez-vous à votre compte {OVH | Gandi} et ajoutez 1 enregistrement
DNS sur le domaine {domaine}.fr :

  Type : CNAME
  Nom : @ (ou laisser vide)
  Cible : {slug}-site.pages.dev
  TTL : 3600 (ou par défaut)

Si vous avez besoin d'aide pour cette étape, on peut le faire ensemble
au téléphone, ça prend 5 minutes.

Une fois ajouté, votre site sera en ligne dans 1 à 24h selon le délai de
propagation DNS (souvent 1-2h en pratique).

Mike
```

#### Vérification de la propagation

Après que le patron a confirmé l'ajout DNS :

```powershell
# Vérifier la propagation DNS
nslookup {domaine}.fr

# Vérifier que le site répond
curl -I https://{domaine}.fr
```

Si le site répond avec un statut 200, c'est en ligne. Sinon, attendre 1-2h supplémentaires (propagation DNS).

### Étape 6 — Récap pour Mike

```
✅ Site déployé pour {NOM_RESTO}

🌐 URLs :
   - Site en production : https://{domaine}.fr
   - URL temporaire Cloudflare : https://{slug}-site.pages.dev
   - Admin Decap : https://{domaine}.fr/admin/
   - Repo GitHub : https://github.com/kroostiyummy-code/{slug}-site
   - Cloudflare Pages : https://dash.cloudflare.com/...

⏱  Statut DNS : {EN ATTENTE PROPAGATION (1-24h) | EN LIGNE}

📋 Prochaines actions Mike :
   - Vérifier la propagation DNS dans 1-2h (curl ou test navigateur)
   - Tester l'admin Decap : se connecter via le compte GitHub
   - Programmer le RDV de livraison avec le patron (étape 4 du process)
   - Lancer en parallèle `gmb-setup {slug}` pour optimiser la fiche Google

🎁 Cadeau surprise à ajouter avant livraison :
   - Voir la liste dans process.md section "Le cadeau surprise"
   - Suggérer : {favicon perso | page 404 rigolote | animation discrète}
   - 1 cadeau par livraison, pas 5
```

---

## Format d'output

Le skill produit :

1. **Repo GitHub** `kroostiyummy-code/{slug}-site` créé et alimenté avec le contenu de `clients/{slug}/`
2. **Projet Cloudflare Pages** connecté au repo, build automatique sur chaque push
3. **Domaine custom** configuré (DNS pointant vers Pages)
4. **Récap textuel** structuré avec toutes les URLs + actions restantes

---

## Règles d'or

1. **Ne JAMAIS faire l'achat du domaine** côté Mike. Le domaine reste sur le compte du patron (principe non-négociable #7). Si Mike réalise au moment du `new-client` que le domaine n'est pas acheté → arrêter le skill et faire acheter au patron immédiatement.

2. **Vérifier que le build local passe avant de pousser**. Un site qui ne build pas en local ne buildera pas non plus sur Cloudflare. Le skill `site-from-brief` a déjà fait cette vérif, mais re-vérifier ici.

3. **Le repo client est privé**. Toujours `--private` pour la création du repo. Le code du site contient le contenu personnel du resto, il n'a aucune raison d'être public.

4. **Le repo client appartient à `kroostiyummy-code`**, pas au patron. Le patron récupère un fork ou un transfert le jour où il veut partir (cf engagement 48h du principe #7).

5. **Pas de secrets dans le repo**. Vérifier que `.env` est dans `.gitignore` (déjà le cas par défaut). Aucun token API ne doit fuiter dans le code.

6. **Tester l'admin Decap après go-live**. L'URL `/admin/` doit charger l'interface Decap CMS. Si erreur, vérifier que `public/admin/config.yml` a bien le bon `backend.repo` (= `kroostiyummy-code/{slug}-site`).

7. **Le patron contrôle les DNS**. Mike donne les instructions DNS mais c'est le patron qui les applique sur son compte registrar. Mike peut ASSISTER mais ne se connecte JAMAIS au compte du patron sans lui.

---

## Resources

- `references/cloudflare-setup.md` : procédure Cloudflare Pages détaillée avec captures d'écran (à créer plus tard si besoin)
- `references/dns-instructions-patron.md` : modèle de SMS/mail à envoyer au patron pour les DNS (à créer plus tard)

Pour le MVP, ces résources ne sont pas indispensables — les instructions étape par étape sont dans le SKILL.md directement.

---

## Exemple d'invocation

```
Mike : Lance new-client pour le-saint-hilaire, domaine = lesainthilaire.fr, registrar = OVH.
```

Le skill exécute les 6 étapes :
1. Pré-checks : `clients/le-saint-hilaire/` existe, build OK ✓
2. Crée le repo `kroostiyummy-code/le-saint-hilaire-site` (via gh CLI ou API)
3. Push initial : commit + push de tout le contenu sur main
4. Connecte Cloudflare Pages au repo (manuel via dash, ou API)
5. Configure le domaine `lesainthilaire.fr` sur Cloudflare Pages + envoie SMS au patron avec les DNS à ajouter sur OVH
6. Récap : URLs en production, prochaines actions

Mike reçoit la confirmation du patron 1-2h plus tard que le DNS est en place, vérifie que le site charge, et programme le rdv de livraison.
