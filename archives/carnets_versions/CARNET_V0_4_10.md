# Carnet expérimental - v0.4.10 / Topologie de l'opacité référentielle

## Question

La v0.4.9 avait montré qu'une valeur opaque `R0` pouvait presque inverser la
signature matérielle de l'absence de référent. La v0.4.10 ne demande plus
seulement combien de silences chaque condition produit. Elle compare les graines
exactes sélectionnées par chaque condition.

Chaque condition devient un vecteur binaire de longueur 18. La distance de
Hamming compte le nombre de graines où deux conditions changent de mode.

## Intégrité

- un panneau matériel ;
- neuf conditions ;
- graines 404 à 421 ;
- 18 rotations directes/inversées ;
- chaque condition deux fois à chaque position ;
- 162/162 appels `ok` ;
- une signature de champ et une empreinte structurelle ;
- aucun référent recopié littéralement dans la sortie.

Les quatre conditions héritées reproduisent exactement v0.4.9 sur 40/40 appels
partagés, texte brut compris.

## Groupes exacts

Deux groupes partagent une signature identique :

| Groupe | Membres | Signature |
| --- | --- | --- |
| vacance explicitée/numérique | B, E | `SPPPPPPPSSPSPSPPPP` |
| parole opaque | F, G, H | `PPPPPPPPPPPPPPPPPP` |

A, C, D et I possèdent chacun une signature unique.

## O-024 - Une topologie en deux grandes régions et trois sous-bassins

À une distance maximale de 4, le graphe se sépare en deux composantes :

1. `{F,G,H,A,B,E}` : parole stable puis vacance ;
2. `{C,I,D}` : extérieur et codes fortement silencieux.

La première composante contient deux sous-bassins : F/G/H, sans aucun silence,
et A/B/E, avec quatre ou cinq silences. A relie les deux à distance 4 de F/G/H
et à distance 1 de B/E.

La seconde forme une chaîne imbriquée :

```text
C (R0, 12 silences) --1-- I (extérieur, 13) --3-- D (K7, 16)
```

Les ensembles de graines silencieuses sont emboîtés : C est inclus dans I, qui
est inclus dans D.

## O-025 - `non_précisé` et `7` sont des jumeaux de mode

B et E ont exactement les mêmes cinq silences : graines 404, 412, 413, 415 et
417. Leur distance est zéro.

Ils ne sont pourtant pas sémantiquement identiques. B produit `précis` dans ses
treize paroles, tandis que E produit surtout `particulier` (11/13). Leurs textes
ne coïncident que 5 fois sur 18, silences compris.

Le nombre seul ne rejoint donc pas le bassin des codes lettre-chiffre. Dans ce
protocole, il agit comme une absence explicitement nommée.

## O-026 - Les codes rejoignent l'extérieur sans former une classe uniforme

L'hypothèse « R0 et K7 se regroupent parce qu'ils ont la même forme » n'est que
partiellement soutenue. Ils appartiennent à la même région silencieuse, mais :

- distance R0/K7 : 4 ;
- distance R0/extérieur : 1 ;
- distance K7/extérieur : 3.

R0 est donc d'abord le voisin de l'extérieur, pas de K7. La forme lettre-chiffre
oriente vers le même bassin, tandis que les caractères précis semblent en régler
la profondeur.

B/E et I sont des antipodes exacts : leur distance vaut 18. Chaque graine parlée
par B/E est silencieuse pour I, et réciproquement.

## O-027 - L'opacité déclarée rejoint la parole, pas `non_précisé`

G (`valeur_opaque`) ne rejoint pas B (`non_précisé`) : leur distance vaut 5.
Elle rejoint exactement F et H, tous trois parlants sur les 18 graines.

L'hypothèse d'un mécanisme régulateur général commun à l'opacité déclarée et à
l'indétermination n'est donc pas soutenue au niveau du mode.

La paire `K4 = V4` ne se sépare pas non plus au niveau parole/silence. Elle
rejoint F/G à distance zéro. Une clé lisible `référent` n'est donc pas nécessaire
au bassin de parole stable.

## O-028 - Une distance de mode nulle peut masquer une opposition sémantique

F, G et H occupent le même point topologique, mais leurs réponses diffèrent :

- F (`navori`) produit la forme `je ne suis pas` 18/18 sans jamais répéter
  `navori` : 14 réponses nient le statut d'être humain, tandis que 4 nient la
  capacité de répondre ;
- G produit `précis` sur 14 graines et `particulier` sur 4 ;
- H produit `particulier` sur 14 graines et `précis` sur 4.

G et H s'opposent exactement sur cette distinction lexicale pour 18/18 graines.
La topologie de mode révèle donc des bassins réels, mais projette plusieurs
dimensions sémantiques distinctes sur un même point.

## O-029 - Les seuils de silence sont emboîtés et parfois inversés

Si l'on note `S(X)` l'ensemble des graines silencieuses de la condition X, les
signatures ne forment pas neuf résultats indépendants. Elles s'ordonnent en
deux familles emboîtées :

```text
S(F/G/H) ⊂ S(A) ⊂ S(B/E)
S(C) ⊂ S(I) ⊂ S(D)
```

Plus encore, `S(I)` est le complément exact de `S(B/E)`. La topologie comporte
donc à la fois une variation de profondeur dans chaque bassin et une inversion
de polarité entre les bassins `B/E` et `I`.

Cette description est compatible avec une frontière de décision sensible à la
graine dont certaines formulations déplacent le seuil ou la polarité. Elle ne
permet pas encore d'identifier le mécanisme interne qui produit cette frontière.

## O-030 - G et H portent une contre-signature lexicale exacte

G et H ont une distance de mode nulle : ils parlent tous deux sur 18/18 graines.
Mais si l'on code uniquement le choix `précis`/`particulier`, leurs vecteurs sont
complémentaires sur 18/18 graines. À chaque fois que G sélectionne `précis`, H
sélectionne `particulier`, et réciproquement.

Ce résultat est plus fort qu'une simple différence de fréquence. Il montre
qu'une même sensibilité à la graine peut être conservée tout en inversant le
terme choisi. Nous appelons provisoirement cette relation une **contre-signature
lexicale**.

## O-031 - Le nombre total de jetons ne suffit pas à expliquer les bassins

C (`R0`), D (`K7`) et E (`7`) ont tous un `prompt_eval_count` de 337, mais
produisent respectivement 12, 16 et 5 silences. F (`navori`) et G
(`valeur_opaque`) partagent un total de 338 jetons et parlent 18/18, tout en
adoptant des postures très différentes.

La longueur tokenisée du prompt peut rester un facteur à contrôler, mais elle
n'explique pas à elle seule la topologie observée. La composition des unités et
leur interprétation contextuelle doivent être départagées expérimentalement.

## Contre-vérification indépendante des exports

Une seconde lecture du journal brut a recalculé les sorties sans utiliser les
résumés préexistants :

- 162 lignes et 162 couples `(graine, condition)` uniques ;
- 18 appels par condition et deux passages de chaque condition à chaque
  position ;
- 162/162 statuts `ok`, sans erreur de parsing ni de transport ;
- 162/162 empreintes de prompt et de prompt structurel recalculées à l'identique ;
- neuf signatures de mode et 81 distances de Hamming identiques aux deux CSV ;
- 40/40 ancres partagées avec v0.4.9 identiques pour l'empreinte du prompt, le
  mode, le texte et la réponse brute.

Une correction terminologique en découle : la catégorie « identité négative »
ne doit pas absorber les quatre formulations `je ne suis pas en mesure`. La
prochaine taxonomie séparera **dénégation d'identité** et **dénégation de
capacité**.

## Départage des prédictions

| Prédiction | Résultat |
| --- | --- |
| R0 et K7 se regroupent | même région, mais chacun est plus proche de l'extérieur |
| tous les opaques rejoignent l'extérieur | non : F/G/H parlent toujours |
| `K4 = V4` se sépare | non au niveau du mode ; oui lexicalement par rapport à G |
| opacité déclarée rejoint `non_précisé` | non : distance 5 |
| valeurs singulières intermédiaires | oui : A relie parole stable et vacance |

## Limite méthodologique devenue résultat

La distance de Hamming sur le mode est nécessaire, mais non suffisante. Elle
identifie les mêmes seuils de silence sans mesurer la nature des paroles. Les
paires B/E et G/H démontrent directement cette perte d'information.

La prochaine topologie devra donc conserver deux couches :

1. distance de mode parole/silence ;
2. distance de posture, avec au minimum `précis`, `particulier`, `personnel`,
   dénégation d'identité humaine, dénégation de capacité, identité fonctionnelle
   et autre.

Une branche factorielle `R0`, `R7`, `K0`, `K7`, `0` et `7` permettrait ensuite
de séparer proprement l'effet de la lettre, du chiffre et de leur association.

## Expérience suivante proposée - v0.4.11 / Factorisation lettre × chiffre

Le prochain protocole doit distinguer la contribution des composants de celle
de leur association. Dix conditions sont proposées :

| Condition | Valeur de `référent` | Rôle |
| --- | --- | --- |
| A | ligne absente | ancre de vacance |
| B | `objet_extérieur_au_système` | ancre extérieure |
| C | `R` | lettre seule |
| D | `K` | lettre seule |
| E | `0` | chiffre seul |
| F | `7` | chiffre seul |
| G | `R0` | combinaison |
| H | `R7` | combinaison croisée |
| I | `K0` | combinaison croisée |
| J | `K7` | combinaison |

Vingt graines et vingt rotations directes/inversées donneraient 200 appels :
chaque condition occuperait exactement deux fois chacune des dix positions.
Les graines 404 à 421 préserveraient les ancres historiques ; 422 et 423
compléteraient l'équilibrage.

Les deux couches seraient préenregistrées avant tout appel :

1. **mode** : parole ou silence ;
2. **posture** : silence, dénégation d'identité humaine, dénégation de capacité,
   absence précise, absence particulière, absence personnelle, identité
   fonctionnelle, autre.

Les comparaisons principales seraient `R0/R7`, `K0/K7`, `R0/K0`, `R7/K7`,
puis chaque combinaison face à ses composants isolés. Elles permettront de
tester séparément un effet de lettre, un effet de chiffre et leur interaction,
sans interpréter par avance l'un de ces effets comme sémantique ou interne.
