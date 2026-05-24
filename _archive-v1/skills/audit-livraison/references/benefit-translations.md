# Table de traduction — métrique technique → bénéfice patron

Bibliothèque utilisée pour générer l'Output B (rapport patron). Chaque métrique technique a sa formulation en langage patron + phrase de bénéfice business. Le skill pioche ici, ne réinvente pas.

**Règle d'or :** une métrique n'apparaît dans le rapport patron QUE si elle est bonne (cf garde-fou #1). Si elle est mauvaise, elle reste dans l'audit interne seulement.

---

## Performance / Vitesse de chargement

**Terme patron :** "Vitesse de chargement"
**Seuil pour valoriser :** LCP ≤ 2,0 s (ou Performance ≥ 85)

- Phrase principale : *"Votre nouveau site s'affiche en **{X} seconde{s}** sur un téléphone."*
- Si snapshot eatbu : *"Votre ancien site prenait **{Y} secondes** — le nouveau est **{Z}× plus rapide**."*
- Bénéfice business : *"30 % des clients quittent un site qui met plus de 3 secondes à s'afficher. Avec un site rapide, vous gardez ces clients qui seraient partis voir ailleurs."*
- Variante mobile : *"7 clients sur 10 regardent votre resto depuis leur téléphone, souvent dans la rue en 4G. Votre site reste rapide même là."*

## SEO / Référencement Google

**Terme patron :** "Référencement Google" ou "visibilité sur Google"
**Seuil pour valoriser :** SEO ≥ 90

- Phrase principale : *"Score de référencement Google : **{X}/100**."*
- Si snapshot eatbu : *"Votre ancien site : {Y}/100."*
- Bénéfice business : *"Google comprend maintenant parfaitement votre menu, vos horaires et vos prix. Quelqu'un qui cherche « {spécialité} {ville} » a beaucoup plus de chances de tomber sur vous — avec votre menu affiché directement dans les résultats."*

## Accessibilité

**Terme patron :** "Lisibilité pour tous"
**Seuil pour valoriser :** Accessibilité ≥ 90

- Phrase principale : *"Score de lisibilité : **{X}/100**."*
- Bénéfice business : *"Une personne âgée ou malvoyante peut lire votre menu sans loupe ni zoom : tailles de texte et contrastes vérifiés. Une partie non négligeable de votre clientèle, surtout le midi en semaine."*

## Bonnes pratiques / Sécurité

**Terme patron :** "Site sûr et bien construit"
**Seuil pour valoriser :** Best Practices ≥ 95

- Phrase principale : *"Votre site est en HTTPS sécurisé, sans erreur technique, conforme aux standards du web."*
- Bénéfice business : *"Le petit cadenas dans la barre d'adresse rassure le client. Et Google pénalise les sites non sécurisés — le vôtre est carré."*

## Poids de la page

**Terme patron :** "Légèreté du site"
**Seuil pour valoriser :** poids ≤ 800 KB

- Phrase principale : *"Votre page d'accueil pèse **{X} KB** — l'équivalent d'une seule photo de téléphone."*
- Si snapshot eatbu : *"Votre ancien site en chargeait **{Y} KB** à chaque visite."*
- Bénéfice business : *"Vos clients ne consomment quasiment pas de données mobiles pour voir votre menu. Ça compte pour quelqu'un qui hésite à cliquer en 4G."*

## Édition autonome (pas une métrique Lighthouse, mais à valoriser systématiquement)

**Terme patron :** "Vous gardez la main"

- Phrase principale : *"Vous modifiez votre menu, vos horaires et vos photos vous-même, depuis **{URL}/admin/**, sans nous appeler et sans rien casser."*
- Bénéfice business : *"Changement de plat du jour, fermeture exceptionnelle, nouvelle photo : 30 secondes depuis votre téléphone. C'est à vous, vous ne dépendez de personne."*

## Schema.org / Données structurées (à valoriser si présent)

**Terme patron :** "Votre fiche directement dans Google"

- Phrase principale : *"Vos horaires, votre note, votre menu et vos prix sont lisibles par Google sous forme structurée."*
- Bénéfice business : *"Quand quelqu'un vous cherche, Google peut afficher « Ouvert jusqu'à 22h · ★ 4,7 · Menu à partir de 16 € » directement, sans même qu'il clique. C'est votre vitrine avant la vitrine."*

---

## Anti-patterns de formulation (à NE jamais écrire dans le rapport patron)

- ❌ "LCP de 1,2 s, CLS de 0,02, TBT de 90 ms" → jargon, illisible patron
- ❌ "Score Lighthouse de 96" tout court → un chiffre sans traduction ne parle pas
- ❌ "Votre ancien site était nul/catastrophique/amateur" → vexant, le patron l'a payé
- ❌ "Meilleur site de Chartres" / "imbattable" → superlatif invérifiable, casse la confiance
- ❌ Toute comparaison nominative avec un autre resto
- ✅ Toujours : chiffre réel → terme patron → conséquence concrète sur SES clients
