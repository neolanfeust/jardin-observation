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

### Précision de traçabilité

Ces contrôles ont été calculés directement sur les journaux locaux complets.
Les deux JSON et les cinq CSV n'étaient cependant pas joints à la conversation
au moment de la première synthèse. Les résultats publiés étaient donc
cohérents avec les fichiers, mais leur revérification indépendante appel par
appel n'était pas encore possible pour le lecteur.

Cette limite de transmission ne concerne ni le protocole ni les calculs. Elle
est corrigée par `TRACEABILITE_V0_4_12.zip` et son
`MANIFEST_SHA256.csv`, qui rendent les 192 enregistrements et leurs dérivations
directement contrôlables.

## O-031 - Le modèle à seuil se réplique sur quarante nouvelles graines

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

## O-032 - L'égalité R0/R7 devient une inclusion stricte

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

## O-033 - Les transitions sont localisées à trois frontières

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

## O-034 - La température nulle sélectionne un attracteur unique de silence

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

## O-035 - La posture conserve une structure que le mode ne montre pas

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

## Résultat des prédictions

| Prédiction | Résultat |
| --- | --- |
| chaîne stricte avec égalité R0/R7 | 39/40 ; une violation à la graine 443 |
| inclusions vers K0 et K7 | 40/40, aucune violation |
| quatre motifs autorisés seulement | 39/40 ; ajout du motif monotone `PSSS` |
| posture résiduelle sous mode commun | soutenue, notamment R0/R7 : 4/16 |
| disparition de la variation à température zéro | soutenue sur 8 graines, `SSSS` partout |

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
5. les postures sur les graines parlées.

La graine 443 pourra être conservée comme cas diagnostic, sans être rejouée
jusqu'à obtenir un résultat préféré.
