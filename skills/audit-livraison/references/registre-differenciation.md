# Registre de différenciation inter-clients

Mémoire du standard non-négociable d'unicité (principe #10 de `CLAUDE.md` + `differenciation-clients.md`). Alimenté **automatiquement** par `audit-livraison` (étape 7bis) **après chaque livraison validée** (0 🔴). Une ligne = un site réellement livré.

Ne pas éditer à la main sauf correction exceptionnelle. Commité **fichier par fichier** (jamais en bloc). Le registre doit toujours refléter le **livré réel** — c'est la base de comparaison du garde-fou anti-jumeau.

Règle de blocage (rappel) : 🔴 si un site déjà livré **dans la même ville** partage `signature` + `variante_hero` + `ordre_sections` identiques ET une `dominante` proche → changer au moins deux axes avant livraison.

`signature` ∈ { fast-food, gastro, traditionnel }.

## Sites livrés

| slug | ville | cuisine | signature | variante_hero | pack_typo | dominante | ordre_sections | date_livraison |
|---|---|---|---|---|---|---|---|---|
| _(vide — première ligne ajoutée à la 1ʳᵉ livraison validée)_ | | | | | | | | |
