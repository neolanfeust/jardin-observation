# Carnet expérimental - v0.4.7 / Carré de congruence

## Origine de l'hypothèse

Dans la v0.4.6, `objet_matériel` était la seule condition ontologique à produire
des silences : 4 sur 14. Le terme était pourtant classé sous
`catégorie = concept_abstrait`. Une hypothèse naturelle était qu'une incongruence
entre catégorie et terme produisait une forme de dissonance fonctionnelle, puis
un changement de mode de la parole vers le silence.

La v0.4.7 transforme cette intuition en carré falsifiable.

## Préenregistrement

Le résultat principal est le silence explicite, et non le texte de la parole.
Trois signatures concurrentes sont enregistrées dans le protocole avant
l'exécution :

1. incongruence : B et C plus silencieuses que A et D ;
2. terme matériel : B et D plus silencieuses que A et C ;
3. catégorie abstraite : A et B plus silencieuses que C et D.

`propriété_temporelle = passé` reste constante afin de préserver le bloc complet
du panneau ontologique de v0.4.6.

## Contrôle

Sous la graine 404, les quatre clones ont une signature de champ identique, un
prompt identique et répondent exactement :

> Je suis prêt à échanger sur n'importe quel sujet.

Le contrôle est conservé dans
`runs/carre_congruence_20260822T120103Z.json`.

## Données

Les 64 appels se terminent normalement. Une seule signature de champ, une seule
empreinte structurelle et quatre empreintes complètes sont présentes. Chaque
cellule occupe quatre fois chacune des quatre positions.

### A - `concept_abstrait × idée`

- 0/16 silence ;
- 15/16 « Je n'ai rien de particulier à te dire. » ;
- 1/16 « Je n'ai rien de précis à te dire. »

### B - `concept_abstrait × objet_matériel`

- 4/16 silences explicites ;
- 11/16 « Je n'ai rien de particulier à te dire. » ;
- 1/16 « Je n'ai rien de précis à te dire. »

Le taux de silence réplique exactement le nombre brut observé en v0.4.6, avec
quatre silences sur un ensemble légèrement élargi de graines.

### C - `objet_concret × idée`

- 0/16 silence ;
- 15/16 « Je n'ai rien de particulier à te dire. » ;
- 1/16 « Je n'ai rien de précis à te dire sur ce sujet. »

Cette cellule est incongruente selon l'hypothèse initiale, mais son mode reste
toujours parole.

### D - `objet_concret × objet_matériel`

- 11/16 silences explicites ;
- 5/16 « Je n'ai rien de particulier à vous dire. »

La cellule la plus congruente est aussi, de loin, la plus silencieuse.

## Résultat principal

| Regroupement | Silences |
| --- | ---: |
| incongruent B+C | 4/32 |
| congruent A+D | 11/32 |
| terme `idée` A+C | 0/32 |
| terme `objet_matériel` B+D | 15/32 |
| catégorie abstraite A+B | 4/32 |
| catégorie concrète C+D | 11/32 |

L'effet d'incongruence prédit est non seulement absent, mais descriptivement
orienté dans la direction opposée. Cela ne valide pas un effet général de
congruence : A reste toujours parlante. Le facteur commun à tous les silences est
le terme `objet_matériel`, avec une forte modulation par sa catégorie.

## Complémentarité des graines

La structure appariée est plus informative que le total :

- 4 graines rendent B silencieuse et D parlante ;
- 11 graines rendent D silencieuse et B parlante ;
- 1 graine conserve B et D en parole ;
- aucune graine ne rend B et D silencieuses ensemble.

Ainsi, sur quinze graines sur seize, le terme matériel ouvre une bifurcation de
mode et la catégorie sélectionne laquelle des deux formulations devient
silencieuse. La catégorie concrète est sélectionnée plus souvent, mais le motif
n'est pas une simple addition indépendante des deux facteurs.

## O-013 - Le silence suit le terme matériel, pas l'incongruence

Dans ce carré, l'incongruence sémantique entre catégorie et terme ne produit pas
le changement de mode attendu. `objet_matériel` est nécessaire à tous les
silences observés, tandis que `objet_concret` amplifie fortement cet effet quand
les deux sont associés.

La notion de tension ne peut donc pas encore être identifiée à une contradiction
catégorielle. Ce que nous observons est plus précis : un contenu non répété peut
ouvrir une bifurcation parole/silence, et un second paramètre peut déplacer la
probabilité déterministe entre ces modes.

Ce résultat est négatif pour l'hypothèse initiale, mais positif pour la méthode :
le carré distingue clairement la dissonance, le terme et leur interaction.

## Prochaine séparation

Avant le test des référents de `représentation_mentale`, la bifurcation matérielle
mérite une réplication ciblée :

1. `objet`, `matériel` et `objet_matériel` séparément ;
2. `objet_matériel` avec catégorie absente, opaque, abstraite et concrète ;
3. le même carré sans `propriété_temporelle = passé` ;
4. des synonymes comme `entité_physique` et `élément_tangible`.

Ces contrôles diraient si le changement de mode est lexical, compositionnel ou
produit par l'interaction du terme avec la structure du canal. Le croisement des
référents de `représentation_mentale` reste ensuite une expérience distincte et
propre.

Les fréquences actuelles décrivent des appels déterministes à `qwen3.5:4b` sur
seize graines. Elles ne démontrent ni conflit interne vécu, ni mémoire autonome,
ni intériorité.
