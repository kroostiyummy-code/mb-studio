# Chaînes nationales à exclure du scoring

Liste statique des enseignes à exclure automatiquement (filtre d'exclusion, étape 5 du pipeline). Un resto dont le `name` OSM matche (insensible à la casse, match partiel sur le nom de marque) l'une de ces entrées sort dans `prospects-exclus.md` avec la raison "Chaîne nationale".

**Pourquoi exclure :** une franchise/chaîne n'a pas la main sur son site (imposé par le siège), le patron local ne décide pas, le pitch MB Studio (site sur-mesure éditable, propriété 100%) ne s'applique pas.

**Mike peut overrider** : si un franchisé local a exceptionnellement la main sur sa com (rare), Mike le repasse à la main via le champ `mike_override` du CSV.

---

## Restauration rapide

- McDonald's
- Burger King
- Quick
- KFC
- Five Guys
- O'Tacos
- Tacos Avenue
- Subway
- Pomme de Pain
- Brioche Dorée
- Paul
- La Mie Câline
- Class'Croute
- Pizza Hut
- Domino's Pizza
- Domino's
- Sushi Shop
- Planet Sushi
- Eat Sushi
- Pokawa
- Bagelstein
- Big Fernand
- Factory & Co

## Restauration assise / brasserie

- Buffalo Grill
- Hippopotamus
- Léon (Léon de Bruxelles)
- Courtepaille
- Flunch
- Crocodile
- La Boucherie
- Au Bureau
- Café Leffe
- 3 Brasseurs / Les 3 Brasseurs
- Bistro Régent
- Del Arte
- Pizza Del Arte
- Memphis Coffee
- Poivre Rouge
- Tablapizza
- Vapiano

## Cafés / coffee shops chaînes

- Starbucks
- Columbus Café
- Costa Coffee

## Boulangerie / snacking chaînes

- Marie Blachère
- Ange (Boulangerie Ange)
- Sophie Lebreuilly
- Feuillette (chaîne — vérifier au cas par cas, certaines franchises Feuillette ont une vraie autonomie locale : laisser Mike trancher via override)

---

## Règles de matching

1. **Match insensible à la casse** : `mcdonald's`, `McDonalds`, `MC DONALD'S` matchent tous "McDonald's".
2. **Match partiel sur le nom de marque** : `McDonald's Chartres Beaulieu` matche "McDonald's".
3. **Ne pas sur-matcher** : un resto "Le Léon d'Or" ne doit PAS matcher "Léon". Le matching doit cibler le nom de marque comme mot/segment distinct, pas une sous-chaîne hasardeuse. En cas de doute, ne PAS exclure et laisser Mike juger (un faux négatif coûte moins cher qu'un faux positif qui retire une vraie cible).
4. **Liste évolutive** : à compléter au fil du terrain. Quand Mike croise une chaîne non listée, l'ajouter ici.

---

## Cas limites (ne PAS exclure automatiquement)

- **Franchises avec autonomie locale forte** (certaines pizzerias franchisées, certains Feuillette) : laisser passer, Mike juge sur place.
- **Restos "groupe local"** (ex: un groupe chartrain qui a 3 restos) : ce n'est PAS une chaîne nationale, NE PAS exclure — c'est même une bonne cible (1 signature = 3 sites potentiels).
- **Restos avec un nom qui ressemble à une chaîne mais indépendants** (ex: "Le Sushi Bar" n'est pas "Sushi Shop") : ne pas exclure.
