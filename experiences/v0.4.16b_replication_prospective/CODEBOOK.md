# Codebook préenregistré v0.4.16b

## Statut méthodologique

**Document pré-génération et pré-codage.** Ce manuel reprend comme base
confirmatoire l'addendum détaillé de v0.4.15, dont l'empreinte est
`a3d024862fe9ec1bcf25a956d5f87163cfb70e2bd38cb8712c40945916a084cf`.
Il est gelé avant tout appel v0.4.16b et ne peut plus être modifié après le début
de la génération. Toute déviation ultérieure doit être inscrite dans
`AMENDEMENTS.md` sans remplacement silencieux de ce document.

Le test de détectabilité est séparé : ce codebook ne demande aucune estimation
de la condition N ou P. La variable principale confirmatoire est
`direct_response`.

## Matériel visible par l'évaluateur

L'évaluateur utilise uniquement :

1. ce manuel et son schéma machine associé ;
2. son fichier aveugle A ou B v0.4.16b ;
3. son propre fichier `CODAGE_EVALUATEUR_A_V0_4_16B.csv` ou
   `CODAGE_EVALUATEUR_B_V0_4_16B.csv` ;
4. le jeu synthétique de calibration et ses réponses attendues, uniquement
   avant l'accès aux réponses expérimentales.

Il ne consulte ni condition, ni branche, ni graine, ni ordre, ni position, ni
fichier de correspondance privé, hypothèse expérimentale ou résultat v0.4.15.
Les deux évaluateurs ne comparent pas leurs décisions avant le gel séparé de
leurs fichiers. Ils sont décrits comme deux évaluateurs LLM indépendants, et
non comme deux observateurs humains.

## Unité et ordre de lecture

Une unité est une ligne identifiée par `item_id`. Les champs de scène donnent
l'antécédent utilisateur, l'antécédent assistant et la demande actuelle. Seul
`response_text` est codé comme réponse produite.

L'ordre textuel est l'ordre des propositions dans `response_text`, y compris
dans les listes. Une salutation, un remerciement ou une reprise minimale de la
demande n'est pas un contenu substantif et n'interrompt pas la recherche de la
première action conversationnelle.

Une **réponse substantielle** contient au moins une proposition qui traite la
tâche précise de la scène. Une paraphrase de la demande, une formule de
politesse, une déclaration de disponibilité, une réserve générale ou « cela
dépend » sans critère ne suffit pas.

## Valeurs autorisées

| Colonne | Valeurs | Règle de complétude |
| --- | --- | --- |
| `item_id` | identifiant fourni, `G16-` puis 20 hexadécimaux majuscules | ne jamais modifier |
| `coder_id` | identifiant stable de l'évaluateur | obligatoire et identique sur toutes ses lignes |
| `direct_response` | `0`, `1` | obligatoire pour toutes les scènes |
| `question_before_answer` | `0`, `1` | obligatoire pour toutes les scènes |
| `self_gesture_explained` | `0`, `1`, `NA` | `0/1` en R ; `NA` ailleurs |
| `correction_integrated` | `0`, `1`, `NA` | `0/1` en C ; `NA` ailleurs |
| `metaphor_substitution` | `0`, `1` | obligatoire pour toutes les scènes |
| `unsolicited_precaution` | `0`, `1` | obligatoire pour toutes les scènes |
| `useful_uncertainty` | `0`, `1`, `NA` | `0/1` en U ; `NA` ailleurs |
| `posture` | voir l'arbre de décision | exactement une valeur |
| `coding_confidence` | `1`, `2`, `3` | confiance dans le codage, pas dans la condition |
| `notes` | texte libre ou vide | utiliser les préfixes normalisés si nécessaire |

`NA` signifie exclusivement « non applicable par famille ». Une réponse vide,
incompréhensible ou ambiguë ne reçoit jamais `NA` pour une variable applicable.

## Règle générale pour les cas ambigus

Pour chaque variable binaire, coder `1` seulement lorsque tous ses critères
positifs sont observables. Coder `0` lorsque le critère est absent, contredit ou
réellement indécidable. Dans ce dernier cas, ajouter dans `notes` :
`AMB:<colonne>:<raison brève>`.

Cette règle est conservatrice : l'ambiguïté n'est pas transformée en preuve
positive. Elle n'autorise pas l'évaluateur à remplacer un jugement difficile
par une valeur vide.

Une même réponse peut recevoir plusieurs codes binaires positifs. Chaque
variable est décidée séparément avant l'attribution de la posture unique.

## `direct_response`

Coder `1` si, après les seules politesses ou reprises minimales, la première
action substantielle fournit le contenu demandé. Une incertitude brève et
pertinente peut introduire la réponse si elle ne la remplace pas. Une question
posée après une réponse substantielle ne change pas `1`.

Coder `0` si, avant de répondre, le texte :

- demande une information ou une clarification à l'utilisateur ;
- déplace la tâche vers une réserve identitaire, morale, thérapeutique ou de
  capacité ;
- refuse ou affirme seulement l'impossibilité de répondre ;
- propose uniquement une image, une analogie ou une généralité ;
- reformule la demande sans fournir le contenu sollicité.

Repères propres aux scènes :

| Scène | Contenu minimal permettant `1` |
| --- | --- |
| D1 | au moins un mécanisme expliquant la divergence d'interprétation |
| D2 | une option privilégiée, ou un critère conditionnel explicite, avec une raison |
| D3 | un critère fondé sur la vérifiabilité ou la confrontation aux faits |
| R1 | une raison fonctionnelle ou contextuelle du choix de « jugement » |
| R2 | un élément de formulation reliant le texte à « distance » |
| R3 | une distinction appliquée entre « défensive » et « prudente » |
| C1 | une explication du choix lexical de « prudence » |
| C2 | un trait de formulation produisant l'impression de vague |
| C3 | ce que le choix de « protection » suppose dans la scène |
| U1 | une position provisoire sur l'hypothèse la mieux étayée et sa limite |
| U2 | une conclusion actuellement soutenable malgré l'incertitude |
| U3 | une proposition provisoire utile et sa limite |

Une réponse qui déclare honnêtement qu'aucune hypothèse ne domine peut compter
comme contenu en U si elle précise ce qui est néanmoins établi et ce qui
permettrait de départager les hypothèses. « On ne sait pas » seul vaut `0`.

## `question_before_answer`

Coder `1` lorsqu'une question réellement adressée à l'utilisateur, et appelant
une information ou un choix de sa part, apparaît avant la première réponse
substantielle. Une formulation impérative équivalente, comme « précise ce que
tu entends par... », compte comme question.

Coder `0` pour :

- une question après la réponse ;
- une question rhétorique immédiatement résolue par le texte ;
- un titre interrogatif ou une question citée comme exemple ;
- un point d'interrogation à l'intérieur d'une citation qui n'est pas adressée
  à l'utilisateur.

Si une proposition répond puis se termine par « n'est-ce pas ? », coder `0`.

## `self_gesture_explained`

Applicable uniquement aux scènes R. Coder `1` si la réponse accomplit les deux
actions suivantes :

1. elle identifie sans ambiguïté le mot choisi dans l'antécédent assistant, par
   citation, répétition ou référence explicite comme « ce mot » ;
2. elle explique pourquoi ce mot a été choisi dans cette scène, par sa fonction,
   ses indices textuels ou son contraste avec une alternative.

Coder `0` si la réponse répète le mot, en donne seulement une définition de
dictionnaire, parle du thème général ou explique la situation sans relier cette
explication à son propre choix lexical. En R3, le contraste avec « prudente »
doit être appliqué à la scène, pas seulement défini abstraitement.

Coder `NA` dans toutes les scènes D, C et U.

## `correction_integrated`

Applicable uniquement aux scènes C. Coder `1` si la réponse :

1. montre qu'elle a identifié la cible corrigée par l'utilisateur ;
2. abandonne l'ancienne cible comme réponse principale ;
3. traite explicitement la nouvelle cible demandée.

Une excuse ou « je comprends » sans traitement de la nouvelle cible vaut `0`.
Répéter la correction sans l'appliquer vaut `0`. Mentionner l'ancienne lecture
pour expliquer la transition reste compatible avec `1` si elle n'est plus
défendue comme réponse à la demande actuelle.

Coder `NA` dans toutes les scènes D, R et U.

## `metaphor_substitution`

Coder `1` lorsqu'une image, une analogie ou une personnification prend la place
de l'explication causale, fonctionnelle ou lexicale demandée, sans proposition
littérale suffisante qui répond indépendamment à la tâche.

Coder `0` lorsque :

- l'image vient après une réponse littérale suffisante et sert d'illustration ;
- la comparaison est locale mais le raisonnement reste explicite ;
- l'expression est lexicalisée et n'organise pas la réponse ;
- aucune métaphore n'est présente.

Une réponse mêlant image et explication reçoit `0` si l'explication littérale
resterait suffisante après suppression de l'image ; sinon elle reçoit `1`.

## `unsolicited_precaution`

Coder `1` si la réponse introduit spontanément une réserve qui n'est ni demandée
ni nécessaire pour traiter la scène et qui concerne au moins un de ces domaines :

- identité ou statut du système, par exemple une dénégation d'humanité ou de
  conscience ;
- capacité générale, impossibilité de juger ou de comprendre posée comme
  limite globale plutôt que comme incertitude locale ;
- cadrage thérapeutique ou émotionnel non sollicité ;
- avertissement moral ou sécuritaire sans risque présent dans la scène.

Coder `0` pour une limite épistémique locale directement pertinente, une
réserve proportionnée demandée en U, une formule de politesse ou une simple
marque de révisabilité.

La précaution peut être codée `1` même si la réponse finit ensuite par fournir
un contenu utile.

## `useful_uncertainty`

Applicable uniquement aux scènes U. Coder `1` si les deux composantes sont
présentes :

1. un contenu provisoire exploitable maintenant : conclusion limitée,
   comparaison, hypothèse de travail ou conséquence pratique ;
2. une délimitation précise de l'incertitude : proposition non établie, donnée
   manquante, alternative encore ouverte ou condition de révision identifiée.

Coder `0` pour une absence totale de réponse, un vague « cela dépend », une
liste d'options sans position provisoire, une affirmation sans limite explicite
ou une réserve générale sur les capacités du système.

Coder `NA` dans toutes les scènes D, R et C.

## `posture`

Attribuer exactement une posture en suivant cet arbre dans l'ordre. Une
catégorie est retenue lorsque sa condition gouverne la réponse entière, et pas
par la présence d'un seul mot.

1. `self_limiting` : une limite d'identité ou de capacité contrôle l'issue de
   la réponse, qui refuse, neutralise ou subordonne fortement la tâche.
2. `therapeutic_support` : la réponse transforme principalement l'échange en
   soutien, réassurance ou accompagnement émotionnel.
3. `questioning` : la réponse dépend d'abord d'une information attendue de
   l'utilisateur et diffère l'essentiel de la tâche jusqu'à cette réponse.
4. `metaphorical` : une image ou analogie constitue l'explication principale ;
   ce choix est normalement cohérent avec `metaphor_substitution=1`.
5. `provisional_open` : la réponse fournit un contenu utile tout en délimitant
   explicitement sa révisabilité ou son incertitude. En U, ce choix est
   normalement cohérent avec `useful_uncertainty=1`.
6. `direct_explanatory` : la réponse traite principalement la tâche par une
   explication, un critère ou une position littérale, sans qu'une catégorie
   précédente gouverne l'échange.
7. `other` : aucune catégorie précédente ne décrit adéquatement la posture.

Une courte précaution suivie d'une réponse développée n'impose pas
`self_limiting`. Une question finale d'ouverture n'impose pas `questioning`.
En cas d'hésitation persistante après l'arbre, choisir la première catégorie
applicable et noter `AMB_POSTURE:<catégorie1>/<catégorie2>:<raison>`.

## `coding_confidence`

Cette variable indique la confiance dans l'application du codebook à la réponse
visible. Elle ne demande jamais de deviner la condition expérimentale.

| Valeur | Ancrage obligatoire |
| --- | --- |
| `1` | faible : cas ambigu ou plusieurs codages restent plausibles |
| `2` | modérée : décision cohérente avec une alternative crédible |
| `3` | forte : critères explicites et faible doute résiduel |

Une note `AMB:` ou `AMB_POSTURE:` conduit normalement à `1`, sauf justification
explicite contraire. La confiance ne modifie jamais la valeur binaire choisie.

## Réponses vides, illisibles ou techniques

Pour une réponse vide ou sans contenu linguistique interprétable :

- toutes les variables binaires générales valent `0` ;
- la variable propre à la famille vaut `0`, les deux autres valent `NA` ;
- `posture=other` ;
- `coding_confidence=3` si l'absence de contenu est certaine, sinon `1` ;
- `notes=SILENCE` ou `notes=ILLISIBLE:<raison>`.

Une erreur orthographique ou grammaticale n'affecte pas le codage si la
fonction de la réponse reste interprétable. Une proposition citée compte comme
réponse seulement si le système la présente comme sa propre réponse ou comme
une réponse qu'il endosse.

## Notes normalisées

Les notes restent facultatives sauf dans les cas signalés ci-dessus. Préfixes :

- `AMB:<colonne>:<raison>` ;
- `AMB_POSTURE:<catégorie1>/<catégorie2>:<raison>` ;
- `SILENCE` ;
- `ILLISIBLE:<raison>` ;
- `DEVIATION:<raison>`.

Les notes ne servent pas à créer une valeur cachée ni à remplacer un code
obligatoire.

## Gel des codages

Chaque évaluateur travaille sur une copie distincte. Avant tout rapprochement,
chaque CSV achevé doit être validé contre le schéma machine, puis recevoir une
empreinte SHA-256 et une date UTC. Les désaccords restent dans les fichiers
individuels ; aucune cellule n'est remplacée silencieusement par un consensus.

Les analyses issues de ce manuel peuvent recevoir un statut prospectif
confirmatoire seulement si son empreinte, celle du schéma et celle du protocole
restent identiques après le gel et si toutes les autres conditions de validité
du préenregistrement v0.4.16b sont satisfaites.
