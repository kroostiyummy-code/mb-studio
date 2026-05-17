# Brief client — {NOM_DU_RESTO}

**Date du brief :** {DATE}
**Lieu :** {ADRESSE_DU_RESTO}
**Présent côté MB Studio :** Mike
**Présent côté patron :** {NOM_DU_PATRON}, {FONCTION}
**Signature retenue :** {fast-food | gastro | traditionnel}
**Dominante :** {HEX_COULEUR}

---

## 1. Identité

- **Nom officiel :** {NOM}
- **Slogan court :** {SLOGAN}
- **Baseline :** {BASELINE_OU_VIDE}
- **Année de lancement :** {YYYY}
- **Ville :** {VILLE}
- **Code région :** {FR-XX}
- **Téléphone (E.164) :** {+33XXXXXXXXX}
- **Téléphone (affichage) :** {XX XX XX XX XX}

---

## 2. Histoire du resto

> {2-3 PHRASES NARRATIVES — version reformulée par Mike, validée par le patron}

**Phrase d'accroche découpée :**
- Lead : "{LEAD}"  (ex: "N°1 à", "Depuis trois", "Cuisine du")
- Accent : "{ACCENT}"  (ex: "Chartres.", "générations.", "marché.")

**Body avec emphases (syntaxe `**mot**`) :**
> {BODY_AVEC_EMPHASES}

**Année à mettre en avant :** {YYYY}

---

## 3. Carte

### Combo / Formule mise en avant

- **Activé :** {oui | non}
- **Étiquette :** {ex: "★ COMBO", "Menu du jour"}
- **Composition :** {ex: "RIZ + CROQ + BOISSON", "Entrée + Plat + Dessert"}
- **Prix :** {XX,XX €}

### Sections du menu

#### Section 1 — {NOM_SECTION} (ordre 1)

| Plat | Description | Prix | Allergènes |
|---|---|---|---|
| ... | ... | ... | ... |

#### Section 2 — {NOM_SECTION} (ordre 2)

| Plat | Description | Prix | Allergènes |
|---|---|---|---|
| ... | ... | ... | ... |

> Etc. — ajouter une section par catégorie de menu.

---

## 4. Adresse et horaires

- **Mode :** {fixe | foodtruck}
- **Adresse :** {ADRESSE_COMPLETE}
- **Coordonnées GPS :** {LAT}, {LNG}
- **Lien Maps embed :** {URL_EMBED_OU_A_GENERER}

### Si mode fixe

| Jour | Créneaux |
|---|---|
| Lundi | {fermé / 12:00-14:00 / 19:00-22:30} |
| Mardi | ... |
| Mercredi | ... |
| Jeudi | ... |
| Vendredi | ... |
| Samedi | ... |
| Dimanche | ... |

### Si mode foodtruck

| Jour | Créneau Midi | Créneau Soir |
|---|---|---|
| Lundi | {fermé / lieu, ville, HH:MM-HH:MM} | {idem} |
| Mardi | ... | ... |
| Mercredi | ... | ... |
| Jeudi | ... | ... |
| Vendredi | ... | ... |
| Samedi | ... | ... |
| Dimanche | ... | ... |

---

## 5. Réseaux sociaux et avis Google

- **Instagram :** {URL_OU_VIDE}
- **Facebook :** {URL_OU_VIDE}
- **TikTok :** {URL_OU_VIDE}
- **Snapchat :** {URL_OU_VIDE}
- **Note Google :** {X.X / 5}
- **Nombre d'avis :** {NNN}
- **URL fiche Google :** {URL_GMB}

> Si note < 4.0 OU avis < 20 → le bloc Avis sera auto-caché (voir conditions.ts du template).

---

## 6. Photos transférées

| # | Fichier | Description (alt) | Légende (optionnelle) | Usage |
|---|---|---|---|---|
| 1 | `hero.jpg` | {DESCRIPTION} | — | Hero |
| 2 | `galerie-01.jpg` | {DESCRIPTION} | {LEGENDE} | Galerie |
| 3 | `galerie-02.jpg` | ... | ... | Galerie |
| ... | ... | ... | ... | ... |

**Total photos galerie :** {N}
**Statut galerie :** {active (≥ 4 photos) | auto-cachée (< 4 photos)}

---

## 7. Bandeau actualités

- **Activé :** {oui | non}
- **Messages :** (3 à 6)
  1. {MESSAGE_1}
  2. {MESSAGE_2}
  3. ...

---

## 8. Notre exigence

- **Activé :** {oui | non}
- **Titre (3 lignes) :**
  1. {LIGNE_1}
  2. {LIGNE_2 — peut contenir `**mot**` pour emphase}
  3. {LIGNE_3}
- **Checklist (4-6 items) :**
  - {ITEM_1}
  - {ITEM_2}
  - ...
- **Bannière finale (optionnelle) :**
  - Titre : {TITRE_OU_VIDE}
  - Sous-titre : {SOUS_TITRE_OU_VIDE}

---

## 9. Réservation

- **Kicker (accroche) :** {TEXTE_OU_DEFAUT}
- **Titre :** {TEXTE_OU_DEFAUT}
- **Perks (3 max) :**
  1. {PERK_1}
  2. {PERK_2}
  3. {PERK_3}

---

## 10. Acompte 245€

- **Forme :** {espèces | virement | chèque}
- **Date d'encaissement :** {DATE}
- **Reçu remis au patron :** {oui | non}
- **Notes :** {NOTES_LIBRES}

---

## 11. Nom de domaine

- **Domaine acheté :** {nomresto.fr}
- **Registrar :** {OVH | Gandi | autre}
- **Compte propriétaire :** **PATRON** (jamais Mike)
- **Date d'achat :** {DATE}
- **Coût :** {XX €/an}
- **Remboursement au patron par Mike :** {oui, en espèces / non encore}
- **Notes DNS :** {notes pour configuration Cloudflare Pages — pas le mot de passe registrar !}

---

## 12. Accès Google Business

- **Mike ajouté en :** Gestionnaire (jamais Propriétaire)
- **Adresse mail utilisée :** {EMAIL_MIKE}
- **Date d'ajout :** {DATE}
- **Confirmation reçue :** {oui | non}

---

## Notes libres de Mike (post-brief)

> {Observations sur le patron, sa motivation, son ton, ses préférences exprimées, des anecdotes utiles pour personnaliser la production. Ces notes ne sont PAS partagées avec le patron.}

---

## Points restant à clarifier (si quelque chose était flou)

> {Liste des points où le patron a hésité ou n'a pas su répondre. Mike contactera par SMS ou attendra la livraison. Aucun point ne doit bloquer le démarrage de la production.}

---

## Récap validé oralement par le patron à la fin du brief

> "Pour résumer : votre site s'appellera {domaine}, mis en ligne le {date+10}. Carte avec {N plats}. {N photos}. Acompte de 245€ encaissé en {forme}. Vous me revoyez à la livraison."

**Validation patron :** {oui | non — si non, lister les ajustements}
