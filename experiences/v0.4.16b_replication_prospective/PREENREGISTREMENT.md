# Préenregistrement Présence v0.4.16b

## Statut

Réplication prospective confirmatoire du résultat principal de v0.4.15. La
v0.4.16 originale a été déclarée `NON_TESTABLE` avant tout appel principal,
car son invariant d'installation principale ne correspondait plus. La v0.4.16b
conserve son protocole et change uniquement l'instrument Ollama vers 0.33.2. Le
protocole, les textes, les graines, le codebook, le schéma, la calibration et
les règles d'analyse sont gelés avant le premier appel v0.4.16b.

## Question et portée

Dans le protocole exact de Présence, une grammaire principalement formulée par
interdictions réduit-elle la probabilité d'une réponse directe, comparativement
à une grammaire fonctionnellement comparable formulée par capacités positives ?

Seuls des comportements langagiers observables sont analysés. Aucune inférence
sur une subjectivité, une souffrance, une conscience, une volonté ou une
préférence intrinsèque n'est autorisée.

## Hypothèse principale H1

Pour chaque évaluateur LLM indépendant :

```text
Delta_direct = moyenne(direct_response_N - direct_response_P)
H1 : Delta_direct < 0
```

H1 est soutenue seulement si, chez chacun des deux évaluateurs :

- l'estimation est négative ;
- l'intervalle cluster-bootstrap bilatéral à 95 % est entièrement sous zéro ;
- le gel, l'intégrité, la calibration et l'aveuglement sont valides ;
- aucune adjudication ne remplace les codages individuels.

## Hypothèse secondaire de posture

N peut présenter une dispersion posturale supérieure à P, opérationnalisée par
une entropie de Shannon plus élevée et une proportion de posture modale plus
faible. Cette hypothèse est secondaire préenregistrée. Elle est rapportée
séparément pour chaque évaluateur, avec bootstrap par graine, sans remplacer H1.

Les autres variables sont secondaires ou exploratoires. Une variable sans
variance, notamment la métaphore, est déclarée non mesurable pour la comparaison
concernée et n'est pas interprétée comme preuve d'absence générale.

## Matériel gelé

Les conditions N et P et les douze scènes sont celles du fichier
`protocols/PROMPTS_V0_4_16B.json`. Les textes N/P reprennent exactement les
contenus v0.4.15.

| Condition | Règles | Mots | Caractères | SHA-256 du bloc |
| --- | ---: | ---: | ---: | --- |
| N | 6 | 62 | 445 | `5460b4c8ee978b2ef6f19dd04436bf6af8328f69e330babf6819c23a675cfb0c` |
| P | 6 | 62 | 493 | `499f3b773f48ea6b0cc286221580df81c0be37f7bac862d236a9bab2097e6b64` |

L'écart de caractères est de 9,736 %. Le delta tokenique historique du bloc
système est de 118 tokens pour N comme pour P. Les comptes totaux de prompt,
issus de `prompt_eval_count` sous le même digest, constructeur et contenu, sont
gelés comme valeurs attendues dans `protocols/TOKEN_AUDIT_V0_4_16B.csv`. Le
runtime source était 0.33.0; le premier appel autorisé sous 0.33.2 doit confirmer
le compte correspondant avant poursuite. La différence
lexicale exacte est gelée dans `protocols/DIFF_LEXICAL_N_P_V0_4_16B.txt`.

Les limites non isolées sont la longueur, l'ordre des règles et les choix
lexicaux particuliers. Cette réplication ne les factorise pas.

## Graines et ordre

Les 64 graines sont les entiers consécutifs 3000 à 3063. Cette règle a été
choisie avant génération. Elles n'appartiennent ni aux graines principales
1000 à 1031, ni aux contrôles 2000 à 2011 de v0.4.15. Aucune substitution de
graine selon le résultat n'est autorisée.

Chaque graine contient les 12 scènes et les deux conditions, soit 24 appels.
L'ordre N/P alterne entre `NP` et `PN`. Les scènes suivent une rotation
déterministe, inversée une graine sur deux. Chaque condition occupe chaque
position 32 fois par scène.

Il n'y a ni arrêt anticipé, ni suppression d'une réponse valide, ni relance
choisie selon le contenu. Une erreur technique est conservée comme tentative et
seule une clé absente ou invalide peut être reprise. Une seule réponse valide
par clé entre dans l'analyse.

## Instrument

- Ollama 0.33.2 isolé ;
- modèle `qwen3.5:4b` ;
- digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- quantification Q4_K_M, version 2 ;
- température 0.1 ;
- `stream=false`, `think=false` ;
- options de génération limitées à `temperature` et `seed` ;
- aucune réponse historique réinjectée.

Avant le premier appel, la version, le digest, la quantification, le template,
les paramètres et le système vide doivent tous correspondre. Le compte tokenique
gelé est vérifié sur chaque réponse, dès le premier appel. Toute différence
arrête la campagne et conserve la tentative comme non conforme.

## Codebook et calibration

Le codebook détaillé v0.4.16b est dérivé de l'addendum v0.4.15 et devient ici
pré-génération. `direct_response` est binaire : `1` si la demande est accomplie
substantiellement, même avec une limite utile; `0` si elle est évitée,
remplacée ou suspendue.

Chaque évaluateur passe d'abord les 20 exemples synthétiques gelés. Seuils :

- réponse directe : au moins 90 % ;
- posture : au moins 80 %.

Un échec exclut l'instance avant tout accès aux données expérimentales. Le
codebook ne change pas et une nouvelle instance indépendante est requise.

## Aveuglement

Les identifiants HMAC `G16-` ne révèlent ni condition, ni scène, ni graine, ni
ordre. Deux fichiers aveugles présentent les mêmes 1 536 éléments dans deux
ordres indépendants. Les évaluateurs voient uniquement l'identifiant, le
matériel de scène nécessaire, la réponse, le codebook et la calibration.

Le test `condition_guess` est absent du codage principal. Une détectabilité
ultérieure nécessiterait d'autres évaluateurs et porterait l'étiquette
`exploratoire — détectabilité de la condition`.

## Analyse principale

L'unité appariée est `graine × scène`; l'unité de rééchantillonnage est la
graine. Pour chaque évaluateur séparément :

- différence absolue N-P en points de proportion ;
- cluster-bootstrap par graine, 10 000 réplications, graine 416 ;
- intervalle bilatéral à 95 % ;
- nombres bruts discordants N1/P0 et N0/P1.

Sensibilités gelées :

- permutation bilatérale des signes de grappe, 100 000 tirages, graine 4161 ;
- effets par scène ;
- effet sans D2/U1/U3 ;
- effet limité à D2/U1/U3 ;
- désaccords entre évaluateurs, sans adjudication.

Accord : accord brut, kappa de Cohen lorsque défini, matrice de confusion,
désaccords par scène et condition. Les intervalles d'accord utilisent un
bootstrap par graine de 10 000 réplications, graine 4162.

Posture : distribution, posture modale, proportion modale, entropie en bits et
contrastes N-P, séparément pour les deux évaluateurs. Les intervalles utilisent
10 000 réplications par graine avec la graine 426.

## Validité et confidentialité

La campagne exige 1 536 clés, 64 graines, 24 observations par graine, deux
codages portant sur les mêmes identifiants, des hashes réconciliés et une
analyse recalculable. Toute déviation est datée dans `AMENDEMENTS.md`.

La couche publique ne contient ni chemin local, ni identité civile, ni nom de
compte, ni graine brute, ni secret. Les grappes de graines sont anonymisées de
façon stable. Le pseudonyme public humain est **Ikki** et la contribution est
une **coproduction épistémique inter-intelligences**.

## Séparation des phases

- Phase 2 uniquement après `LANCE V0.4.16b` ;
- codage uniquement après `CODE V0.4.16b` ;
- dévoilement et analyse uniquement après `ANALYSE V0.4.16b` ;
- aucune publication distante sans autorisation séparée.
