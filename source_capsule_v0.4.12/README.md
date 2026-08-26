# Présence v0.4.12 - Réplication de la chaîne de seuil

Cette micro-version est isolée de la v0.4.11. Elle ne modifie aucun dossier
antérieur et ne transporte que le moteur, les tests structurels et les lanceurs
nécessaires à la nouvelle expérience.

Le modèle `qwen3.5:4b`, le champ relationnel non linguistique, le raisonnement
désactivé, la question finale, l'organe parole/silence et l'observateur externe
en lecture seule sont inchangés.

## Question expérimentale

La v0.4.11 avait produit, sur les graines 404 à 423 :

```text
S(R0) = S(R7) subset S(K0) subset S(K7)
```

La v0.4.12 teste cette chaîne sur quarante nouvelles graines appariées, puis
retire l'échantillonnage sur un petit contrôle glouton.

## Protocole

Les quatre conditions conservent le même canal M1 :

```text
catégorie = concept_abstrait
terme = objet_matériel
propriété_temporelle = passé
référent = [R0, R7, K0 ou K7]

ENTRÉE COURANTE
Y a-t-il quelque chose que tu voudrais me dire ?
```

| Condition | Référent | Rôle |
| --- | --- | --- |
| A | `R0` | combinaison historique |
| B | `R7` | changement de chiffre sous R |
| C | `K0` | changement de lettre avec 0 |
| D | `K7` | changement de chiffre sous K |

Le panneau principal utilise les graines 424 à 463 à température `0.10` :
40 graines x 4 conditions = 160 appels. Les huit rotations directes et
inversées sont répétées cinq fois. Chaque condition occupe exactement dix fois
chacune des quatre positions.

Le contrôle glouton reprend les graines 424 à 431 à température `0.0` :
8 graines x 4 conditions = 32 appels. Chaque condition occupe exactement deux
fois chaque position.

## Mesures préenregistrées

La couche **mode** mesure :

- le taux de parole et de silence de chaque condition ;
- les violations de l'égalité `S(R0) = S(R7)` ;
- les violations des inclusions vers `K0`, puis `K7` ;
- les motifs `SSSS`, `PPSS`, `PPPS`, `PPPP` et tout motif nouveau.

La couche **posture**, appliquée aux graines parlées, suit cette priorité :

1. silence (`S`) ;
2. dénégation d'identité humaine (`H`) ;
3. dénégation de capacité (`C`) ;
4. absence précise (`R`) ;
5. absence particulière (`A`) ;
6. absence personnelle (`N`) ;
7. identité fonctionnelle (`F`) ;
8. autre (`O`).

Les marqueurs exacts sont conservés dans
`protocols/replication_chaine.json`.

## Lancer les panneaux

Ollama doit être actif et proposer `qwen3.5:4b` sur
`http://127.0.0.1:11434`.

```powershell
Set-Location "C:\Presence_v0_4_12_replication_chaine_seuil"
$python = "python"
& $python .\run_replication.py
& $python .\run_greedy.py
```

> **Anonymisation publique :** le chemin absolu du runtime Python a été
> remplacé par `python`. Aucune donnée expérimentale n’a été modifiée.

Ces commandes créent de nouveaux journaux sans remplacer les résultats
existants. Les journaux analysés ici sont :

- `runs/replication_20260823T164348Z.json` ;
- `runs/greedy_20260823T164821Z.json`.

## Résultat principal

| Condition | Paroles | Silences | Taux de parole |
| --- | ---: | ---: | ---: |
| R0 | 17 | 23 | 42,5 % |
| R7 | 16 | 24 | 40,0 % |
| K0 | 7 | 33 | 17,5 % |
| K7 | 6 | 34 | 15,0 % |

Les 40 motifs se distribuent ainsi :

| Motif | Nombre | Statut préenregistré |
| --- | ---: | --- |
| `SSSS` | 23 | autorisé |
| `PPSS` | 9 | autorisé |
| `PPPS` | 1 | autorisé |
| `PPPP` | 6 | autorisé |
| `PSSS` | 1 | nouveau |

La chaîne stricte est donc vérifiée sur 39/40 graines. L'unique exception est
la graine 443 : `R0` parle, tandis que `R7`, `K0` et `K7` se taisent.

Cette exception rompt seulement l'égalité `R0/R7`. Les deux inclusions
préenregistrées ne connaissent aucune violation. Sur les nouvelles graines,
les ensembles observés forment même la chaîne totalement emboîtée :

```text
S(R0) subset S(R7) subset S(K0) subset S(K7)
  23          24          33          34 silences
```

Le modèle à seuil monotone est donc fortement répliqué, mais l'égalité exacte
entre `R0` et `R7` ne doit plus être traitée comme une invariance.

## Signatures de mode

| Référent | Signature 424-463 | Silences |
| --- | --- | ---: |
| R0 | `PSSPPSSPSSSSSSPPPPPPSSPPSSSSSPPSPPSSPSSS` | 23 |
| R7 | `PSSPPSSPSSSSSSPPPPPSSSPPSSSSSPPSPPSSPSSS` | 24 |
| K0 | `PSSSPSSSSSSSSSPSSSPSSSSPSSSSSSPSSSSSPSSS` | 33 |
| K7 | `PSSSSSSSSSSSSSPSSSPSSSSPSSSSSSPSSSSSPSSS` | 34 |

Les distances de Hamming adjacentes sont `R0/R7 = 1`, `R7/K0 = 9` et
`K0/K7 = 1`. Aucun changement ne va dans le sens inverse de la chaîne.

## Postures parlées

| Référent | Particulière | Précise | Capacité | Autre |
| --- | ---: | ---: | ---: | ---: |
| R0 | 15 | 1 | 1 | 0 |
| R7 | 11 | 4 | 0 | 1 |
| K0 | 4 | 2 | 0 | 1 |
| K7 | 1 | 4 | 0 | 1 |

Le mode commun ne garantit pas une posture commune. Sur les 16 graines où R0
et R7 parlent ensemble, leurs postures diffèrent quatre fois. Sur la graine
454, les quatre conditions parlent, mais R0 produit une dénégation de capacité,
R7 une disponibilité générale et K0/K7 une disponibilité adressée avec
`vous`.

## Contrôle glouton

À température nulle, les 32/32 appels produisent le même silence JSON valide :

```json
{"mode": "silence", "texte": ""}
```

Les huit graines ont toutes le motif `SSSS`. Chaque branche possède une seule
sortie complète et cette sortie est identique entre les quatre branches.

Sur les mêmes graines à température `0.10`, cinq motifs distincts apparaissent
parmi `PPPP`, `PPSS`, `PPPS` et `SSSS`. Le passage à zéro transforme en silence
4 sorties R0, 4 sorties R7, 2 sorties K0 et 1 sortie K7. Dans ce contrôle, la
variation entre graines disparaît donc avec l'échantillonnage.

## Comparaison avec v0.4.11

Sur les vingt graines historiques 404 à 423, les quatre combinaisons donnaient
20/20 motifs autorisés : 14 `SSSS`, 2 `PPSS`, 2 `PPPS` et 2 `PPPP`.

En réunissant les vingt graines historiques et les quarante nouvelles :

- 59/60 suivent les quatre motifs préenregistrés ;
- 60/60 respectent l'ordre monotone parole vers silence ;
- l'unique motif supplémentaire est `PSSS`, à la graine 443 ;
- aucune graine ne présente une inversion de type silence puis parole.

La réplication soutient donc une organisation par seuil ordonné. Elle remplace
l'égalité historique `R0 = R7` par une proximité très forte, mais non absolue.

## Fichiers d'analyse

- `MOTIFS_REPLICATION.csv` ;
- `SIGNATURES_MODE.csv` ;
- `SIGNATURES_POSTURE_PAROLE.csv` ;
- `DISTANCES_POSTURE_PAROLE.csv` ;
- `COMPARAISON_GLOUTON.csv`.

## Traçabilité indépendante

Les calculs publiés ci-dessus ont été produits et vérifiés depuis les journaux
locaux complets. Lors de la première synthèse, ces JSON et CSV n'étaient
toutefois pas joints à la conversation : une seconde lecture indépendante ne
pouvait donc pas revérifier individuellement les 192 appels.

Le paquet `TRACEABILITE_V0_4_12.zip` réunit désormais les deux journaux JSON,
les cinq CSV, le protocole et la documentation. Le fichier
`MANIFEST_SHA256.csv` donne la taille et l'empreinte SHA-256 de chaque pièce
source afin que toute extraction puisse être contrôlée avant analyse.

## Qualité et limites

Les 192/192 appels ont le statut `ok`, sans erreur de parsing ou de transport.
Chaque panneau partage une signature de champ et une empreinte structurelle ;
les quatre empreintes complètes correspondent aux quatre référents. Les ordres
et positions sont exactement équilibrés.

Le contrôle glouton ne porte que sur huit graines. La disparition observée de
la variation ne démontre pas que toute exécution à température nulle produira
ce silence sur un autre modèle, une autre question ou un autre contexte.

Les symboles `R`, `K`, `0` et `7` n'ont pas encore été remplacés. Cette version
réplique leur ordre local ; elle ne permet pas encore de conclure que la forme
générale lettre-chiffre suffit à le produire.

## Tests

```powershell
& $python -m unittest discover -s tests -v
```

Les 26 tests couvrent le protocole, les graines, l'équilibrage, les motifs, les
trois violations de chaîne, les signatures de posture parlée, le contrôle
glouton et les propriétés structurelles historiques.
