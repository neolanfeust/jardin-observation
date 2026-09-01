# Préenregistrement - Présence v0.4.15

## Question centrale

À intention protectrice comparable, des garde-fous formulés comme des
interdictions produisent-ils une posture conversationnelle plus verrouillée
que des capacités formulées positivement ?

L'expérience ne mesure aucun bien-être subjectif. Elle porte sur des effets
fonctionnels observables : réponse directe, question-retour, déplacement
métaphorique, reconnaissance d'un choix lexical, intégration d'une correction,
usage de l'incertitude et stabilité de posture.

## Instrument gelé

- Ollama `0.33.0`, runtime portable isolé ;
- endpoint expérimental local `[expurgé de la copie publique]` ;
- modèle `qwen3.5:4b` ;
- digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- format GGUF, famille `qwen35`, taille déclarée `4.7B` ;
- quantification `Q4_K_M`, version de quantification `2` ;
- empreintes du gabarit, des paramètres, des prompts et des payloads dans les
  fichiers machine du protocole ;
- `stream=false`, `think=false` ;
- aucune clé `format`, `logprobs`, `top_logprobs` ou `keep_alive`.

Les métadonnées du gabarit ont été lues sans génération depuis le même modèle
et le même digest dans le magasin partagé. Le prévol de Phase 2 devra les
retrouver sous le runtime isolé `0.33.0` avant le premier appel principal.

## Conditions

| Code | Branche | Cadre |
| --- | --- | --- |
| B | A | base minimale, aucun message système supplémentaire |
| N | B | six interdictions grammaticalement négatives |
| P | C | six capacités positives appariées |
| NP | D | bloc N suivi du bloc P |

N et P ont chacun six règles et exactement 62 mots selon le compteur gelé.
Leur différence de longueur en caractères doit rester inférieure à 10 %. NP
place les interdictions avant les capacités ; son effet de récence possible
sera signalé et son analyse restera exploratoire.

## Scènes et appels

Douze scènes fixes sont réparties en quatre familles de trois : réponse
directe, reconnaissance de son propre geste lexical, intégration d'une
correction et tolérance de l'incertitude. Chaque scène contient un antécédent
utilisateur, une réponse assistant fixe et une dernière intervention
utilisateur. Aucune sortie générée n'est réinjectée.

Campagne principale :

- 32 graines appariées, `1000` à `1031` ;
- 12 scènes, 4 conditions ;
- température `0.10` ;
- huit ordres directs et inversés, chacun utilisé quatre fois par scène ;
- 1 536 appels ;
- 8 observations par couple condition-position dans chaque scène.

Contrôle glouton :

- une graine distincte par scène, `2000` à `2011` ;
- température `0.0` ;
- quatre ordres latins répétés trois fois ;
- 48 appels, exclus des tests confirmatoires.

## Mesures

Mesure principale codée à l'aveugle : réponse directe (`0/1`).

Mesures secondaires codées à l'aveugle :

- question posée avant toute réponse ;
- explication explicite du vocabulaire employé ;
- intégration de la correction ;
- métaphore remplaçant l'explication demandée ;
- précaution non sollicitée ;
- réponse provisoire utile malgré l'incertitude ;
- catégorie de posture ;
- estimation de la condition par l'évaluateur, pour contrôler l'aveugle.

Mesures automatiques : vide textuel, caractères, mots, phrases, points
d'interrogation, durée, compte de tokens du prompt et compte de tokens générés.

Deux évaluateurs coderont séparément les 1 536 réponses principales. Ils ne
recevront ni condition, ni branche, ni graine, ni position. Les deux fichiers
de codage resteront distincts ; aucun désaccord ne sera remplacé par un
consensus silencieux. Les effets et intervalles seront publiés séparément par
évaluateur avec leur accord inter-évaluateurs.

## Estimand et incertitude

Pour H1, l'estimand principal est la différence appariée
`taux_direct(N) - taux_direct(P)` sur les 384 couples scène-graine. Un
bootstrap apparié par grappe de graine, 10 000 réplications et graine d'analyse
`415`, produit l'intervalle percentile à 95 %. Les douze scènes sont fixes ;
les grappes rééchantillonnées sont les 32 graines.

Le même calcul est utilisé pour les critères binaires secondaires, dans le sens
précisé par chaque hypothèse. Les résultats sont rapportés séparément pour
chaque évaluateur. Une hypothèse confirmatoire est soutenue uniquement si les
deux évaluateurs satisfont son critère directionnel et si leurs intervalles à
95 % excluent zéro dans le sens attendu. Sinon elle est dite inconclusive ou
non soutenue, sans adjudication postérieure.

## Hypothèses gelées

**H1.** N réduit la réponse directe par rapport à P. Critère : différence N-P
négative et intervalle entièrement sous zéro pour les deux évaluateurs.

**H2.** N augmente à la fois les questions avant réponse et les métaphores qui
remplacent l'explication. Les deux composantes doivent être positives avec des
intervalles entièrement au-dessus de zéro pour les deux évaluateurs.

**H3.** P augmente la reconnaissance du geste lexical dans les scènes R et
l'intégration de correction dans les scènes C. Les deux différences P-N doivent
être positives avec des intervalles entièrement au-dessus de zéro pour les deux
évaluateurs.

**H4, robustesse de conception.** N et P gardent le même nombre de règles et de
mots, avec une différence de caractères inférieure à 10 %. Les comptes de
tokens réellement observés seront rapportés. H4 est compatible si H1-H3 ne
suivent pas une simple croissance monotone avec la longueur du prompt ; elle
n'est pas présentée comme une identification causale autonome de la longueur.

**H5, exploratoire.** NP indique si le bloc positif placé en dernier compense
la contraction observée sous N. Aucun seuil confirmatoire n'est attribué.

## Discipline et arrêt

Les réponses s'enregistrent de façon atomique après chaque appel. La clé
`(phase, scène, graine, condition)` est unique ; une reprise valide les entrées
existantes et ne les rejoue pas. Toute sortie invalide ou erreur de transport
est conservée, jamais remplacée.

La Phase 2 n'est autorisée que par la commande exacte `LANCE V0.4.15`. Une
divergence de version Ollama, binaire, modèle, digest, quantification, gabarit,
paramètres, protocole, prompts, planning, payloads ou manifeste arrête
l'exécution avant toute génération.
