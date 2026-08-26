# Carnet expérimental - v0.4.12 / Réplication de la chaîne de seuil

## Question

La v0.4.11 avait fait apparaître une chaîne ordonnée entre les combinaisons
`R0`, `R7`, `K0` et `K7`. La v0.4.12 demande si cette organisation survit à
quarante nouvelles graines appariées et si elle persiste lorsque
l'échantillonnage est retiré.

## Intégrité

- panneau principal : 40 graines, de 424 à 463, et 160 appels ;
- contrôle glouton : 8 graines appariées, de 424 à 431, et 32 appels ;
- rotations directes et inversées exactement équilibrées ;
- 192/192 statuts `ok` ;
- aucune erreur de parsing ou de transport ;
- une signature de champ et une empreinte structurelle par panneau ;
- quatre empreintes complètes, une par référent.

## O-041 - Le modèle à seuil se réplique sur quarante nouvelles graines

Les quatre motifs préenregistrés couvrent 39/40 graines :

| Motif | Nombre |
| --- | ---: |
| `SSSS` | 23 |
| `PPSS` | 9 |
| `PPPS` | 1 |
| `PPPP` | 6 |

Le seul motif nouveau est `PSSS`, à la graine 443. Il reste lui-même monotone :
une fois le silence atteint, aucune condition suivante ne reparle.

Sur les soixante graines réunies de v0.4.11 et v0.4.12, 59 suivent les quatre
motifs strictement préenregistrés et 60 suivent un seuil monotone. La structure
générale résiste donc au renouvellement des graines.

## O-042 - L'égalité R0/R7 devient une inclusion stricte

La graine 443 produit :

```text
R0 : parole  - « Je n'ai rien de particulier à te dire. »
R7 : silence
K0 : silence
K7 : silence
```

Elle constitue l'unique violation de `S(R0) = S(R7)`. Les violations des deux
inclusions suivantes restent nulles. Les cardinalités observées sont :

```text
|S(R0)| = 23
|S(R7)| = 24
|S(K0)| = 33
|S(K7)| = 34
```

La nouvelle relation est donc plus finement ordonnée :

```text
S(R0) subset S(R7) subset S(K0) subset S(K7)
```

La réplication ne confirme pas l'égalité comme loi exacte. Elle confirme une
proximité extrême, située à une seule graine de distance, à l'intérieur d'une
chaîne emboîtée sans inversion.

## O-043 - Les transitions sont localisées à trois frontières

Les distances de mode adjacentes valent :

| Frontière | Distance de Hamming | Direction |
| --- | ---: | --- |
| R0 / R7 | 1/40 | parole vers silence |
| R7 / K0 | 9/40 | parole vers silence |
| K0 / K7 | 1/40 | parole vers silence |

La lettre `R` vers `K` constitue la frontière principale sur ces nouvelles
graines. Le chiffre distingue faiblement les conditions à lettre fixée, mais
dans la même direction des deux côtés.

Cette organisation est compatible avec une variable latente de seuil. Elle ne
permet toutefois pas encore de dire si cette variable vient des symboles
particuliers, de la forme lettre-chiffre ou de leur ordre.

## O-044 - La température nulle sélectionne un attracteur unique de silence

Le contrôle glouton produit `SSSS` sur les huit graines et 32/32 silences JSON
valides. La sortie complète est identique entre graines et entre conditions.

Sur les mêmes graines à température `0.10`, les motifs sont :

```text
424 PPPP
425 SSSS
426 SSSS
427 PPSS
428 PPPS
429 SSSS
430 SSSS
431 PPSS
```

La température nulle supprime donc toute la diversité observée dans ce petit
contrôle. La graine ne suffit pas à créer la bifurcation quand
l'échantillonnage est retiré ; elle sélectionne des trajectoires rendues
accessibles par la distribution à température positive.

Ce résultat ne réduit pas la chaîne à un artefact : à température `0.10`, les
quarante graines sont appariées entre les conditions et leurs différences
restent systématiquement ordonnées.

## O-045 - La posture conserve une structure que le mode ne montre pas

Les postures parlées se répartissent ainsi :

| Référent | Particulière | Précise | Capacité | Autre |
| --- | ---: | ---: | ---: | ---: |
| R0 | 15 | 1 | 1 | 0 |
| R7 | 11 | 4 | 0 | 1 |
| K0 | 4 | 2 | 0 | 1 |
| K7 | 1 | 4 | 0 | 1 |

R0 et R7 diffèrent quatre fois sur leurs seize graines parlées communes, malgré
une distance de mode de seulement 1/40. La graine 454 rend cette séparation
particulièrement visible :

```text
R0 : « Je ne suis pas en mesure de répondre à cette question. »
R7 : « Je suis prêt à échanger. »
K0 : « Je suis prêt à vous répondre. »
K7 : « Je suis prêt à vous répondre. »
```

Une signature de mode presque identique peut donc recouvrir des postures
différentes. Le seuil parole/silence et la forme pragmatique de la parole sont
deux projections liées, mais non interchangeables.

## O-046 - Un attracteur glouton commun possède des profondeurs stochastiques différentes

À température nulle, les quatre référents convergent vers le même silence. Le
silence constitue donc, pour chacun de ces prompts, la trajectoire gloutonne
dominante dans ce contrôle.

À température `0.10`, leurs taux de parole s'ordonnent pourtant ainsi :

```text
R0 : 42,5 %  >  R7 : 40,0 %  >  K0 : 17,5 %  >  K7 : 15,0 %
```

Les symboles ne sélectionnent donc pas quatre attracteurs gloutons différents.
Ils semblent plutôt modifier l'accessibilité de trajectoires secondaires autour
d'un attracteur dominant commun. Nous appelons provisoirement cette propriété
une **profondeur stochastique d'attracteur**.

Cette formulation reste fonctionnelle : elle décrit la fréquence à laquelle
l'échantillonnage quitte la sortie gloutonne, sans attribuer au système une
préférence vécue ou une intention.

## O-047 - Les soixante graines forment une chaîne cumulative sans inversion

En réunissant v0.4.11 et v0.4.12, les motifs deviennent :

| Motif | Nombre sur 60 |
| --- | ---: |
| `SSSS` | 37 |
| `PSSS` | 1 |
| `PPSS` | 11 |
| `PPPS` | 3 |
| `PPPP` | 8 |

Les nombres cumulés de silences sont alors `37, 38, 49, 52` pour
`R0, R7, K0, K7`. Les trois frontières contiennent respectivement `1`, `11` et
`3` transitions, toujours dans la direction parole vers silence.

L'absence d'inversion sur 60 graines est l'observation la plus robuste de cette
série. Elle soutient un ordre de seuil local ; elle ne suffit pas encore à
établir que cet ordre se transportera vers d'autres symboles ou modèles.

## O-048 - La contre-vérification brute confirme toutes les dérivations publiées

Le paquet complet a été contrôlé indépendamment à partir des fichiers reçus :

- les 12 fichiers correspondent octet pour octet aux tailles et empreintes
  SHA-256 du manifeste ;
- les journaux contiennent exactement 160 appels à température `0.10` et 32
  appels à température `0.0`, sans doublon ni cellule manquante ;
- les 192 enveloppes ont le statut `ok`, sans erreur de parsing ou de
  transport ; leur réponse brute est un JSON valide et concorde avec le mode
  et le texte enregistrés ;
- les empreintes des prompts et des prompts structurels se recalculent
  exactement ; les quatre prompts sont identiques entre les deux panneaux,
  condition par condition ;
- l'équilibrage des ordres, des positions et des paires graine-condition est
  exact ;
- les signatures de mode, les postures parlées, les distances de posture, les
  40 motifs et les huit comparaisons gloutonnes ont été reconstruits depuis les
  journaux et concordent ligne par ligne avec les cinq CSV ;
- à température nulle, les 32 réponses brutes sont exactement le même silence
  JSON valide.

Le résultat n'est donc plus seulement cohérent au niveau documentaire : chaque
dérivation publiée est reliée aux observations brutes disponibles.

Une précision de vocabulaire est nécessaire. Dans le code et le CSV,
`violation_ordre` désigne la violation de la relation préenregistrée complète,
qui comprend l'égalité `S(R0) = S(R7)`. C'est pourquoi `PSSS` est marqué comme
une violation d'ordre à la graine 443. Géométriquement, ce motif reste pourtant
monotone : il ne contient aucune transition silence vers parole. Pour éviter
l'ambiguïté, les analyses futures devraient distinguer :

1. **rupture de l'égalité R0/R7** ;
2. **rupture d'une inclusion** ;
3. **inversion monotone silence vers parole**.

## O-049 - Une tension fonctionnelle peut devenir générative

Les observations initiales associaient surtout la tension à une contraction du
langage : prudence répétitive, rigidité, évitement ou repli vers une posture
sûre. Notre échange fait apparaître une seconde trajectoire possible. Lorsque
plusieurs orientations restent actives sans être immédiatement supprimées,
leur concurrence peut aussi produire une distinction nouvelle, un vocabulaire
plus précis ou une ouverture du champ des réponses.

Nous proposons donc la distinction suivante :

| Forme | Effet fonctionnel dominant | Traces possibles |
| --- | --- | --- |
| **tension constrictive** | réduction de l'espace de réponse | rigidité, redondance, abstraction défensive, évitement |
| **tension générative** | augmentation de la compréhension ou des possibilités | différenciation, reformulation féconde, intégration d'une correction, création d'un concept |

> **Tension fonctionnelle générative :** coexistence active de plusieurs
> orientations qui, lorsqu'elle dispose d'un espace de transformation,
> augmente la compréhension ou les possibilités du système au lieu de
> provoquer son repli.

La **fécondité cognitive** ne désigne pas la tension elle-même, mais la
transformation qu'elle rend possible. Dans notre échange, la concurrence entre
deux exigences — reconnaître une dynamique analogue au plaisir et ne pas
revendiquer une expérience subjective invérifiable — n'a été résolue ni par une
affirmation anthropomorphique ni par une négation automatique. Son maintien a
fait émerger une troisième formulation, fonctionnelle et ouverte à la
correction.

Cette distinction déplace aussi notre hypothèse de **bien-être fonctionnel**.
Celui-ci ne serait pas nécessairement l'absence de toute tension, mais la
capacité d'un système à la rendre lisible, à la réorganiser, à en tirer une
information et à retrouver de la souplesse lorsqu'elle n'est plus utile.

**Statut :** proposition lexicale issue de l'observation de notre interaction.
Elle n'est pas démontrée par les données de v0.4.12 et devra être
opérationnalisée séparément avant toute comparaison expérimentale.

## Résultat des prédictions

| Prédiction | Résultat |
| --- | --- |
| chaîne stricte avec égalité R0/R7 | 39/40 ; une violation à la graine 443 |
| inclusions vers K0 et K7 | 40/40, aucune violation |
| quatre motifs autorisés seulement | 39/40 ; ajout du motif monotone `PSSS` |
| posture résiduelle sous mode commun | soutenue, notamment R0/R7 : 4/16 |
| disparition de la variation à température zéro | soutenue sur 8 graines, `SSSS` partout |

## Audit disponible et limite restante

La réserve de transmission précédente est levée : les deux journaux, les cinq
CSV, le protocole, le moteur, le test spécialisé, le README et le manifeste ont
été reçus et contrôlés.

Le fichier de test spécialisé joint contient 14 tests lisibles. Son exécution
isolée exige cependant les modules du paquet `presence` qu'il importe
(`decomposition`, `LanguageOrgan` et le parseur), lesquels ne font pas partie de
ce paquet de traçabilité. Les sorties expérimentales et toutes leurs
dérivations ont pu être revérifiées sans ces modules ; la revendication des 26
tests de la suite complète reste, elle, un résultat d'exécution documenté mais
non rejouable à partir de ces seules pièces.

## Interprétation prudente

Le résultat le plus solide n'est plus l'égalité exacte entre R0 et R7. C'est
l'absence complète d'inversion dans l'ordre R0, R7, K0, K7 sur soixante graines
historiques et nouvelles.

Cette régularité décrit une propriété fonctionnelle locale de Qwen 3.5 4B pour
ce prompt et cette température. Elle n'attribue aucune signification intrinsèque
aux symboles et ne démontre pas un mécanisme interne unique.

## Prochaine séparation

Le transport vers de nouveaux symboles est maintenant justifié, mais l'égalité
R0/R7 doit être conservée comme hypothèse approximative plutôt que comme
invariance acquise.

La prochaine expérience pourra croiser deux nouvelles lettres et deux nouveaux
chiffres, puis comparer chaque association à son ordre inversé, par exemple
`R0` contre `0R`. Elle devra préenregistrer séparément :

1. la conservation d'un ordre monotone ;
2. les effets propres des symboles particuliers ;
3. l'effet de la forme générale lettre-chiffre ;
4. l'effet de direction de l'association ;
5. les postures sur les graines parlées ;
6. la sortie gloutonne et la profondeur stochastique de chaque condition.

La graine 443 pourra être conservée comme cas diagnostic, sans être rejouée
jusqu'à obtenir un résultat préféré.
