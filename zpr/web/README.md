# La page web — mode d'emploi (sans rien installer)

Deux calculatrices dans **une seule page**, à ouvrir dans ton navigateur. Aucune
ligne de commande, aucune installation.

## Comment l'ouvrir

1. Récupère le dossier `zpr/web/` (les 3 fichiers `.js` + `index.html` doivent
   rester **ensemble** dans le même dossier).
2. **Double-clique sur `index.html`** → il s'ouvre dans ton navigateur (Chrome,
   Edge, Firefox…).
3. C'est tout. Tu peux mettre la page en favori.

> 📲 **Pour avoir un lien à cliquer** (utilisable sur téléphone, à partager) :
> suis [`MISE-EN-LIGNE.md`](MISE-EN-LIGNE.md) — 2 minutes, gratuit, sans coder.

## Onglet « 🧭 Où prospecter ? »

Compare des villes pour décider où t'implanter.

1. Clique **« ▶︎ Voir un exemple »** pour voir tout de suite comment ça marche
   (chiffres fictifs), puis **« Calculer le classement »**.
2. Pour tes vraies villes : pour chaque ville, renseigne au minimum :
   - **Nombre de logements** — sur le site de l'INSEE (lien sous chaque ville) ;
   - **Ventes par an** — le bouton **⚡ Récupérer** essaie de le remplir tout seul.
     S'il n'y arrive pas (protection du navigateur), ouvre la **carte DVF** (lien
     fourni) et compte les ventes — la page te guide.
3. Les champs *optionnels* (% propriétaires, % 60 ans+, % passoires F/G) **affinent
   le score** mais ne sont pas obligatoires.
4. **Calculer le classement** → verdict **GO / NO-GO** (seuil 4 %) et classement.

## Onglet « 📊 Où j'en suis ? »

Suit ton activité vers l'objectif (100 000 € / 10 mandats en 6 mois).

1. Vérifie ton **objectif** en haut (déjà pré-rempli).
2. Ajoute tes **prospects** et tiens leur **statut** à jour
   (contact → qualifié → estimation → mandat).
3. Le **tableau de bord** se met à jour tout seul : mandats, CA, projection à
   l'échéance, **nombre de contacts à produire par semaine**, et alertes de
   conformité (Bloctel/RGPD).

## Bon à savoir

- **Rien n'est envoyé sur Internet** : tout se calcule dans ton navigateur. Tes
  prospects restent sur ton ordinateur (la page ne les sauvegarde pas encore d'une
  fois sur l'autre — demande-moi si tu veux cette option).
- Le bouton ⚡ va chercher des données publiques **gratuites** (DVF, DPE, INSEE).
- Mêmes calculs que les outils « pros » du dossier (`zpr/run_zpr.py`,
  `zpr/tunnel/run_tunnel.py`) — la page n'est que la version « sans commande ».

## Vérifier que la mécanique est bonne (facultatif)

Les calculs sont testés automatiquement : `node zpr/web/tests/test-core.js`.
