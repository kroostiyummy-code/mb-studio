# Mettre la page en ligne (avoir un lien à cliquer)

Objectif : transformer le dossier `zpr/web/` en **adresse web** (ex.
`https://zpr-mbstudio.pages.dev`) que tu ouvres d'un clic, même sur ton téléphone.

> Bonne nouvelle : une fois en ligne (en `https`), le bouton **⚡ Récupérer**
> fonctionne **mieux** qu'en ouvrant le fichier en local.

Tu n'as **rien à installer** ni à coder. Choisis **une** des deux options.

---

## ✅ Option A — La plus rapide (glisser-déposer) · ~2 min

Idéale pour tester tout de suite. Pas de compte technique, pas de Git.

1. Sur GitHub, télécharge le projet : bouton vert **« Code » → « Download ZIP »**,
   puis décompresse-le. Repère le dossier **`zpr/web`**.
2. Va sur **https://app.netlify.com/drop** (ou, si tu as déjà un compte
   Cloudflare : tableau de bord → **Workers & Pages → Create → Pages → Upload assets**).
3. **Glisse le dossier `web`** dans la zone prévue.
4. Au bout de quelques secondes, tu obtiens **un lien `https://…`**. C'est fini 🎉
   Mets-le en favori, partage-le, ouvre-le sur ton téléphone.

> Pour publier une nouvelle version plus tard : tu re-glisses le dossier. (Mise à
> jour manuelle.)

---

## 🔁 Option B — Mise à jour automatique (Cloudflare Pages + GitHub) · ~5 min

C'est l'hébergement déjà utilisé par MB Studio. Avantage : **chaque modification
poussée sur GitHub se met en ligne toute seule**. Ton dépôt reste **privé** — seule
la page est publique (et elle ne contient aucune donnée de prospect).

1. Connecte-toi sur **https://dash.cloudflare.com** → **Workers & Pages** →
   **Create** → onglet **Pages** → **Connect to Git**.
2. Autorise GitHub et choisis le dépôt **`mb-studio`**.
3. Dans la configuration du build, mets **exactement** ceci :
   - **Production branch** : `claude/real-estate-prospecting-tool-lh7whh`
     (ou `main` une fois la branche fusionnée) ;
   - **Framework preset** : `None` ;
   - **Build command** : *(laisser vide)* ;
   - **Build output directory** : `zpr/web`
4. **Save and Deploy**. Au bout d'une minute, tu as ton lien `…pages.dev`.

À chaque fois que tu (ou moi) mettons à jour la page, elle se republie seule.

---

## Lequel choisir ?

| | Option A (glisser) | Option B (Cloudflare + Git) |
|---|---|---|
| Rapidité | ⚡ 2 min | 5 min |
| Compte requis | aucun (Netlify Drop) | compte Cloudflare |
| Mises à jour | manuelles (re-glisser) | **automatiques** |
| Recommandé pour | tester, dépanner | usage durable |

**Mon conseil :** Option A pour voir ton lien tout de suite aujourd'hui, puis
Option B quand tu veux que ça se mette à jour tout seul.

---

## Questions fréquentes

- **Mes prospects seront-ils visibles en ligne ?** Non. La page calcule tout dans
  ton navigateur ; rien n'est envoyé ni stocké en ligne. Le lien public ne montre
  que la calculatrice vide.
- **Le dépôt devient-il public ?** Non (Option B garde le dépôt privé ; seule la
  page est servie).
- **Ça coûte quelque chose ?** Non, ces hébergements sont gratuits pour cet usage.
- **Besoin d'aide pour choisir le nom du lien ?** Demande-moi, je te propose un
  nom propre (ex. `zpr-mbstudio`).
