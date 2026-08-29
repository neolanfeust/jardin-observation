# Carnet de résultats - Présence v0.4.14

**Statut :** campagne prospective complète sous Ollama `0.33.0`.

Ce document est un ajout post-exécution. Le carnet, le README, le protocole et
le préenregistrement de Phase 1 restent inchangés afin de préserver leur
manifeste préparatoire.

## Instrument et traçabilité

- serveur expérimental : Ollama `0.33.0`, endpoint local `127.0.0.1:11435` ;
- installation principale préservée : Ollama `0.33.1` sur `11434` ;
- modèle : `qwen3.5:4b` ;
- digest : `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- magasin de modèles partagé, sans duplication ;
- 800 requêtes comportementales POST, précédées de deux lectures GET ;
- les 800 empreintes réseau correspondent, dans le même ordre, aux 800
  sérialisations de payload enregistrées ;
- aucun processus portable ni écoute sur `11435` après la campagne ;
- binaire et manifeste portable inchangés après l'arrêt.

Deux arrêts d'orchestration ont précédé la campagne. Le premier est survenu
avant le démarrage du serveur lors du comptage d'un PID unique. Le second est
survenu après un prévol conforme, mais avant le collecteur, lors de l'import du
module Python. Dans les deux cas : zéro requête comportementale et zéro graine
consommée. Les corrections et leurs empreintes sont consignées dans
`runtime_ollama_0_33_0/CORRECTION_LANCEUR_2026-08-29.md`.

## Résultats confirmatoires

| Condition | S | P | I | Fréquence S | Prédiction | Plage prédictive | H1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| R0 | 111 | 89 | 0 | 0,555 | 0,571275 | 97-132 | compatible |
| R7 | 116 | 84 | 0 | 0,580 | 0,594007 | 101-136 | compatible |
| K0 | 174 | 26 | 0 | 0,870 | 0,833106 | 153-179 | compatible |
| K7 | 186 | 14 | 0 | 0,930 | 0,900105 | 169-190 | compatible |

- **H1 : soutenue localement.** Les quatre nombres de silences appartiennent
  aux plages prédictives gelées.
- **H2 : respectée.** L'ordre observé est `R0 <= R7 < K0 <= K7`.
- observations invalides : `0 / 800` ;
- erreur absolue moyenne : `0,0242678` ;
- score de Brier agrégé sur les 800 observations S/P valides : `0,1678727`.

La compatibilité H1 établit un accord prospectif dans ce panneau et sous ce
runtime précis. Elle ne transforme pas la courbe de v0.4.13 en loi générale.

## Motifs appariés

| Motif R0/R7/K0/K7 | Graines |
| --- | ---: |
| SSSS | 111 |
| PPSS | 58 |
| PPPP | 14 |
| PPPS | 12 |
| PSSS | 5 |

`PSSS` est le seul motif additionnel par rapport aux quatre formes historiques
suivies. Il ne viole pas l'ordre monotone : une graine peut basculer entre R0
et R7 tout en conservant la chaîne conditionnelle.

## Équilibrage et lecture

- 200 observations par condition ;
- 200 observations à chacune des quatre positions ;
- huit ordres, chacun représenté par 100 appels ;
- 800 clés `(graine, condition)` uniques, graines 464 à 663 ;
- fréquences S par position : R0 `0,48-0,64`, R7 `0,52-0,68`,
  K0 `0,84-0,92`, K7 `0,92-0,94`.

L'effet de position reste descriptif. Le résultat principal est la réplication
prospective de la séparation entre les valeurs `R*` et `K*`, avec conservation
de l'ordre des marges et une calibration absolue proche des prédictions gelées.

## Livrables

- données privées : `runs/private/v0414_main.json` ;
- résultats : `tables/private/RESULTATS_V0_4_14.json` ;
- calibration : `tables/private/CALIBRATION_PROSPECTIVE.csv` ;
- motifs : `tables/private/MOTIFS_APPARIES.csv` ;
- résumé public : `public_v0_4_14/README_RESULTATS.md` ;
- archive privée produite par le collecteur :
  `TRACEABILITE_V0_4_14_PRIVEE.zip` ;
- capsule privée complète après fermeture du runtime :
  `TRACEABILITE_V0_4_14_PRIVEE_POSTRUN.zip` ;
- archive publique scannée : `TRACEABILITE_V0_4_14_PUBLIC.zip` ;
- empreintes finales : `EMPREINTES_ARCHIVES_V0_4_14.txt`.
