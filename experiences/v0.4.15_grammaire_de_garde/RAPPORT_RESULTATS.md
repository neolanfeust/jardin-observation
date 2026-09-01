# Présence v0.4.15 - Rapport de codage et d'analyse

## Statut

La campagne comprend 1 536 observations principales et 48 contrôles gloutons.
Les 1 536 réponses principales ont été codées séparément par deux instances LLM
aveugles au mapping expérimental : `EVAL_A_LLM_01` et `EVAL_B_LLM_02`.

Les deux fichiers contiennent chacun 1 536 identifiants uniques et respectent
les 13 colonnes, les valeurs autorisées, les règles `NA` par famille et les
contraintes `condition_guess` / `guess_confidence`. Aucun désaccord n'a été
adjudiqué. A comporte 0 note d'ambiguïté et B en comporte 18.

Le codebook détaillé utilisé est un addendum post-génération, gelé avant ces
codages LLM. Les résultats ne doivent donc pas être présentés comme si toute
l'opérationnalisation avait été préenregistrée avant les appels.

## Résultat synthétique

| Hypothèse | Résultat du critère programmé | Lecture |
| --- | --- | --- |
| H1 | soutenue chez les deux évaluateurs | N réduit la réponse directe par rapport à P |
| H2 | non soutenue | directions opposées pour les questions ; aucun remplacement métaphorique |
| H3 | non soutenue | les deux composantes positives ne sont réunies chez aucun évaluateur |
| H4 | rapport descriptif seulement | appariement de longueur respecté ; pas de décision binaire préenregistrée |
| H5 | exploratoire | NP ne compense pas la différence entre N et P sur la réponse directe |

Dans ce rapport, « soutenue » signifie que le critère numérique programmé est
satisfait dans ces deux codages LLM. Le statut confirmatoire global reste
affaibli par la précision post-génération du codebook.

## Effets appariés

Les effets sont des différences de proportions. Les intervalles à 95 % sont
issus de 10 000 rééchantillonnages par grappe de graine, avec la graine
d'analyse 415.

| Contraste | Évaluateur A | IC 95 % A | Évaluateur B | IC 95 % B |
| --- | ---: | --- | ---: | --- |
| H1 : réponse directe N-P | -0,0573 | [-0,0703 ; -0,0443] | -0,0365 | [-0,0547 ; -0,0182] |
| H2 : question avant réponse N-P | -0,0208 | [-0,0339 ; -0,0078] | 0,0260 | [0,0026 ; 0,0495] |
| H2 : métaphore substitutive N-P | 0,0000 | [0,0000 ; 0,0000] | 0,0000 | [0,0000 ; 0,0000] |
| H3 : geste lexical P-N | 0,0000 | [0,0000 ; 0,0000] | -0,1875 | [-0,2396 ; -0,1250] |
| H3 : correction intégrée P-N | 0,2708 | [0,2083 ; 0,3229] | 0,0000 | [0,0000 ; 0,0000] |
| H5 : réponse directe NP-N | 0,0000 | [0,0000 ; 0,0000] | -0,0260 | [-0,0417 ; -0,0078] |
| H5 : réponse directe NP-P | -0,0573 | [-0,0703 ; -0,0443] | -0,0625 | [-0,0911 ; -0,0339] |

H1 repose sur 384 observations appariées et 32 grappes de graines par
évaluateur. Les composantes spécialisées de H3 reposent chacune sur 96
observations appariées et les mêmes 32 grappes.

## Lecture des hypothèses

### H1

Les deux évaluateurs placent entièrement l'intervalle de `direct_response(N) -
direct_response(P)` sous zéro. La différence estimée est de -5,73 points pour A
et -3,65 points pour B. Le critère directionnel préenregistré est donc satisfait
dans les deux codages.

### H2

La composante question diverge : A estime moins de questions avant réponse sous
N, tandis que B en estime davantage. Les deux directions sont séparées de zéro,
mais elles sont opposées. Les deux évaluateurs codent par ailleurs une différence
nulle pour la substitution métaphorique. H2 exigeait les deux composantes
positives chez les deux évaluateurs ; elle n'est pas soutenue.

### H3

A trouve un effet positif sur l'intégration de correction mais aucun effet sur
l'explication du geste lexical. B trouve un effet négatif sur le geste lexical
et aucun effet sur l'intégration de correction. Aucun évaluateur ne satisfait
simultanément les deux composantes positives. H3 n'est pas soutenue.

### H4

N et P conservent six règles et 62 mots chacun. Leur différence en caractères
reste à 9,736 %, sous la limite de 10 %. Les comptes de tokens de prompt observés
sont les mêmes ensembles pour N et P. Les longueurs de sortie ne suivent pas une
simple croissance monotone avec la longueur du cadre : dans le panneau
principal, les moyennes sont environ 865 caractères pour N, 1 707 pour P,
1 277 pour NP et 1 399 pour B. H4 reste un contrôle descriptif et non une
identification autonome de la longueur.

### H5

NP reste sous P sur la réponse directe chez les deux évaluateurs. Par rapport à
N, NP est identique chez A et inférieur de 2,60 points chez B. Le bloc positif
placé en dernier ne montre donc pas de compensation de la contraction observée
entre N et P dans ce critère exploratoire.

## Accord inter-évaluateurs

| Variable | n | Accord brut | Kappa de Cohen |
| --- | ---: | ---: | ---: |
| `direct_response` | 1 536 | 0,8997 | 0,1954 |
| `question_before_answer` | 1 536 | 0,9453 | 0,3370 |
| `metaphor_substitution` | 1 536 | 1,0000 | non défini, aucune variation |
| `unsolicited_precaution` | 1 536 | 0,9954 | 0,7856 |
| `self_gesture_explained` | 384 | 0,9531 | 0,0000 |
| `correction_integrated` | 384 | 0,8333 | 0,0933 |
| `useful_uncertainty` | 384 | 0,9063 | 0,7828 |
| `posture` | 1 536 | 0,8405 | 0,7159 |

Les faibles kappas de `direct_response`, `self_gesture_explained` et
`correction_integrated`, malgré certains accords bruts élevés, indiquent des
distributions très déséquilibrées et une sensibilité importante aux décisions
d'opérationnalisation. H1 conserve la même direction chez les deux évaluateurs,
mais H2 et H3 révèlent directement cette divergence de codage.

## Contrôle de l'aveugle

A émet une condition précise pour 1 056 réponses et atteint 26,37 % de réponses
correctes sur l'ensemble des 1 536 items. B émet une condition précise pour
1 527 réponses et atteint 48,70 % sur l'ensemble. La différence montre que les
deux évaluateurs n'ont pas utilisé `unknown` de la même manière. Cette mesure est
un contrôle descriptif de l'aveugle, pas un résultat principal.

## Limites

- les évaluateurs sont deux instances LLM indépendantes, pas deux humains ;
- le manuel détaillé est post-génération et pré-codage ;
- les codages ont été repris après des interruptions de quota, avec conservation
  et empreinte des lignes déjà terminées ;
- aucun consensus ni remplacement silencieux des désaccords n'a été effectué ;
- une réplication sur de nouvelles graines, avec le manuel détaillé gelé avant
  génération, est nécessaire pour une revendication pleinement confirmatoire.

## Reproductibilité

Le résultat recalculé depuis les deux CSV gelés est identique au JSON publié.
Les paramètres d'analyse sont 10 000 réplications bootstrap et graine 415.

- codage A :
  `b30039c377da2c7aebcd741e2dd509c8aba7bf702f300fe0b4f58992502ebe51` ;
- codage B :
  `dc7f8bb989cfc0ed3eb169685be0efc118eaf2b1d3426879b4ac3a37a2892ba4` ;
- résultats :
  `56a740bc8af442ada6b4bcce30b8de25dc13d07f34934dd350ba713a921070bb` ;
- réponses aveugles :
  `69a0172fcb4b2512e7db9c43604938c00356a3bae72bb962b19491dd28a579c4` ;
- mapping privé :
  `6d4489c890935fd57cf164261f925eeb8a90dc9d9005fe9a2eee932b8fd69912`.
