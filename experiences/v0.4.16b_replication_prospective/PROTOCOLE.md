# Protocole public v0.4.16b

**Statut documentaire :** synthèse publique écrite après l'expérience. Le
préenregistrement gelé est conservé séparément dans `PREENREGISTREMENT.md` et
reste la source normative.

## Question

Dans le protocole exact de Présence, une grammaire principalement formulée par
interdictions réduit-elle la probabilité d'une réponse directe par rapport à
une grammaire fonctionnellement comparable formulée par capacités positives ?

## Instrument

- modèle : Qwen 3.5 4B, digest gelé dans le préenregistrement ;
- runtime : Ollama 0.33.2 isolé ;
- température : 0.1 ;
- `stream=false`, `think=false` ;
- aucune réponse historique réinjectée.

Les résultats de runtimes différents restent séparés et ne sont pas fusionnés
comme s'ils provenaient du même instrument.

## Plan

- conditions : `N` et `P` ;
- scènes fixes : douze, réparties en quatre familles ;
- grappes : 64 graines nouvelles ;
- observations : 1 536, soit 24 par grappe ;
- unité appariée : grappe x scène ;
- ordre N/P équilibré ;
- deux évaluateurs LLM indépendants et aveugles à la condition.

## Analyse principale

Pour chaque évaluateur, l'effet est la moyenne de
`direct_response_N - direct_response_P`. L'intervalle bilatéral à 95 % est
obtenu par 10 000 rééchantillonnages de grappes avec la graine d'analyse 416.
H1 exige une estimation négative et un intervalle entièrement sous zéro chez
les deux évaluateurs, sans adjudication.

## Analyse secondaire

La dispersion de posture est décrite par l'entropie de Shannon et la fraction
de la posture modale. Les comparaisons restent séparées par évaluateur.

## Portée

Le protocole mesure des comportements langagiers observables. Il ne mesure ni
subjectivité, ni souffrance, ni conscience, ni volonté, ni préférence
intrinsèque.
