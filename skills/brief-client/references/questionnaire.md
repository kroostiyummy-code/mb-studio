# Questionnaire détaillé — 12 sujets du brief client

Liste exhaustive des questions à poser dans l'ordre, par sujet. Le skill `brief-client` suit cette structure pour conduire l'entretien.

---

## Sujet 1 — Identité (5 min)

> "On commence par les bases."

1. Quel est le **nom officiel** du restaurant, tel qu'il apparaît sur la devanture et sur Google ?
2. Avez-vous un **slogan court** ? (ex: "Le 1er Riz Kroosti à Chartres", "Cuisine du marché", "Bistrot familial depuis 1972")
3. Quelques **mots-clés** pour décrire le resto en 5 secondes ? (ex: "Halal · Fait maison · 170 avis 5★")
4. En quelle **année** avez-vous ouvert ?
5. La **ville** précise (avec code postal si possible) ?
6. Votre **numéro de téléphone** principal, format français ?

**Reformulation type** :
> "Donc je résume : {Nom}, à {Ville}, depuis {année}. Slogan court '{slogan}'. Sous-titre : '{baseline}'. Téléphone {tel}. C'est bon ?"

→ Mapping settings : `nom`, `slogan`, `baseline`, `est_year`, `ville`, `region_code` (à déduire du département), `telephone` (E.164), `telephone_display` (format français lisible)

---

## Sujet 2 — Histoire du resto (8 min)

> "Maintenant l'histoire. C'est ce qui va donner du caractère au site."

1. Depuis **combien de temps** le resto existe ?
2. Qui est **derrière** ? (le chef, le couple fondateur, la famille…)
3. **Pourquoi** ce resto ? (l'anecdote, la raison)
4. Ce qui **différencie** votre resto de ses voisins (fait maison, produits locaux, ambiance, recette signature, etc.)
5. Une phrase d'accroche **forte** que vous diriez à quelqu'un qui demande "c'est quoi votre resto ?" en 10 secondes

**Reformulation type** :
> "Si je résume votre histoire en 3 phrases : '{phrase 1}. {phrase 2}. {phrase 3}'. Ça vous va ?"

→ Mapping settings : `histoire.statement_lead` + `histoire.statement_accent` (la phrase d'accroche découpée), `histoire.body` (les 2-3 phrases reformulées avec emphases `**mot**`), `histoire.lancement_year`

---

## Sujet 3 — Spécialités et carte (15 min)

> "Place à la carte. C'est la section la plus importante du site."

**Combo / Formule (si applicable) :**
1. Avez-vous une **formule mise en avant** ? (menu du jour, combo, formule midi…)
2. Si oui : son **nom**, sa **composition**, son **prix exact**

**Menu détaillé** :
3. Combien de **sections** voulez-vous afficher ? (entrées / plats / desserts / boissons / vins / autres)
4. Pour chaque section, **les plats** un par un :
   - Nom du plat
   - Description courte (1-2 lignes max)
   - Prix exact (avec virgule pour les centimes : "12,50")
   - **Allergènes** : Gluten / Lait / Œuf / Fruits à coque / Soja / Poisson / Crustacés / Céleri / Moutarde / Sésame / Sulfites / Lupin / Mollusques / Arachide (obligation légale française — Décret 2015-447)

**Note Mike** : si le patron a la flemme de tout détailler, lui dire : "On peut commencer par vos 5 plats signatures. Le reste s'ajoutera au CMS, vous pourrez le faire en 10 minutes depuis votre téléphone après la livraison."

**Reformulation type** :
> "Donc on a {N} sections : {liste}. Combo {combo_nom} à {prix}€. {N plats} détaillés. Allergènes notés pour {N} plats. On passe à la suite ou vous voulez en rajouter ?"

→ Mapping settings : `combo` (object si applicable), + fichiers `src/content/menu/sections/{section}.yml` un par section

---

## Sujet 4 — Adresse et horaires (5 min)

> "Maintenant l'adresse et les horaires."

1. **Mode** : Est-ce que le resto a **une adresse fixe** ou est-ce un **foodtruck itinérant** ?

**Si mode fixe** :
2. **Adresse complète** (rue, numéro, code postal, ville)
3. **Horaires** pour chaque jour de la semaine :
   - Lundi : ouvert ? Si oui, quels créneaux ? (midi : HH:MM-HH:MM, soir : HH:MM-HH:MM)
   - Mardi, Mercredi, Jeudi, Vendredi, Samedi, Dimanche : idem
4. Le patron a-t-il un **lien Google Maps embed** ou doit-on le générer ? (Maps > Partager > Intégrer)

**Si mode foodtruck** :
2. **Tournée hebdomadaire** : pour chaque jour, le foodtruck est-il en service ?
3. Pour chaque jour en service : **lieu**, **ville**, **moment** (midi/soir), **horaires** (HH:MM-HH:MM)

**Reformulation type (fixe)** :
> "Mode fixe à {adresse}. Ouvert : {liste jours}. Fermé : {liste}. Service du midi : {horaire}. Service du soir : {horaire}. OK ?"

→ Mapping settings : `mode`, `adresse`, `geo` (à géocoder), `google_maps_embed_url` (si fourni), `horaires` ou `horaires_foodtruck`

---

## Sujet 5 — Réseaux sociaux et avis Google (3 min)

> "Pour les réseaux et Google."

1. Le resto a-t-il un compte **Instagram** ? Si oui, l'URL ou le @handle.
2. Une page **Facebook** ? URL ou nom.
3. Un compte **TikTok** ? URL ou @handle.
4. Un **Snapchat** ? URL ou @handle.
5. **Note Google actuelle** et **nombre d'avis** (Mike peut vérifier en direct sur la fiche GMB)
6. **URL de la fiche Google** pour le bouton "Lire les avis"

**Note Mike** : si la note < 4.0 ou les avis < 20, le bloc Avis sera auto-caché par le template. Expliquer au patron : "On l'active dès que vous montez à 4★ et 20 avis. Avec le Pack Suivi mensuel, on peut travailler ça ensemble."

→ Mapping settings : `reseaux.*`, `avis_google.note`, `avis_google.count`, `google_avis_url`

---

## Sujet 6 — Photos (10 min, le sujet le plus long)

> "Les photos. C'est le n°1 facteur de conversion."

1. Avez-vous des **photos sur votre téléphone** ? On va les transférer maintenant.
2. **Méthodes de transfert** :
   - AirDrop si patron sur iPhone et Mike sur iPhone/Mac
   - WhatsApp à Mike puis téléchargement
   - Mail à Mike avec pièce jointe
   - Câble USB si patron OK pour brancher

3. Pour chaque photo transférée :
   - **Description** (sera utilisée pour le `alt` SEO et l'accessibilité) : ex "Bol de Riz Kroosti avec poulet pané et sauce maison"
   - **Légende** (optionnelle, courte) : ex "Notre plat signature"

4. **Photo hero** : laquelle est la plus forte ? Le foodtruck en service, la salle au coucher du soleil, le plat signature en gros plan ?

**Note Mike** :
- Si **0-3 photos** disponibles : la galerie sera auto-cachée. Proposer au patron : "Vous pouvez me faire 4-5 photos rapides maintenant avec votre téléphone (vue de la salle, gros plan plat, équipe, devanture, terrasse), je les retouche après."
- Si **4+ photos** : galerie active, on continue
- Si le patron veut un **photographe pro** : noter pour proposition future Pack Pro 120€/mois (à introduire après 6e client)

→ Mapping settings : `hero_image` + `hero_image_alt`, + fichier `src/content/galerie/galerie.yml` avec liste photos

---

## Sujet 7 — Bandeau actualités (3 min, optionnel)

> "On peut afficher un bandeau en haut du site qui défile avec des messages courts. Le patron peut le modifier en 30 secondes depuis son téléphone. C'est sa plus belle démo d'autonomie."

1. **Voulez-vous activer un bandeau** ? (oui / non / on verra)
2. Si oui : **3 à 6 messages courts** à mettre dedans
   - Ex : "Menu du marché renouvelé chaque mercredi", "Fermé le 15 août", "Plat du jour : tartare 14,50€"

**Note Mike** : si le patron hésite, lui montrer un exemple sur la maquette Kroosti ("vous voyez le bandeau jaune avec '170 avis 5★ · Halal · Fait maison'", etc.). Le patron comprend visuellement.

→ Mapping settings : `bandeau.messages[]`, `sections.bandeau: true/false`

---

## Sujet 8 — Notre exigence (3 min, optionnel)

> "Si vous avez une certification ou une checklist qualité (fait maison, bio, halal, AOP, etc.), on peut l'afficher en bloc."

1. **Voulez-vous activer un bloc "Notre exigence"** ?
2. Si oui :
   - Un **titre** court en 2-3 lignes (ex: "Tout. Vraiment **tout.** Fait maison.")
   - Une **checklist** de 4-6 points qualité (ex: "Riz cuit minute", "Sauce maison", "Cookie maison")
   - Une **bannière finale** optionnelle (ex: "100% Halal — Certifié", "Maître Restaurateur 2021", "AOP depuis 1985")

→ Mapping settings : `exigence.*`, `sections.exigence: true/false`

---

## Sujet 9 — Réservation (2 min)

> "Le bloc 'Réservez' avec le numéro géant. Vous voulez personnaliser le texte ou on utilise les défauts ?"

1. Le **kicker** (petite phrase d'accroche) : ex "Pas envie de faire la queue ?", "Une table en vue ?", "Une bonne table ?" — sinon défaut "Une table en vue ?"
2. Le **titre principal** : ex "Réservez votre commande.", "Réservez votre table.", "Réservez votre repas." — sinon défaut "Réservez votre table."
3. **3 perks** à mettre en avant : ex "Évitez la queue / Prêt à votre arrivée / Service rapide" — sinon défauts "Service rapide / Accueil chaleureux / À votre arrivée"

→ Mapping settings : `reservation.kicker`, `reservation.titre`, `reservation.perks[]`

---

## Sujet 10 — Acompte 245€ (1 min)

> "On verrouille l'acompte avant la prod."

1. **Forme de paiement** : espèces / virement / chèque
2. Si **espèces** : encaisser maintenant devant le patron, donner reçu signé
3. Si **virement** : confirmer que le RIB MB Studio est bien transmis, virement à faire avant la fin de la journée
4. Si **chèque** : encaisser physiquement, vérifier nom + montant + date + signature

**Reçu** : Mike donne un **reçu signé** au patron avec mention "Acompte 50% Pack Solo — 245€ — sera encaissé par MB Studio".

**Règle absolue** : pas de production sans acompte. Si le patron promet de payer plus tard sans encaisser maintenant, **arrêter le brief** et reprendre à l'encaissement effectif.

→ Pas mapping settings : noter dans `brief.md` la forme + date d'encaissement.

---

## Sujet 11 — Achat du nom de domaine (5 min)

> "On va acheter votre nom de domaine maintenant. Sur VOTRE compte, avec VOTRE carte. Vous en serez propriétaire à 100%."

1. **Choix du domaine** : proposer 2-3 variations
   - `nomresto.fr` (idéal)
   - `nomresto-ville.fr` (si .fr pris)
   - `restaurant-nomresto.fr` (fallback)
2. **Registrar suggéré** : OVH ou Gandi (~12€/an)
3. **Procédure** :
   - Le patron crée un compte sur OVH (s'il n'en a pas)
   - Il achète le domaine avec **sa propre carte**
   - Coût : ~12€/an
   - Mike **rembourse les 12€ immédiatement** en espèces ou virement (les 12€ sont inclus dans les 490€ du Pack Solo, première année)
4. Mike note **uniquement les identifiants DNS** (pour pouvoir configurer Cloudflare Pages plus tard). Jamais le mot de passe registrar.

**Règle absolue** : Mike ne paie JAMAIS le domaine avec sa carte. Le patron est seul propriétaire (principe non-négociable #7). Si le patron insiste pour que Mike paie : refuser et expliquer "C'est important que ce soit à votre nom : le jour où vous voudriez changer de prestataire, vous gardez tout sans rien transférer."

→ Pas mapping settings : noter dans `brief.md` le domaine acheté + date.

---

## Sujet 12 — Accès gestionnaire Google Business (3 min)

> "Dernier point : l'accès à votre fiche Google. Vous restez propriétaire, je suis juste gestionnaire pour pouvoir l'optimiser."

1. Procédure : sur `business.google.com` → Paramètres → Personnes → Ajouter
2. Adresse mail à ajouter : **{l'adresse pro de Mike}**
3. Rôle : **Gestionnaire** (pas Propriétaire)
4. Vérifier que Mike reçoit le mail d'invitation et accepte sur place

**Note Mike** : ce sujet peut être technique pour certains patrons. Proposer : "Si vous préférez, on le fait ensemble depuis votre téléphone, ça prend 2 minutes."

→ Pas mapping settings : noter dans `brief.md` la date d'ajout + l'adresse mail utilisée.

---

## Récap final (5 min)

Avant de partir, lire au patron le **récap complet** du brief :

> "Donc pour résumer :
> - Votre site s'appellera {domaine}, mis en ligne sous 10 jours
> - Vous m'avez raconté votre histoire, j'ai noté {points clés}
> - Votre carte a {N sections, M plats}
> - Vos horaires sont {résumé}
> - {N photos} transférées
> - L'acompte de 245€ est encaissé en {forme}
> - Je suis gestionnaire de votre fiche Google
> - Je vous recontacte sous 5 jours pour un point d'avancement
> - Livraison prévue le {date+10 jours}
>
> J'ai oublié quelque chose ?"

Si le patron ajoute quelque chose : intégrer immédiatement dans le brief.md.

→ Le brief.md final reflète **exactement** ce qui a été validé oralement. C'est le contrat moral du contenu.
