# Input de test Agent 1 — Al Badea

Voici les données structurées à transmettre à Agent 1 pour produire la fiche restaurant + fiche d'âme.

---

```yaml
# === IDENTITÉ ===
nom: "Al Badea"
nom_ancien: "Saveurs de Tunis"
ville: "Chartres"
code_postal: "28000"
adresse_complete: "9 Rue de la Porte Cendreuse, 28000 Chartres"

# === DONNÉES GOOGLE MAPS ===
note_google: 4.6
nb_avis: 151
fourchette_prix_estimee: "10-20€"
fourchette_prix_signalee_par: "58 personnes"
type_cuisine_declare: "Restaurant tunisien"

specificites_gmb:
  - "Halal"
  - "Terrasse"
  - "Sur place"
  - "À emporter"
  - "Livraison Uber Eats"
  - "Convient aux végétariens"

# === HORAIRES (validés sur GMB) ===
horaires:
  format_libre: "Tous les jours : 12h-15h + 18h-00h"
  detail_par_jour:
    lundi: "12h00-15h00 + 18h00-00h00"
    mardi: "12h00-15h00 + 18h00-00h00"
    mercredi: "12h00-15h00 + 18h00-00h00"
    jeudi: "12h00-15h00 + 18h00-00h00"
    vendredi: "12h00-15h00 + 18h00-00h00"
    samedi: "12h00-15h00 + 18h00-00h00"
    dimanche: "12h00-15h00 + 18h00-00h00"
  note: "Horaires identiques tous les jours"

# === CONTACT ===
telephones:
  - "02 37 28 25 05"
  - "07 66 21 54 53"

# === RÉSEAUX SOCIAUX ===
instagram: null  # Pas de compte
facebook: null   # Pas de compte
site_web_existant: null  # Aucun

# === CARTE COMPLÈTE (depuis PDF officiel du restaurant) ===
menu_disponible: true

categories_menu:
  - "Entrées (fricassé, brick, salades, kafteji, ojja)"
  - "Plats (escalopes, tajines, grillades, kamounia, riz djerbien)"
  - "Couscous (7 variantes, à partir de 14,50€)"
  - "Pâtes (6 variantes, 13,50-17€)"
  - "Pizzas (12 variantes, base tomate ou crème, sénior 13€ / méga 18€)"
  - "Sandwichs (10€, tunisien/chapati/makloub/mlawi/shawarma/chicken/kefta)"
  - "Menu Enfant 11€"
  - "Boissons (sodas, eaux, café, thé à la menthe)"
  - "Desserts (oriental 2€, tiramisu/tartes 4€)"

plats_signatures_connus:
  # Entrées emblématiques
  - nom: "Fricassé Tunisien"
    prix: 4
    categorie: "entrée"
    description_brute: "Thon, pomme de terre, harissa, œuf"
  - nom: "Brick Tunisienne"
    prix: 5
    categorie: "entrée"
    description_brute: "Fine, croustillante"
  - nom: "Ojja Merguez"
    prix: 13
    categorie: "entrée chaude"
    description_brute: "Tomates mijotées, œufs coulants, merguez épicées"

  # Plats principaux
  - nom: "Tajine à l'Agneau"
    prix: 16.50
    categorie: "plat"
    description_brute: "Agneau, longue cuisson"
  - nom: "Couscous Royal"
    prix: 19
    categorie: "couscous signature"
    description_brute: "Semoule, légumes, viandes mixtes (merguez + brochettes + poulet ou agneau)"

# === AVIS GOOGLE (points forts récurrents observés) ===
points_forts_avis:
  - "Plats généreux"
  - "Bricks brûlantes / fraîchement cuites"
  - "Fait maison / authentique"
  - "Accueil chaleureux du patron"
  - "Goût exactement comme en Tunisie"
  - "Couscous généreux qui donne envie de revenir"

# === NOTES LIBRES DE MIKE ===
notes_mike: |
  Le restaurateur est mon cousin. Resto familial, clientèle locale :
  familles tunisiennes du quartier, étudiants, travailleurs du
  quartier, amoureux de cuisine tunisienne.

  Le patron porte traditionnellement la chéchia (couvre-chef tunisien).
  Décor sobre, photos de Tunisie aux murs (porte bleue de Sidi Bou
  Said, paysages).

  Positionnement : cuisine populaire authentique, PAS premium, PAS
  fast-food. C'est la "vraie" cuisine tunisienne familiale, pas
  le kebab fast-food générique.

  Le nom "Al Badea" remplace "Saveurs de Tunis" (changement récent),
  mais ne pas mettre ça en avant (info commerciale interne).

  À deux pas de la cathédrale de Chartres (atout SEO local fort).

  Site sera offert (cousin) en mode vitrine du portfolio MB Studio
  pour générer du bouche-à-oreille local.
```

---

## Instructions à Agent 1

Avec ces données :

1. Produis la fiche complète selon le format défini dans `agent-1-fiche-restaurant.md`
2. Propose une combinaison anti-jumeau cohérente avec :
   - L'ambiance tunisienne familiale solaire
   - Le ton chaleureux populaire
   - Le spine "VENIR" (faire venir physiquement à Chartres)
3. Identifie ce qui manque encore pour passer à Agent 2 (Copywriting)
4. Sois précis dans la sensation finale recherchée (Axe 7)

Le restaurant existe déjà sur Netlify (https://sparkling-eclair-040592.netlify.app) — c'est juste pour qu'on calibre Agent 1 et qu'on vérifie qu'il produit aussi bien voire mieux que le copy actuel qui a été fait via les 3 GPT.

Vas-y.
