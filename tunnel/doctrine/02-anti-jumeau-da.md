# 02 — Garde-fou anti-jumeau

## Le problème à résoudre

MB Studio promet : *"Aucun site MB Studio ne ressemble à un autre."*

Sans garde-fou systématique, deux sites finiront par se ressembler par hasard :
- Deux restos méditerranéens auront tendance à hériter des mêmes couleurs chaudes
- Deux bistrots auront tendance à utiliser la même typo serif
- Deux foodtrucks auront tendance à reprendre la même structure courte

Ce hasard est notre ennemi. Il faut le rendre impossible structurellement.

## Le système : matrice de combinaisons uniques

Chaque site est défini par une **combinaison de 5 dimensions**. Deux clients ne peuvent jamais avoir la même combinaison.

### Dimension 1 — Direction Artistique (DA)

8 DA disponibles dans le catalogue MB Studio :

1. **Dark Lounge** — Nocturne, intimité chaude, marbre noir, cuivre, velours (réf. Anamour)
2. **Bistrot Patine** — Bois ancien, ardoise, lumière douce, traditions françaises
3. **Méditerranéen Solaire** — Blanc cassé, bleu Sidi Bou Said, terre cuite, chaleur diurne (réf. Al Badea)
4. **Tropical Vivant** — Couleurs saturées, madras, motifs ethniques, soirée festive (réf. La Casa Tropical)
5. **Gastro Marbre** — Marbre clair, typographie serif fine, espaces aérés, élégance contemporaine
6. **Tradition Bois** — Bois brut, ferronnerie, textures rustiques, ambiance terroir
7. **Fast-Casual Pop** — Couleurs pop, typographie display, rythme rapide, énergie dopamine (réf. Kroosti)
8. **Editorial Magazine** — Typographie magazine, photos pleine page, ambiance contemplative (réf. Terra)

### Dimension 2 — Pack typographique

6 packs typo disponibles, chacun avec une famille principale + une secondaire :

1. **Editorial** — Playfair Display + Inter
2. **Modern Soft** — Cormorant Garamond + Manrope
3. **Bistrot Classic** — Libre Caslon Text + Work Sans
4. **Display Bold** — Anton + Source Sans Pro
5. **Lounge Sensuel** — Cinzel + Lora
6. **Pop Energique** — Archivo Black + IBM Plex Sans

### Dimension 3 — Structure de hero

5 structures de hero possibles :

1. **Direct** — Headline + sous-titre + CTA, photo plein écran en arrière-plan
2. **Editorial** — Photo dominante + texte côté, mise en page magazine
3. **Cinématique** — Photo plein écran + texte minimal flottant, ambiance film
4. **Split** — 50/50 photo/texte, structure équilibrée
5. **Carrousel ambiance** — Plusieurs photos défilantes + texte fixe

### Dimension 4 — Spine commercial (CTA dominant)

5 spines possibles selon la fonction principale du commerce :

1. **VENIR** — Pour les restos qui veulent du passage (CTA "Nous trouver", "Voir le plan")
2. **RÉSERVER** — Pour les restos qui veulent maîtriser leurs services (CTA "Réserver une table")
3. **APPELER** — Pour les restos sans réservation en ligne (CTA "Appeler maintenant")
4. **COMMANDER** — Pour les restos avec vente à emporter ou livraison (CTA "Commander")
5. **DÉCOUVRIR** — Pour les restos nouveaux qui veulent éduquer le marché (CTA "Voir la carte")

### Dimension 5 — Ton de copy

5 tons possibles :

1. **Sensoriel premium** — Phrases courtes, lexique sensoriel, élévation poétique mesurée
2. **Chaleureux populaire** — Tutoiement parfois, lexique du quotidien, proximité humaine
3. **Éditorial discret** — Phrases longues, vocabulaire riche, distance respectueuse
4. **Pop énergique** — Phrases courtes, points d'exclamation maîtrisés, dopamine
5. **Tradition assumée** — Vocabulaire ancien, références patrimoniales, ancrage terroir

## La règle de combinaison

**Aucun nouveau client ne peut avoir une combinaison identique à un client existant sur les 5 dimensions.**

Au minimum **2 dimensions sur 5 doivent différer** entre deux clients du même type de cuisine.

## Le registre des combinaisons

Un fichier `registre-clients.yml` à la racine du projet MB Studio liste toutes les combinaisons utilisées :

```yaml
clients:
  - slug: "al-badea-chartres"
    type_cuisine: "tunisien"
    ville: "Chartres"
    da: "Mediterraneen_Solaire"
    pack_typo: "Bistrot_Classic"
    structure_hero: "Editorial"
    spine: "VENIR"
    ton_copy: "Chaleureux_populaire"
    date_livraison: "2026-05-22"

  - slug: "anamour-luce"
    type_cuisine: "turc_moderne"
    ville: "Lucé"
    da: "Dark_Lounge"
    pack_typo: "Lounge_Sensuel"
    structure_hero: "Cinematique"
    spine: "RESERVER"
    ton_copy: "Sensoriel_premium"
    date_livraison: "2026-05-XX"

  - slug: "la-casa-tropical-chartres"
    type_cuisine: "afro_caribeen"
    ville: "Chartres"
    da: "Tropical_Vivant"
    pack_typo: "Pop_Energique"
    structure_hero: "Carrousel_ambiance"
    spine: "RESERVER"
    ton_copy: "Chaleureux_populaire"
    date_livraison: "2026-05-XX"
```

## Le script de vérification

Avant chaque nouveau client, le script `check-unicite.py` (ou commande Claude Code) vérifie :

1. La nouvelle combinaison est-elle déjà présente dans le registre ?
2. Combien de dimensions partagées avec chaque client existant ?
3. Si plus de 3/5 dimensions partagées avec un client existant → alerte rouge
4. Si même type de cuisine ET moins de 2 dimensions de différence → blocage

Output type :

```
NOUVEAU CLIENT : pizza-tonino-chartres
Type cuisine : italien
Combinaison proposée :
  DA: Bistrot_Patine
  Typo: Editorial
  Hero: Direct
  Spine: VENIR
  Ton: Chaleureux_populaire

VÉRIFICATION :
  vs al-badea-chartres : 1/5 dimensions partagées → OK
  vs anamour-luce : 0/5 dimensions partagées → OK
  vs la-casa-tropical : 0/5 dimensions partagées → OK

→ COMBINAISON VALIDÉE
```

## Cas particulier : restaurants du même type de cuisine

Si on signe deux restos italiens, le risque de jumeau est plus élevé.

**Règle renforcée** : pour deux restos du même type de cuisine, au minimum **3 dimensions sur 5 doivent différer**.

Exemple : si Pizza Tonino utilise DA Bistrot Patine + Typo Editorial + Hero Direct, alors le prochain resto italien devra avoir au moins 3 dimensions différentes (par exemple DA Méditerranéen Solaire + Typo Lounge Sensuel + Hero Cinématique).

## Cas particulier : ville unique

Pour deux restos de la même ville (même petite, comme Chartres), la règle stricte s'applique : **2 dimensions différentes minimum**, idéalement 3 sur 5.

L'enjeu : un client de Chartres qui voit deux sites MB Studio de Chartres ne doit jamais penser "ils se ressemblent". Sinon notre promesse d'unicité s'écroule localement.

## L'évolution du catalogue

Quand le catalogue de combinaisons commence à saturer (5+ clients dans la même ville, 8+ clients du même type de cuisine), il faut **étendre les dimensions** :

- Ajouter des sous-variantes dans chaque DA (Dark Lounge cuivré / Dark Lounge bordeaux)
- Ajouter des packs typo supplémentaires
- Inventer des structures de hero hybrides

Ce travail d'extension fait partie de la maintenance MB Studio. Il garantit que la promesse d'unicité tient même à 50 clients.

## Le test ultime

Avant chaque livraison, faire le **test des deux onglets** :

1. Ouvrir le nouveau site dans un onglet
2. Ouvrir un site existant MB Studio dans l'onglet d'à côté
3. Demander : *"Quelqu'un qui ne sait rien de MB Studio devinerait-il que c'est le même studio ?"*

Si la réponse est "facilement oui" → les sites se ressemblent trop, refonte d'au moins 2 dimensions nécessaire.
Si la réponse est "peut-être à la signature en bas" → parfait, c'est ce qu'on veut.
Si la réponse est "impossible à deviner" → encore mieux, l'unicité est totale.
