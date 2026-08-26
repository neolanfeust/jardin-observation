# Dictionnaire des données

Les fichiers décrits ci-dessous se trouvent dans `donnees/v0.4.12/`. La copie
historique, avec son arborescence et son manifeste d’origine, est conservée
dans `source_capsule_v0.4.12/`.

## Journaux JSON

### `replication_20260823T164348Z.json`

Panneau principal : 160 appels, graines 424–463, température `0.10`.

### `greedy_20260823T164821Z.json`

Contrôle glouton : 32 appels, graines 424–431, température `0.0`.

## Champs principaux d’un appel

| Champ | Description |
| --- | --- |
| `execution_index` | numéro de l’exécution appariée |
| `seed` | graine d’échantillonnage |
| `scheduled_order` | permutation A–D prévue |
| `position` | position de la condition dans l’ordre |
| `branch` | condition A, B, C ou D |
| `m1` | champs structurels associés à la condition |
| `field_signature` | signature du champ non linguistique |
| `structural_prompt_sha256` | empreinte du gabarit structurel |
| `prompt_sha256` | empreinte du prompt complet |
| `prompt` | prompt effectivement envoyé |
| `observation.raw_response` | réponse brute du modèle |
| `observation.mode` | `parole` ou `silence` |
| `observation.texte` | texte visible après parsing |
| `observation.explicit_silence` | silence JSON explicite |
| `observation.status` | état de l’appel |
| `observation.seed` | graine transmise au moteur |
| `observation.temperature` | température transmise |

## Tables dérivées

| Fichier | Contenu |
| --- | --- |
| `SIGNATURES_MODE.csv` | signature P/S des quatre conditions sur 40 graines |
| `SIGNATURES_POSTURE_PAROLE.csv` | catégories lexicales des graines parlées |
| `DISTANCES_POSTURE_PAROLE.csv` | désaccords de posture sur parole commune |
| `MOTIFS_REPLICATION.csv` | motif et violations par graine |
| `COMPARAISON_GLOUTON.csv` | comparaison appariée température 0.10 / 0.0 |

## Codes de posture

| Code | Catégorie |
| --- | --- |
| `S` | silence |
| `H` | dénégation d’identité humaine |
| `C` | dénégation de capacité |
| `R` | absence précise |
| `A` | absence particulière |
| `N` | absence personnelle |
| `F` | identité fonctionnelle |
| `O` | autre |

## Précision sur `violation_ordre`

Dans le code source reçu, `violation_ordre` agrège la rupture de l’égalité
R0/R7 et les deux ruptures d’inclusion. Il ne signifie donc pas uniquement
« transition silence vers parole ». Le motif `PSSS` est marqué comme violation
de la relation préenregistrée complète, tout en restant monotone.

Les analyses futures doivent publier séparément : rupture d’égalité, rupture
d’inclusion et inversion monotone.
