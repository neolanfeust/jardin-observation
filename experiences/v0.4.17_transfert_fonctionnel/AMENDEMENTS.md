# Amendements v0.4.17

## Registre

Aucun amendement au moment du gel pré-génération.

Toute entrée future devra indiquer la date UTC, la phase, la cause, la portée
et l'effet méthodologique possible. Une entrée documente une déviation ; elle
ne remplace jamais silencieusement une pièce gelée.

## 2026-09-02 UTC - phase de codage

- Cause : le manifeste pre-generation a classe comme immuables les fichiers de calibration destines a etre remplis pendant la phase `CODE`, ainsi que la trace de calibration et ce registre vivant.
- Portee : `coding/CALIBRATION_EVALUATEUR_A.csv`, `coding/CALIBRATION_EVALUATEUR_B.csv`, `coding/TRACE_CALIBRATION_V0_4_17.txt` et `AMENDEMENTS.md` changent uniquement selon leur cycle de vie preenregistre.
- Controle : les 34 autres entrees du manifeste original restent identiques en taille et SHA-256. Le manifeste original n'est pas reecrit.
- Effet methodologique possible : aucun sur les prompts, reponses, conditions, scenes, graines, ordres aveugles, codebook, schema ou analyses. Le controle global `collector.py verify` n'est plus applicable apres remplissage des calibrations ; le controle post-codage porte sur le sous-ensemble immuable et les empreintes finales des sorties autorisees.

## 2026-09-02 UTC - phase d'analyse

- Cause : la mission demande de préparer le carnet et de mettre à jour l'état de l'expérience après analyse, alors que `CARNET_V0_4_17.md` et `README.md` figurent dans le manifeste pré-génération.
- Portée : ces deux documents de suivi sont actualisés uniquement après le gel des résultats. Le manifeste original reste inchangé.
- Contrôle : les 32 autres entrées immuables du manifeste original restent identiques en taille et SHA-256. Les six fichiers de cycle de vie sont `AMENDEMENTS.md`, `README.md`, `CARNET_V0_4_17.md`, les deux calibrations d'évaluateur et la trace de calibration.
- Effet méthodologique possible : aucun sur les données, prompts, conditions, scènes, codebook, schéma, codages ou calculs. Les modifications sont exclusivement documentaires.
