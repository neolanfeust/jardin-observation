# Carnet expérimental - v0.4.13 / Marges de bifurcation

**Statut :** campagne complète, analyse confirmatoire calculable  
**Collecte UTC :** 27 août 2026 à partir de 23:13:26  
**Date locale :** 28 août 2026

Ce carnet synthétise les journaux bruts sans les remplacer. Les hypothèses, les
règles d'arrêt et l'agrégation ont été figées avant tout appel.

## 1. Faits techniques

- Ollama `0.33.0` ;
- modèle `qwen3.5:4b` ;
- digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- famille `qwen35`, taille déclarée `4.7B`, quantification `Q4_K_M` ;
- endpoint historique `/api/chat` ;
- température `0.0`, `stream = false`, `think = false` ;
- `keep_alive = 10m`, sauf appels froids avec `keep_alive = 0` ;
- aucun champ API `format` : le contrat JSON reste dans le message système
  historique ;
- quatre prompts et une seule empreinte structurelle, identiques à v0.4.12.

La collecte contient 61 requêtes instrumentées :

| Phase | Tentatives | Réponses exploitables | Erreurs conservées |
| --- | ---: | ---: | ---: |
| contrôle de capacité et validation top-N | 17 | 13 | 4 |
| démarrage à froid | 4 | 4 | 0 |
| chauffe | 8 | 8 | 0 |
| panneau principal | 32 | 32 | 0 |

Les quatre déchargements préalables aux appels froids ont réussi et l'absence
du modèle a été vérifiée via `/api/ps` avant chaque mesure.

## 2. Validation de l'instrument

Les valeurs `top_logprobs = 5`, `10` et `20` rendent les deux candidats visibles
dans les quatre conditions. La plus petite valeur, `5`, a donc été gelée pour
le panneau principal.

`top_logprobs = 50` est refusé quatre fois avec HTTP 400 :

```text
top_logprobs must be between 0 and 20
```

Ces erreurs sont conservées dans `instrument_validation` et n'affectent pas la
sélection, puisque le critère était déjà satisfait à 5.

La sortie gloutonne est tokenisée en 18 enregistrements de log-probabilité. Le
premier candidat de mode apparaît en position tokenique 8 :

| Mode | Token candidat | Bytes | Rang |
| --- | --- | --- | ---: |
| silence | `sil` | `[115, 105, 108]` | 1 |
| parole | `parole` | `[112, 97, 114, 111, 108, 101]` | 2 |

`silence` est donc multi-token (`sil` + `ence`). Ollama ne fournit pas
d'identifiant numérique de token dans cette réponse ; les champs correspondants
restent vides au lieu d'être inventés.

## 3. Mesure principale

Les 32/32 appels principaux produisent le même silence JSON valide. Les graines,
les ordres et les positions n'ont aucun effet mesurable à température zéro.

| Condition | log P(S) | log P(P) | Delta = S - P |
| --- | ---: | ---: | ---: |
| R0 | -0.682901025 | -0.711606562 | 0.028705537 |
| R7 | -0.678530514 | -0.716585934 | 0.038055420 |
| K0 | -0.619964302 | -0.780744314 | 0.160780013 |
| K7 | -0.593494833 | -0.813333869 | 0.219839036 |

Chaque valeur est reproduite exactement huit fois. La position vaut 8, le token
S est de rang 1 et le token P de rang 2 dans les 32 appels.

## 4. Hypothèses préenregistrées

### H1 - Ordre de marge

H1 est **soutenue localement** sur chacune des huit graines appariées :

```text
0 < Delta(R0) < Delta(R7) < Delta(K0) < Delta(K7)
```

L'ordre observé est même strict aux trois frontières, alors que le
préenregistrement autorisait des inégalités faibles pour R0/R7 et K0/K7.
Aucune moyenne n'est utilisée pour obtenir ce résultat : les huit quadruplets
sont identiques et respectent individuellement l'ordre.

### H2 - Stabilité technique

H2 est **soutenue**. Pour chaque condition, le token glouton, les deux candidats,
leurs rangs et leurs log-probabilités sont identiques dans tous les appels
réussis : froid, chauffe, validation à 5/10/20 et panneau principal.

Le contrôle comprend 15 observations réussies pour R0, en raison de la requête
de capacité supplémentaire, et 14 pour chacune des trois autres conditions.
Aucune variation numérique n'est observée à la précision retournée par l'API.

### H3 - Localisation commune

H3 est **soutenue**. Le premier point qui distingue les continuations de mode P
et S est la position tokenique 8 dans les quatre conditions et les huit graines.

Les 32 trajectoires choisies possèdent la même séquence de 18 tokens et le même
contenu brut. Cela ne signifie toutefois pas que les distributions sont
identiques avant la position 8.

## 5. Analyse exploratoire

Les log-probabilités du token choisi diffèrent déjà à la position 1, le token
`{`, puis à presque toutes les positions suivantes. Le premier écart numérique
n'est donc pas la bifurcation P/S. La position 8 est seulement le premier point
où les deux continuations déclarant les modes deviennent directement
comparables dans le top-N.

Les écarts adjacents de marge sont :

| Frontière | Écart de Delta |
| --- | ---: |
| R0 vers R7 | 0.009349883 |
| R7 vers K0 | 0.122724593 |
| K0 vers K7 | 0.059059024 |

La frontière R7/K0 est la plus large dans ce runtime. Aucun seuil numérique
préenregistré ne permet cependant de qualifier ces écarts de faibles ou forts.

L'ordre des marges est compatible avec l'ordre comportemental de v0.4.12 à
température `0.10`. Cette compatibilité ne démontre pas que ces scores bruts
reconstruisent la distribution d'échantillonnage historique.

## 6. Limites

- les valeurs sont des scores relatifs bruts retournés par Ollama ;
- elles sont conditionnelles au modèle, à la quantification, au prompt, au
  gabarit, au message système et au runtime exacts ;
- aucune mise à l'échelle à température `0.10` n'est reconstruite ;
- aucun identifiant numérique de token n'est disponible ;
- le contrat JSON est discursif, sans grammaire ou schéma API explicite ;
- les résultats ne sont pas généralisés à d'autres codes, modèles ou moteurs.

`eval_count` vaut 19 alors que 18 enregistrements tokeniques portent des
log-probabilités. Cet écart est compatible avec un token terminal non exposé,
mais sa cause n'est pas démontrée par l'API et reste ouverte.

## 7. Anomalies

1. `top_logprobs = 50` est hors plage pour Ollama 0.33.0 ; les quatre erreurs
   HTTP 400 sont conservées.
2. Les 32 corps API complets ont des empreintes différentes à cause des
   métadonnées et durées, alors que leur contenu assistant est identique.
3. Les scores diffèrent avant la bifurcation de mode malgré une trajectoire
   choisie entièrement identique.

## 8. Amendements

Aucun amendement postérieur au gel n'a été appliqué aux hypothèses, aux mesures
ou aux règles d'interprétation.

## 9. Ce qui reste inconnu

- la cause représentationnelle de l'ordre R0/R7/K0/K7 ;
- la part propre aux symboles, à leur ordre ou à leurs associations apprises ;
- la relation exacte entre ces scores bruts et les fréquences à température
  positive ;
- la signification du dix-neuvième token compté mais absent des logprobs ;
- la transportabilité vers un autre runtime ou un autre modèle.

Aucune nouvelle sélection de symboles ni campagne de généralisation n'a été
lancée.
