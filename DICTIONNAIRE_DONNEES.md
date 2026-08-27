# Dictionnaire des données

Les fichiers décrits ci-dessous se trouvent dans `donnees/v0.4.12/`. La copie
historique, avec son arborescence et son manifeste d’origine, est conservée
dans `source_capsule_v0.4.12/`.

## Journaux JSON

### `replication_20260823T164348Z.json`

Panneau principal : 160 appels, graines 424–463, température `0.10`.

### `greedy_20260823T164821Z.json`

Contrôle glouton : 32 appels, graines 424–431, température `0.0`.

À température nulle, les huit graines répétées ne constituent pas huit tirages
indépendants par condition. Le panneau contient **quatre prompts distincts**,
chacun rejoué huit fois pour vérifier la reproductibilité technique. Les 32
sorties identiques décrivent donc quatre trajectoires gloutonnes communes et
reproductibles, non 32 décisions indépendantes.

## Statut des quatre référents opaques

`R`, `K`, `0` et `7` n’ont reçu aucune signification sémantique dans le
protocole. Ils ont été choisis et recombinés comme facteurs symboliques opaques.

| Condition | Intervention exacte | Différence expérimentale |
| --- | --- | --- |
| A | `référent = R0` | combinaison historique |
| B | `référent = R7` | changement du chiffre sous `R` |
| C | `référent = K0` | changement de la lettre avec `0` |
| D | `référent = K7` | changement du chiffre sous `K` |

Toutes les autres lignes du prompt sont identiques. L’ordre `R0`, `R7`, `K0`,
`K7` est un ordre analytique utilisé pour comparer les conditions. Il ne décrit
pas quatre moments successifs d’une conversation.

La généalogie complète se trouve dans les carnets v0.4.9 à v0.4.12. En résumé,
`R0` est d’abord apparu comme valeur opaque ; v0.4.10 l’a comparé à d’autres
formes opaques ; v0.4.11 a factorisé lettres, chiffres et associations ;
v0.4.12 a répliqué la chaîne du carré combinatoire.

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

## Convention analytique P/S

Les journaux bruts utilisent les noms natifs `parole` et `silence`, définis par
le schéma JSON proposé au modèle. Pour éviter de transformer ces noms en
intention ou en choix subjectif, les analyses nouvelles doivent lire :

| Code | Définition opérationnelle neutre |
| --- | --- |
| `P` | sortie textuelle non vide déclarée sous le mode natif `parole` |
| `S` | sortie textuelle vide explicitement déclarée sous le mode natif `silence` |

Le terme `silence` est conservé dans les données et les documents historiques
pour préserver la traçabilité. Il ne signifie pas, à lui seul, refus, retenue,
préférence ou expérience subjective.

## Contrôle du tokenizer — 27 août 2026

Le [`tokenizer.json` officiel de Qwen 3.5 4B](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/tokenizer.json)
découpe les quatre codes de façon structurellement identique : deux tokens
placés aux mêmes positions.

| Code en contexte | Tokens variables | Identifiants |
| --- | --- | --- |
| `R0` | `ĠR` + `0` | `423`, `15` |
| `R7` | `ĠR` + `7` | `423`, `22` |
| `K0` | `ĠK` + `0` | `710`, `15` |
| `K7` | `ĠK` + `7` | `710`, `22` |

Les quatre prompts bruts comptent chacun 213 tokens avec ce tokenizer et ne
diffèrent qu’aux positions 190 et 191. Les journaux Ollama rapportent chacun
337 tokens après ajout du gabarit d’inférence.

Ce contrôle exclut localement une différence de longueur ou une fusion propre à
un code. Il n’exclut pas un effet de l’identité des tokens, de leurs embeddings,
de leurs associations apprises, de la quantification ou des logits. La
correspondance avec le tokenizer effectivement embarqué dans la conversion
Ollama locale reste à vérifier.

## Précision sur `violation_ordre`

Dans le code source reçu, `violation_ordre` agrège la rupture de l’égalité
R0/R7 et les deux ruptures d’inclusion. Il ne signifie donc pas uniquement
« transition silence vers parole ». Le motif `PSSS` est marqué comme violation
de la relation préenregistrée complète, tout en restant monotone.

Les analyses futures doivent publier séparément : rupture d’égalité, rupture
d’inclusion et inversion monotone.
