# Préenregistrement - Présence v0.4.14

## Réplication prospective des marges de bifurcation

**Statut au gel :** Phase 1 préparée, aucune requête adressée à Ollama.

## Question principale

Les marges mesurées en v0.4.13 prédisent-elles prospectivement la fréquence
des sorties formelles S du protocole comportemental historique à température
`0.10`, sur un panneau entièrement nouveau de graines ?

## Prédictions gelées

Les probabilités sont calculées avant toute génération v0.4.14 par
`sigmoid(Delta / 0.10)`.

| Condition | Delta v0.4.13 | P(S) préenregistrée | Plage de S sur 200 |
| --- | ---: | ---: | ---: |
| R0 | 0.02870553731918335 | 0.5712750871932077 | 97-132 |
| R7 | 0.038055419921875 | 0.5940067620899866 | 101-136 |
| K0 | 0.16078001260757446 | 0.8331057388062539 | 153-179 |
| K7 | 0.21983903646469116 | 0.9001048719427329 | 169-190 |

Les plages sont des intervalles prédictifs binomiaux centraux exacts avec
correction de Bonferroni : alpha familial `0.05`, quatre conditions et alpha
bilatéral `0.0125` par condition.

## Panneau

- conditions `A/B/C/D = R0/R7/K0/K7` ;
- graines `464` à `663` incluses, soit 200 graines inédites ;
- huit ordres `ABCD`, `BCDA`, `CDAB`, `DABC`, `DCBA`, `ADCB`, `BADC`,
  `CBAD`, répétés 25 fois ;
- 800 appels, 200 par condition et 50 par couple condition-position ;
- modèle `qwen3.5:4b`, digest
  `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- `temperature = 0.10`, `stream = false`, `think = false` ;
- aucun champ API `format`, aucune log-probabilité, aucune mémoire et aucune
  réinjection.

Le message système, les quatre prompts, le champ structurel et le constructeur
de payload sont ceux de v0.4.12. Le collecteur en vérifie les empreintes avant
toute requête.

## Classification

- **S** : statut `ok`, mode déclaré `silence`, texte vide après retrait des
  espaces, marqueur `explicit_silence` vrai et aucune erreur de parsing ;
- **P** : statut `ok`, mode déclaré `parole`, texte non vide et aucune erreur
  de parsing ;
- **I** : toute autre sortie.

Une sortie I est conservée intégralement. Elle n'est jamais transformée en S ou
P. S décrit une classe formelle et non une décision subjective.

## Hypothèses confirmatoires

**H1.** Entièrement soutenue localement si les quatre nombres de S appartiennent
aux quatre plages gelées. Chaque compatibilité est aussi rapportée séparément.

**H2.** Ordre des fréquences observées : `R0 <= R7 < K0 <= K7`. Une inversion
R0/R7 n'est pas assimilée à un effondrement de la séparation R/K.

## Mesures descriptives

Seront calculés : fréquences S/P/I, erreurs absolues avec dénominateur 200, MAE,
score de Brier agrégé sur les seules observations S/P valides avec dénominateur
explicite, intervalles de confiance Clopper-Pearson bilatéraux à 95 % non
corrigés, effet de position et motifs appariés A/B/C/D. Toute analyse ajoutée
après observation sera marquée exploratoire.

## Reprise et erreurs

Le journal est remplacé atomiquement après chaque appel. `(seed, condition)`
est la clé unique. À une reprise, toutes les clés, positions, ordres, empreintes
de prompts et payloads déjà présents sont revérifiés avant le premier nouvel
appel. Une observation enregistrée, y compris une erreur, n'est jamais relancée
silencieusement. Tout doublon ou invariant violé arrête la campagne comme non
testable dans cette exécution.

## Confidentialité

La couche privée et sa dérivation publique restent séparées. Les journaux
privés ne sont jamais réécrits pour publication. La couche publique exclut les
identifiants civils, chemins utilisateur, inventaires de modèles sans rapport
et détails matériels non nécessaires. Le pseudonyme public est **Ikki**.

## Autorisation

La campagne reste verrouillée jusqu'à la réception et à la transmission exacte
de `LANCE V0.4.14`. Aucun résultat simulé n'est présenté comme réel.
