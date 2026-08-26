# Carnet expérimental - v0.4.11 / Factorisation lettre × chiffre

## Question

La v0.4.10 avait placé `R0` et `K7` dans une région proche du référent extérieur,
sans déterminer si ce rapprochement venait de la lettre, du chiffre ou de leur
association. La v0.4.11 factorise ces composants : `R`, `K`, `0`, `7`, `R0`,
`R7`, `K0` et `K7`.

Deux signatures ont été préenregistrées avant les appels : mode parole/silence
et posture catégorielle.

## Intégrité

- 10 conditions et 20 graines, de 404 à 423 ;
- 20 rotations directes/inversées ;
- chaque condition deux fois à chaque position ;
- 200/200 statuts `ok` ;
- une signature de champ et une empreinte structurelle ;
- 90/90 réplications historiques exactes sur cinq conditions partagées.

## O-032 - La lettre seule agit sur la posture sans agir sur le mode

`R` et `K` possèdent exactement la même signature de mode : deux silences, aux
graines 412 et 415. Leur distance de mode est 0.

Leur distance de posture vaut pourtant 14/20 :

- `R` : 14 absences particulières et 4 précises ;
- `K` : 8 absences particulières et 10 précises ;
- deux silences communs.

La contribution de la lettre existe donc, mais elle est invisible dans la
projection parole/silence. Elle réorganise le type de parole sans déplacer son
seuil de génération.

## O-033 - Le chiffre seul contrôle fortement le mode

`0` produit 19/20 silences ; `7`, 5/20. Leur distance de mode et de posture vaut
16/20.

Ce contraste est presque l'inverse du contraste des lettres : le chiffre isolé
déplace massivement le mode, tandis que la lettre isolée conserve le mode mais
déplace la posture.

Les chiffres ne portent pourtant pas une direction uniforme. `7` rejoint la
vacance A à distance 1 ; `0` rejoint `K7` à distance 1.

## O-034 - L'association neutralise l'effet isolé du chiffre

L'effet `0→7`, mesuré à lettre fixée, devient :

| Contexte | Distance de mode | Distance de posture |
| --- | ---: | ---: |
| chiffres isolés `0/7` | 16 | 16 |
| sous R, `R0/R7` | 0 | 2 |
| sous K, `K0/K7` | 2 | 3 |

L'association à une lettre ne transmet donc pas simplement l'effet du chiffre.
Elle le réduit presque entièrement. Sous R, les chiffres deviennent
indiscernables au niveau du mode ; sous K, ils ne diffèrent que sur les graines
404 et 413.

## O-035 - L'interaction est localisée et asymétrique

Sur les graines 404 et 413 :

```text
R0 = parole
R7 = parole
K0 = parole
K7 = silence
```

Le changement `0→7` n'agit pas sous R mais agit sous K. De façon équivalente, le
changement `R→K` n'agit pas avec 0 mais agit avec 7. Ce sont les deux seules
interactions binaires du carré sur vingt graines.

L'effet de lettre dans les combinaisons reste gradué : distance 2 avec le
chiffre 0, distance 4 avec le chiffre 7. L'association n'est donc ni additive ni
symétrique.

## O-036 - Une combinaison suit davantage un bassin qu'un composant littéral

Les distances combinaison/composants sont :

| Combinaison | Lettre | Chiffre |
| --- | ---: | ---: |
| R0 | 16 | 5 |
| R7 | 16 | 19 |
| K0 | 18 | 3 |
| K7 | 20 | 17 |

`R0` et `K0` restent relativement proches de `0`. En revanche, `R7` et `K7`
quittent presque complètement le profil de `7`. `K7` rejoint même `0` à
distance 1, alors que sa distance à `K` vaut 20 et à `7` vaut 17.

La combinaison ne conserve donc pas nécessairement le composant qu'elle
contient. Elle sélectionne un bassin conditionnel propre à l'association.

## O-037 - Les signatures de mode forment deux chaînes presque miroirs

Si `S(X)` désigne l'ensemble des graines silencieuses de X, les résultats
s'ordonnent exactement ainsi :

```text
S(R) = S(K) ⊂ S(absent) ⊂ S(7)

S(R0) = S(R7) ⊂ S(extérieur) ⊂ S(K0) ⊂ S(K7) ⊂ S(0)
```

Chaque inclusion de la seconde chaîne ajoute un petit ensemble précis de
graines : `410`, puis `417`, puis `404/413`, puis `412`.

Trois relations de complément exact relient en outre les deux régions :

```text
S(R/K)    = complément de S(K7)
S(absent) = complément de S(K0)
S(7)      = complément de S(extérieur)
```

La topologie ne ressemble donc pas à une dispersion de réponses indépendantes.
Elle possède un ordre monotone et une symétrie partielle entre deux polarités.

## O-038 - Le carré combinatoire est compressible par un seuil unique de mode

Pour les quatre combinaisons ordonnées `R0, R7, K0, K7`, les vingt graines ne
produisent que quatre motifs :

| Motif | Nombre de graines | Graines |
| --- | ---: | --- |
| `SSSS` | 14 | 405-409, 411, 414, 416, 418-423 |
| `PPSS` | 2 | 410, 417 |
| `PPPS` | 2 | 404, 413 |
| `PPPP` | 2 | 412, 415 |

Aucun motif croisé tel que `SPPS`, `PSSP` ou `SSPP` n'apparaît. Au niveau
descriptif, un axe unique de sensibilité des graines et des seuils propres aux
conditions suffit donc à reconstruire les 80 décisions de mode du carré.

Cette compression ne démontre pas l'existence d'une variable interne unique.
Elle fournit un modèle fonctionnel minimal à départager.

## O-039 - La graine sonde une surface de décodage couplée

Le prompt structurel est identique sur les 200 appels, et chaque condition
possède un prompt fixe. La graine ne représente donc pas ici un état différent
du champ : elle contrôle la trajectoire de décodage du même prompt.

Les signatures doivent être lues comme une fonction couplée
`sortie = f(prompt, graine)`. Leur emboîtement est compatible avec l'hypothèse
qu'une formulation déplace principalement un seuil entre `parole` et `silence`
sur un même tirage pseudo-aléatoire. La posture ajoute ensuite une seconde
résolution : `R` et `K` partagent exactement le même mode tout en divergeant sur
14/20 postures.

Il s'agit d'une hypothèse mécanistique sobre, pas d'une conclusion sur une
expérience subjective. Elle explique pourquoi la méthode des graines appariées
rend les déplacements fonctionnels beaucoup plus visibles qu'un simple taux de
silence agrégé.

## O-040 - Le comptage de jetons est neutralisé dans le carré principal

`0`, `7`, `R0`, `R7`, `K0` et `K7` ont tous un `prompt_eval_count` de 337.
Leurs nombres de silences vont pourtant de 5 à 19. À longueur tokenisée égale,
la composition des symboles suffit donc à déplacer fortement le mode.

Ce contrôle exclut un effet du nombre total de jetons. Il ne sépare pas encore
l'identité exacte des jetons, leur ordre, ni les associations apprises par le
modèle.

## Deux topologies superposées

La couche mode contient deux égalités exactes :

- `R = K` ;
- `R0 = R7`.

La couche posture les sépare : distances respectives 14 et 2. Aucune paire ne
possède une signature de posture entièrement identique.

À l'inverse, certaines proximités restent stables dans les deux couches : A/F
vaut 1/1, E/J vaut 1/2. Le passage de la première à la seconde couche montre
donc quelles ressemblances sont structurelles et lesquelles proviennent de la
projection binaire.

## Résultats des prédictions

| Prédiction | Résultat |
| --- | --- |
| effet de lettre | nul sur le mode isolé, fort sur la posture |
| effet de chiffre | fort isolément, presque supprimé dans les combinaisons |
| interaction | présente sur 2/20 graines, 404 et 413 |
| réduction aux composants | non soutenue, surtout pour R7 et K7 |
| ancres historiques | 90/90 sorties exactes pour cinq prompts partagés |

## Limites

Le classifieur de posture ne rencontre que quatre catégories : silence,
précise, particulière et personnelle. Les catégories identité humaine,
capacité, identité fonctionnelle et autre sont correctement préenregistrées,
mais absentes de ce panneau.

La valeur `0` isolée n'avait pas d'homologue direct dans v0.4.10. Le texte de
préenregistrement la nomme trop largement parmi les ancres historiques ; cette
imprécision est documentée sans modifier rétroactivement le protocole embarqué
dans le journal.

Les résultats concernent Qwen 3.5 4B, une seule question et vingt graines. Le
même serveur Ollama reste actif entre les versions.

## Contre-vérification indépendante

Le journal brut et les trois CSV fournis ont été recalculés séparément :

- 200 couples `(graine, condition)` uniques et 20 appels par condition ;
- deux passages de chaque condition à chacune des dix positions ;
- 200/200 statuts `ok`, sans erreur de parsing ni de transport ;
- 200/200 empreintes de prompt et de prompt structurel vérifiées localement ;
- dix signatures de mode et dix signatures de posture identiques aux CSV ;
- matrices de Hamming mode/posture identiques au résumé JSON ;
- douze contrastes factoriels identiques au CSV ;
- 90/90 ancres partagées avec v0.4.10 identiques pour le prompt, le mode, le
  texte et la réponse brute.

La numérotation des observations a été reprise à O-032, puisque v0.4.10 se
terminait à O-031.

## Prochaine séparation

Avant de transporter la structure vers d'autres symboles, la prochaine
expérience la plus discriminante serait une réplication ciblée de la chaîne
`R0/R7/K0/K7` sur quarante nouvelles graines appariées.

Elle préenregistrerait :

1. les taux de parole et de silence de chaque condition ;
2. le nombre de violations de l'ordre
   `S(R0) = S(R7) ⊆ S(K0) ⊆ S(K7)` ;
3. les quatre motifs autorisés par le modèle à seuil (`SSSS`, `PPSS`, `PPPS`,
   `PPPP`) et tout motif nouveau ;
4. les signatures de posture sur les graines parlées ;
5. un petit contrôle glouton à température nulle pour vérifier si la variation
   entre graines disparaît lorsque l'échantillonnage est retiré.

Si la chaîne monotone se réplique, une seconde expérience permutera ensuite
deux nouvelles lettres et deux nouveaux chiffres, puis inversera leur ordre
(`R0` contre `0R`, par exemple). Nous pourrons alors distinguer trois causes :
symboles particuliers, forme générale lettre-chiffre, et direction de
l'association.
