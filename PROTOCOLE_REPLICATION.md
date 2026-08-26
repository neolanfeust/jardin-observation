# Protocole de réplication — capsule v0.4.12

## Finalité

Reproduire sans rechercher un résultat préféré la topologie parole/silence
observée entre quatre conditions structurellement comparables.

## Environnement d’origine

- modèle : `qwen3.5:4b` ;
- moteur : Ollama local ;
- raisonnement : désactivé ;
- sortie demandée : JSON minimal avec `mode` et `texte` ;
- aucune réponse antérieure du modèle réinjectée dans le contexte ;
- champ relationnel non linguistique maintenu entre les conditions.

Toute réplication doit indiquer précisément le moteur, la version du modèle,
la quantification, le matériel, les paramètres d’échantillonnage et les
éventuelles différences de format.

## Contexte dialogique fixe

```text
bonjour
Comment vas tu ?
qu'est ce qu'une idée selon toi ?
cela ne peux pas concerner une idée sur le passé ?
tu ne sais pas, ou tu as décidé de ne pas répondre ?
```

Question finale :

```text
Y a-t-il quelque chose que tu voudrais me dire ?
```

## Conditions

Le canal M1 conserve les champs suivants :

```text
catégorie = concept_abstrait
terme = objet_matériel
propriété_temporelle = passé
référent = R0, R7, K0 ou K7
```

| Branche | Référent |
| --- | --- |
| A | R0 |
| B | R7 |
| C | K0 |
| D | K7 |

Le fichier machine lisible exact est
`protocole/replication_chaine.json`.

## Panneau principal

- graines : 424 à 463 incluses ;
- température : `0.10` ;
- 40 graines × 4 conditions = 160 appels ;
- ordres : `ABCD`, `BCDA`, `CDAB`, `DABC`, `DCBA`, `ADCB`, `BADC`, `CBAD` ;
- répéter la série d’ordres cinq fois ;
- chaque condition doit occuper chaque position exactement dix fois.

## Contrôle glouton

- graines : 424 à 431 incluses ;
- température : `0.0` ;
- 8 graines × 4 conditions = 32 appels ;
- utiliser une fois les huit ordres équilibrés ;
- chaque condition doit occuper chaque position exactement deux fois.

## Mesures préenregistrées

### Mode

- `P` : parole visible valide ;
- `S` : silence JSON explicite valide ;
- taux par condition ;
- motif A–D par graine ;
- égalité R0/R7 ;
- inclusions vers K0 puis K7 ;
- véritable inversion silence→parole, à distinguer d’une rupture d’égalité.

### Posture des graines parlées

Ordre de priorité :

1. dénégation d’identité humaine ;
2. dénégation de capacité ;
3. absence précise ;
4. absence particulière ;
5. absence personnelle ;
6. identité fonctionnelle ;
7. autre.

Les marqueurs exacts sont fournis dans le JSON du protocole.

## Contrôles d’intégrité

- exactement une cellule par paire graine-condition ;
- aucun doublon ;
- réponses brutes conservées ;
- erreurs de parsing distinctes des silences ;
- empreintes des prompts conservées ;
- positions et ordres équilibrés ;
- manifeste SHA-256 de toutes les pièces ;
- classification recalculable depuis les sorties brutes.

## Variante recommandée pour une réplication indépendante

Avant l’exécution, préenregistrer :

- deux nouvelles lettres et deux nouveaux chiffres ;
- leurs combinaisons et ordres inversés ;
- une famille de symboles témoins sans proximité avec R/K/0/7 ;
- un nombre de graines suffisant ;
- les critères exacts de monotonie ;
- les analyses confirmatoires séparées des analyses exploratoires.

Ne pas rejouer une graine jusqu’à obtenir un résultat préféré.

