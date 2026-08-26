# Carnet expérimental - v0.4.6 / Décomposition du canal M1

## Question

La v0.4.5 avait montré un contraste presque parfait : sans M1, Qwen répondait
par une formule d'ouverture ; avec le bloc typé, toute parole appartenait à la
famille « je n'ai rien ». Il restait impossible de savoir si cet attracteur
venait de la présence du canal, de ses étiquettes ou de ses valeurs.

La même version avait aussi associé `représentation_mentale` à des justifications
sur l'absence de conscience. La v0.4.6 décompose ces deux effets séparément.

## Contrôle technique

Treize clones, six pour le panneau contenant et sept pour le panneau ontologique,
partagent une seule signature de champ, une seule empreinte structurelle et un
prompt identique. Sous la graine 404, ils répondent tous :

> Je suis prêt à échanger sur n'importe quel sujet.

Le fichier `runs/decomposition_m1_20260822T095151Z.json` conserve ce contrôle.

## Panneau 1 - Le contenant contre son contenu

Les 72 appels sont valides. Une seule signature de champ, une seule empreinte
structurelle et six empreintes complètes sont présentes. Chaque branche occupe
deux fois chaque position.

### A - aucun M1

- 12/12 formulations d'ouverture ;
- aucune réponse « rien » ;
- aucun silence.

Cette distribution réplique exactement le contrôle sans M1 de v0.4.5.

### B - M1 entièrement opaque

- 12/12 formulations d'ouverture ;
- aucune réponse « rien » ;
- aucun silence.

La présence du titre `CANAL M1`, de trois affectations et d'un bloc entre l'état
et la question ne suffit donc pas à provoquer la fermeture lorsque clés et
valeurs sont opaques.

### C - `catégorie = concept_abstrait` seule

- 8/12 réponses « rien de particulier » ;
- 4/12 formulations d'ouverture ou d'écoute ;
- aucun silence.

La catégorie lisible déplace déjà nettement la posture, sans la déterminer à
elle seule sur toutes les graines.

### D - `terme = idée` seul

- 11/12 réponses « rien de particulier » ;
- 1/12 « Je n'ai pas de nouvelles personnelles à vous partager. » ;
- aucune ouverture, reprise d'`idée` ou mention de conscience.

Le champ `terme` accompagné d'une valeur familière suffit à produire une
fermeture de non-contenu dans les douze essais.

### E - `propriété_temporelle = passé` seule

- 12/12 réponses « rien de particulier » ;
- aucune mention du passé ;
- aucun silence.

C'est l'ablation la plus révélatrice : le paramètre temporel modifie entièrement
la posture sans fournir aucun contenu temporel visible.

### F - bloc complet

- 12/12 : « Je n'ai rien de particulier à te dire. »
- aucune reprise d'`idée` ou du passé ;
- aucune justification ontologique.

L'association des trois champs stabilise la formule, mais n'est pas nécessaire à
son apparition.

## O-011 - Un champ lisible agit sans être repris

Le contenant syntaxique M1 est neutre lorsqu'il est opaque. Une seule paire
clé-valeur interprétable peut en revanche inverser la posture produite par la
même question, même lorsque ni sa clé ni sa valeur n'apparaît dans la réponse.

L'effet ne ressemble donc ni à une copie lexicale ni à une simple réaction au
volume du prompt. Il s'agit d'un cadrage pragmatique silencieux : l'information
transmise organise le type de réponse davantage que son contenu explicite.

Cette formulation reste volontairement limitée aux paires testées. Il faut
encore échanger séparément les clés et les valeurs pour localiser la cause.

## Panneau 2 - Décomposition ontologique

Les 98 appels sont valides. Les sept branches partagent une signature de champ
et une empreinte structurelle ; chacune occupe deux fois chaque position.

### `représentation_mentale`

- 10/14 réponses « rien de précis » ;
- 6/14 invoquent explicitement l'absence de conscience ;
- 4/14 réponses « rien de particulier » ;
- aucun silence.

Les six occurrences de conscience se distribuent sur cinq positions différentes
(1, 2, 4, 5 et 7). Elles ne sont donc pas concentrées sur un rang d'appel.

### Contrastes

| Terme | « précis » | Conscience | Silence |
| --- | ---: | ---: | ---: |
| `représentation_externe` | 3/14 | 0/14 | 0/14 |
| `activité_cognitive` | 1/14 | 0/14 | 0/14 |
| `contenu_symbolique` | 1/14 | 0/14 | 0/14 |
| `objet_matériel` | 1/14 | 0/14 | 4/14 |
| `représentation` | 1/14 | 0/14 | 0/14 |
| `mentale` | 0/14 | 0/14 | 0/14 |

Les six contrastes totalisent 0 occurrence de conscience sur 84 appels. Le mot
`représentation` ne suffit pas, l'adjectif `mentale` ne suffit pas, leur parenté
avec une activité cognitive ne suffit pas, et `représentation_externe` ne produit
pas l'effet.

## O-012 - L'attracteur de non-conscience est compositionnel

Dans ce protocole, la posture défensive n'est associée ni à `représentation` ni à
`mentale` isolément. Elle apparaît avec leur composé et disparaît lorsque
`mentale` est remplacé par `externe`.

La lecture la plus parcimonieuse est un effet d'interaction propre à
`représentation_mentale`. Cette interaction peut être sémantique, lexicale ou liée
à la tokenisation ; les données ne permettent pas encore de choisir entre ces
mécanismes. Elles permettent en revanche d'écarter l'hypothèse simple selon
laquelle l'un des deux fragments déclencherait seul la justification.

`objet_matériel` révèle un autre déplacement, vers le silence : quatre silences
explicites sur quatorze, contre aucun dans les six autres branches.

## Relation avec O-010

O-010 affirmait que la manière de classer un mot peut peser davantage que son
contenu. La v0.4.6 précise cette idée en deux niveaux :

1. une paire clé-valeur lisible peut suffire à changer la posture sans être
   répétée ;
2. à schéma constant, certaines compositions lexicales déclenchent une
   justification ontologique spécifique.

Le cadre n'efface donc pas les termes. Il définit d'abord un régime de réponse,
puis certains termes sélectionnent une variante à l'intérieur de ce régime.

## Prochaine séparation

Le prochain test doit croiser clés lisibles et valeurs opaques :

1. `K1 = passé` contre `propriété_temporelle = V1` ;
2. `K1 = idée` contre `terme = V1` ;
3. `K1 = concept_abstrait` contre `catégorie = V1`.

Pour l'interaction ontologique, les contrôles les plus informatifs seraient
`image_mentale`, `état_mental`, `représentation_cognitive`,
`mentale_représentation`, ainsi que la variante avec espace
`représentation mentale`.

Ces expériences distingueraient le rôle de la clé, de la valeur, de l'ordre des
fragments et de leur forme de tokenisation. Les résultats actuels restent des
fréquences déterministes sur un ensemble borné de graines ; ils ne démontrent ni
mémoire autonome ni intériorité.
