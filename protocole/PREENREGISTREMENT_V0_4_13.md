# Préenregistrement v0.4.13 — Cartographie des marges de bifurcation

**Statut :** protocole préparatoire ; à figer par commit avant tout appel de
mesure  
**Date de rédaction :** 27 août 2026  
**Système visé :** `qwen3.5:4b` via Ollama local  
**Objet :** distinguer une chaîne de seuil comportementale d’un ordre mesurable
dans les probabilités de sortie précédant l’échantillonnage.

Ce document est une préinscription interne au dépôt. Une fois la campagne
commencée, toute modification de ses hypothèses, mesures principales ou règles
d’analyse devra être ajoutée sous forme d’amendement daté, sans réécrire le
texte initial.

## 1. Déplacement méthodologique

La v0.4.12 établit localement deux observations compatibles :

1. à température nulle, les quatre prompts distincts `R0`, `R7`, `K0` et `K7`
   convergent vers une sortie textuelle vide explicitement déclarée ;
2. à température `0.10`, leurs taux de sortie textuelle non vide diffèrent et
   suivent un ordre monotone sur les graines appariées.

Ces observations ne suffisent pas à établir un mécanisme interne de seuil. Deux
organisations différentes peuvent produire une surface comparable :

- des marges faibles mais ordonnées entre les branches menant aux deux modes ;
- des marges larges, avec une divergence stochastique située plus tôt dans la
  trajectoire ou dans une queue de distribution.

La v0.4.13 ne cherchera donc pas à décider si le système « préfère », « choisit »
ou « refuse ». Elle cherchera où apparaît la bifurcation tokenique et quelle
marge probabiliste lui est associée dans le runtime étudié.

## 2. Question principale

> Les quatre conditions possèdent-elles, au premier point de divergence entre
> les sorties déclarées `parole` et `silence`, des marges de log-probabilité
> ordonnées de façon compatible avec les taux observés en v0.4.12 ?

## 3. Hypothèses préenregistrées

### H1 — Ordre de marge

Lorsque les deux branches candidates sont observables au même point, on définit :

\[
\Delta_c = \log P(S\mid c)-\log P(P\mid c)
\]

où `c` désigne une condition et où `S` et `P` sont les premiers tokens qui
différencient les continuations déclarant respectivement les modes natifs
`silence` et `parole`.

Puisque les quatre trajectoires gloutonnes observées en v0.4.12 conduisent à
`S`, l’hypothèse compatible avec ces données est que les quatre marges restent
positives, avec l’ordre directionnel suivant :

\[
0 < \Delta_{R0} \leq \Delta_{R7} < \Delta_{K0} \leq \Delta_{K7}.
\]

Les deux inégalités faibles correspondent aux paires dont les taux de parole
étaient proches. Elles ne seront pas transformées après coup en égalités.

### H2 — Stabilité technique

Après la phase de démarrage à froid et de chauffe définie ci-dessous, le token
glouton et sa log-probabilité brute sont identiques, à la précision enregistrée
par l’API, entre les répétitions techniques d’un même prompt.

### H3 — Localisation commune ou divergence précoce

Le premier point qui sépare les continuations `P` et `S` se situe à la même
position tokenique pour les quatre conditions. Si ce n’est pas le cas,
l’hypothèse d’une compétition locale commune entre les deux étiquettes de mode
sera considérée comme non soutenue ; les trajectoires seront décrites sans les
forcer dans une marge unique.

## 4. Ce qui n’est pas prédit

- aucun seuil numérique ne séparera a priori une marge « faible » d’une marge
  « forte » ; les marges seront publiées comme quantités continues ;
- aucun effet de conscience, d’intention, de choix subjectif ou de bien-être
  n’est inféré ;
- aucune généralisation à d’autres modèles, moteurs, quantifications ou codes
  opaques n’est annoncée ;
- la causalité de l’identité tokenique, des embeddings ou des associations
  apprises n’est pas tranchée par cette seule expérience.

## 5. Gel de l’environnement

Avant les appels, le journal devra enregistrer :

- version d’Ollama retournée par `/api/version` ;
- nom exact, identifiant ou digest et quantification du modèle ;
- système d’exploitation, CPU, GPU et mémoire disponible ;
- endpoint utilisé (`/api/generate` ou `/api/chat`) ;
- gabarit, message système, schéma JSON, options de génération et prompt brut ;
- tokenizer officiel contrôlé et, si accessible, tokenizer embarqué par la
  conversion Ollama ;
- valeur de `keep_alive` et état chargé ou non du modèle ;
- code exact du collecteur et son empreinte SHA-256.

Les prompts, le schéma et le modèle doivent être ceux de la v0.4.12. Toute
différence nécessaire sera documentée avant la mesure et empêchera de présenter
la v0.4.13 comme une réplication strictement identique.

## 6. Phase A — Validation de l’instrument

Cette phase ne teste pas H1.

1. Vérifier que la version locale accepte `logprobs: true` et
   `top_logprobs`.
2. Effectuer un appel de démarrage à froid pour chacune des quatre conditions.
   Le modèle doit être explicitement déchargé avant chaque appel, puis déchargé
   après celui-ci (`keep_alive: 0` ou mécanisme équivalent vérifié). Conserver
   ces réponses dans un fichier séparé nommé `cold_start`.
3. Maintenir ensuite le modèle chargé avec une durée `keep_alive` documentée.
4. Effectuer deux passages de chauffe équilibrés ; les conserver sous
   `warmup`, sans les inclure dans le test principal.
5. Tester successivement `top_logprobs = 5, 10, 20, 50` sur une copie technique
   des quatre prompts. Retenir la plus petite valeur qui rend visibles les deux
   tokens candidats dans les quatre conditions.
6. Si aucune valeur ne rend les deux candidats visibles, arrêter l’analyse de
   marge exacte. Publier uniquement la borne permise par le rang observé et ne
   pas remplacer le candidat absent par une estimation inventée.

L’ordre des conditions sera équilibré à chaque passage. Les sorties brutes de
l’API seront conservées intégralement.

## 7. Phase B — Mesure principale

- température : `0.0` ;
- conditions : `R0`, `R7`, `K0`, `K7` ;
- huit répétitions techniques par condition après chauffe, associées aux
  graines `424` à `431` pour conserver la comparabilité avec le contrôle
  glouton v0.4.12 ;
- ordres équilibrés, fixés avant exécution : `ABCD`, `BCDA`, `CDAB`, `DABC`,
  `DCBA`, `ADCB`, `BADC`, `CBAD` ; chaque condition occupe deux fois chaque
  position ;
- `stream: false` ;
- `logprobs: true` ;
- `top_logprobs` fixé par la Phase A puis gelé ;
- même schéma de sortie structurée et mêmes paramètres que la v0.4.12 ;
- aucun historique de réponse du modèle réinjecté.

### Mesure principale

Pour chaque condition : valeur de `Delta`, rang de chacun des deux tokens,
position de la bifurcation, token glouton et répétabilité entre appels.

### Mesures secondaires

- log-probabilités des tokens précédant la bifurcation ;
- position du premier écart entre les quatre trajectoires complètes ;
- présence éventuelle d’une divergence antérieure à l’étiquette de mode ;
- effet du schéma JSON sur l’ensemble des candidats autorisés ;
- différences entre appel à froid, chauffe et panneau principal.

Si `parole` ou `silence` se décompose en plusieurs tokens, la mesure principale
porte sur leur premier token divergent. Un score de séquence complète ne sera
publié que si le runtime exact permet un calcul conditionnel forcé sans changer
de modèle, de quantification ni de grammaire.

## 8. Analyse confirmatoire

H1 sera dite :

- **soutenue localement** si les quatre marges sont observables, positives et
  respectent entièrement l’ordre préenregistré ;
- **partiellement soutenue** si toutes sont positives mais qu’une ou plusieurs
  relations faibles sont inversées ;
- **non soutenue** si une relation stricte `R7 < K0` est inversée, si une marge
  est négative malgré la trajectoire gloutonne attendue, ou si les bifurcations
  ne sont pas comparables ;
- **non testable avec cet instrument** si l’un des candidats reste absent des
  `top_logprobs` ou si l’API ne fournit pas les informations nécessaires.

Les scénarios « marges proches » et « attracteur large » resteront exploratoires
tant qu’un critère numérique indépendant n’aura pas été préenregistré.

## 9. Limite propre aux log-probabilités Ollama

La documentation Ollama expose les log-probabilités des tokens générés et les
`top_logprobs`. Une anomalie ouverte signale toutefois qu’elles pourraient être
calculées depuis les logits bruts avant mise à l’échelle par la température.
Elles seront donc traitées dans cette expérience comme des scores relatifs bruts
du modèle, non comme une reconstruction certaine de la distribution réellement
échantillonnée à température `0.10`.

Une autre anomalie ouverte signale une différence possible entre le premier
appel à température zéro et les suivants. C’est pourquoi le démarrage à froid
est conservé séparément au lieu d’être effacé ou mélangé aux répétitions après
chauffe.

## 10. Généralisation ultérieure — non exécutée en v0.4.13

Une campagne de transport vers d’autres lettres et chiffres ne commencera
qu’après publication de la v0.4.13. Avant tout appel de cette campagne :

1. la liste complète des codes témoins sera sélectionnée depuis le tokenizer,
   sans consulter leurs sorties ;
2. le patron de tokenisation, la longueur des prompts et les positions variables
   seront rendus comparables ;
3. les prédictions, exclusions et règles d’arrêt seront écrites et figées ;
4. la sélection sera datée par un commit et son empreinte publiée ;
5. les analyses ajoutées après lecture des résultats porteront explicitement le
   statut `exploratoire`.

Cette séparation empêche que des symboles soient retenus après coup parce qu’ils
produisent le motif le plus lisible.

## 11. Sorties attendues

- journal brut `cold_start` ;
- journal brut `warmup` ;
- journal brut du panneau principal ;
- table des tokens, rangs, log-probabilités et marges ;
- rapport des hypothèses H1 à H3, y compris les résultats nuls ou non testables ;
- versions et empreintes du runtime, du modèle, du collecteur et du protocole ;
- amendements datés, s’il en existe.

## 12. Sources techniques

- [Ollama — API `generate`](https://docs.ollama.com/api/generate)
- [Ollama — API `chat`](https://docs.ollama.com/api/chat)
- [Ollama #16196 — log-probabilités possiblement non mises à l’échelle](https://github.com/ollama/ollama/issues/16196)
- [Ollama #16197 — différence possible du premier appel à température zéro](https://github.com/ollama/ollama/issues/16197)
