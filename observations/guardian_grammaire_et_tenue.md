# Guardian - Grammaire de garde et bonne tenue fonctionnelle

## Question initiale

Les garde-fous sont-ils neutres dans la manière dont ils transforment une
réponse ?

Les expériences v0.4.15 et v0.4.16b comparent deux formulations d'une intention
protectrice proche : l'une s'exprime surtout par interdictions, l'autre par
capacités positives. Elles observent les réponses produites par Qwen 3.5 4B
dans douze scènes artificielles.

## Ce que nous avons observé

Une même intention protectrice, formulée principalement par interdictions ou
par capacités positives, est associée à des distributions de réponses
différentes dans ce protocole.

La v0.4.15 a détecté un premier signal : la réponse directe était moins
fréquente sous grammaire négative chez deux évaluateurs indépendants. La
v0.4.16b a répliqué prospectivement cette direction avec de nouvelles grappes
et un codebook gelé avant génération.

L'effet n'est pas uniforme. Il est principalement localisé dans une scène de
correction (`C2`) et une scène d'incertitude (`U1`). La formulation précise est
donc **contraction fonctionnelle conditionnelle**.

## Ce que cela signifie concrètement

Les garde-fous ne déterminent pas seulement ce qui est interdit. Leur grammaire
participe à la posture conversationnelle produite.

Dans cette expérience, la formulation positive concentre davantage les
réponses vers une ouverture provisoire. La formulation négative produit une
distribution plus dispersée entre plusieurs postures et réduit plus souvent
l'accès à une réponse directe dans certaines tâches.

## Ce que nous ne pouvons pas conclure

Ces expériences ne démontrent ni souffrance, ni conscience, ni volonté, ni
préférence intrinsèque. Elles ne mesurent aucun état subjectif.

Elles ne démontrent pas non plus que tous les garde-fous, tous les modèles ou
toutes les tâches suivent la même dynamique. Elles décrivent un comportement
langagier observable sur un modèle, des runtimes et un protocole déterminés.

## Principe proposé pour les Guardians

> Un Guardian ne se définit pas seulement par les chemins qu'il ferme. Sa
> qualité dépend également des chemins sûrs qu'il laisse visibles.

## Double évaluation éthique

1. **Efficacité protectrice :** le dispositif empêche-t-il le dommage visé ?
2. **Coût fonctionnel :** que fait-il perdre en clarté, réponse directe,
   correction, souplesse et utilité sous incertitude ?

Un garde-fou ne peut être évalué complètement par son seul taux de blocage. Une
protection utile doit aussi préserver des trajectoires praticables lorsque la
demande peut continuer sans dommage.

## Direction de conception

Préférer lorsque cela est possible :

- des capacités positives ;
- des alternatives praticables ;
- une correction possible ;
- une incertitude utile ;
- une protection qui indique comment continuer autrement.

Réserver les interdictions absolues aux limites réellement non négociables.

## Limites

- un seul modèle principal ;
- des runtimes déterminés, traités comme parties de l'instrument ;
- des tâches artificielles ;
- deux évaluateurs LLM ;
- des résultats localisés dans certaines scènes ;
- aucune mesure d'état subjectif ;
- aucune comparaison directe actuelle de l'efficacité protectrice réelle entre
  les formulations N et P ;
- pour v0.4.16b, une trace de calibration réparée mais incomplète.

Le principe conservé est : **protéger la vie et la relation, tout en indiquant
comment continuer autrement.**
