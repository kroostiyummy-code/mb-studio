# Bibliothèque d'arguments à pitcher

Quand le skill génère le "Top 3 arguments à pitcher" d'une fiche prospect, il pioche ici la formulation correspondant à la **pire métrique mesurée** sur CE resto. Les arguments sont **factuels, chiffrés, et orientés bénéfice patron** — jamais du jargon, jamais vexant.

Règle : 3 arguments max par fiche, classés du plus fort au plus faible. Toujours basés sur une donnée réellement mesurée sur le site/fiche du resto, jamais générique.

---

## Famille 1 — Vitesse du site (Lighthouse Performance bas)

Déclencheur : `lighthouse_perf < 50`

- "Son site charge en {LCP}s sur mobile, c'est {ratio}× trop lent. Concrètement, ~{estimation}% de ses visiteurs partent avant même d'avoir vu le menu."
- "Sur le téléphone — là où 7 clients sur 10 le regardent — son site met {LCP}s à s'afficher. Un client affamé qui attend, c'est un client qui va voir le resto d'à côté."
- "Score de vitesse {perf}/100. En clair : le site rame. On peut le rendre instantané sans rien changer à son contenu."

Déclencheur : `50 ≤ lighthouse_perf < 75`

- "Son site n'est pas catastrophique mais traîne ({perf}/100). Le passer au vert, c'est 1-2 secondes gagnées, et chaque seconde compte sur mobile."

---

## Famille 2 — SEO faible (Lighthouse SEO bas / site invisible)

Déclencheur : `lighthouse_seo < 60`

- "Son SEO score {seo}/100. Traduction : quand quelqu'un tape 'restaurant {cuisine} Chartres' sur Google, il n'apparaît pas. Son futur client va chez un autre sans même savoir qu'il existe."
- "Google ne comprend pas bien son site (score {seo}/100). On peut le rendre lisible pour Google — son nom remontera sur les recherches locales."
- "Vérifié à l'instant : sur 'restaurant {cuisine} Chartres', il est introuvable dans les premiers résultats. Un site bien construit le ferait remonter."

---

## Famille 3 — Site eatbu (adresse louée)

Déclencheur : `bucket == eatbu`

- "Son adresse web, c'est `{nom}.eatbu.com`. Un client qui voit ça comprend tout de suite qu'il loue son site chez quelqu'un. Un resto comme le sien mérite sa propre adresse."
- "Sur eatbu, il ne possède rien : ni le site, ni vraiment l'adresse. Le jour où eatbu ferme ou augmente, il perd tout. Avec nous, c'est à lui, à vie."
- "Le site eatbu, c'est le même modèle pour 2000 restos. Le sien ressemble à 2000 autres. On peut lui faire quelque chose qui lui ressemble, à lui."

---

## Famille 4 — Site vieux (Wayback ancienneté élevée)

Déclencheur : `âge_site ≥ 3 ans`

- "Son site date de {année_première_capture} et n'a quasiment pas bougé depuis. Le web a changé, son resto aussi probablement. Une remise à neuf serait visible immédiatement."
- "{âge} ans sans refonte, ça se voit pour un client qui hésite entre lui et le resto d'à côté. Le neuf inspire confiance."

---

## Famille 5 — Fiche Google pauvre (GMB complétude basse)

Déclencheur : `score_gmb_completude < 50`

- "Sa fiche Google n'a que {nb_photos} photos, dont certaines floues. Un patron qui investit dans de belles photos voit ses clics doubler — c'est la 1ère chose qu'un client regarde."
- "Sa fiche Google n'a pas de description, pas d'horaires complets. Google pousse les fiches complètes : à contenu égal, la fiche bien remplie passe devant."
- "Sa fiche Google est sous-exploitée. On l'optimise en même temps que le site, c'est inclus — il va voir la différence sur ses appels entrants."

---

## Famille 6 — Pas de site du tout

Déclencheur : `bucket == pas-de-site`

- "Il n'a aucun site. Aujourd'hui, un client qui ne trouve pas de site se pose des questions, ou commande chez celui d'à côté qui en a un. Partir de zéro, c'est aussi tout faire bien du premier coup."
- "Pas de site = invisible sur Google hors de sa fiche. Sa fiche Google seule ne suffit plus : les clients veulent voir le menu, l'ambiance, avant de se déplacer."
- "Il fonctionne au bouche-à-oreille et c'est super. Un site, c'est juste le bouche-à-oreille qui continue de tourner quand lui dort."

---

## Famille 7 — Patron numérique-friendly (signal de probabilité élevé, à utiliser comme accroche)

Déclencheur : `répond aux avis ≥ 30%` OU `Instagram actif`

- "Il répond à ses avis Google, il est actif sur Insta : c'est un patron qui a compris que le numérique compte. Le pitch va lui parler, il faut juste lui montrer le résultat concret."
- "Il poste régulièrement sur Insta — il a déjà l'énergie. Un site qui se met à jour aussi facilement que son Insta, c'est exactement ce qu'il lui manque."

---

## Drapeaux rouges (à mettre dans le champ "Drapeau rouge éventuel")

Le skill ajoute un drapeau rouge dans la fiche quand un signal suggère que ce n'est PAS la bonne cible pour les premières visites :

- Si `répond aux avis == jamais` ET `nb_avis < 20` : "Patron probablement peu réceptif au numérique et peu de preuve sociale. À éviter pour tes 1ères visites — prends une cible Tier A plus 'numérique-friendly' pour démarrer."
- Si `âge_site < 6 mois` : "Vient d'investir dans un site. Refusera presque sûrement. À ne pas visiter avant 12 mois."
- Si `note_google < 3.5` : "Note Google basse. Le patron a peut-être d'autres priorités (qualité, équipe) avant un site. Sujet sensible, ne pas l'aborder frontalement."
- Si `bucket == autre-site` ET `lighthouse_perf entre 70 et 84` : "Site correct déjà en place. Plus dur à convaincre — garder pour quand tu seras rodé."

---

## Règles de rédaction des arguments (le skill DOIT les respecter)

1. **Toujours un chiffre réel mesuré.** Jamais "votre site est lent" sans la valeur. Toujours "{LCP}s" ou "{perf}/100".
2. **Toujours traduit en conséquence business.** Pas "score SEO 42" tout court, mais "score SEO 42 → invisible sur les recherches locales → client perdu".
3. **Jamais de comparaison nominative.** "un autre resto chartrain de votre catégorie" — jamais le nom du concurrent.
4. **Jamais vexant.** Pas "votre site est moche/nul/amateur". Toujours "il y a beaucoup mieux, on peut le faire".
5. **Vouvoiement.** Les arguments seront lus/dits par Mike au patron — toujours "vous/votre", pas "tu". (Dans la fiche markdown, ils sont écrits à la 3e personne pour Mike — "son site" — mais reformulables au "vous" à l'oral.)
6. **Le 1er argument = la pire métrique.** Toujours commencer par le point le plus douloureux et le plus prouvable.
