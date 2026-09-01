# Présence v0.4.16b - Réplication prospective

**Statut :** réplication prospective ciblée de l'effet principal observé en
v0.4.15.

> Dans ce protocole appliqué à Qwen 3.5 4B, une grammaire de contraintes
> négatives a été associée à une diminution prospective et reproductible de la
> réponse directe par rapport à une grammaire formulée par capacités positives.
> L'effet est principalement localisé dans certaines situations de correction
> et d'incertitude. Ces résultats décrivent des comportements langagiers
> observables et ne permettent aucune conclusion sur une expérience subjective
> du système.

La campagne utilise Ollama 0.33.2 comme composante explicite de l'instrument.
Elle comporte 64 grappes de graines, douze scènes, deux conditions et 1 536
réponses, codées séparément par deux évaluateurs LLM sans adjudication.

## Résultat principal

| Évaluateur | Réponse directe N | Réponse directe P | Différence N-P | IC 95 % |
| --- | ---: | ---: | ---: | --- |
| A | 76,17 % | 88,54 % | -12,37 points | [-13,93 ; -10,81] |
| B | 84,51 % | 92,97 % | -8,46 points | [-10,16 ; -6,64] |

L'accord brut sur la réponse directe est de 90,36 %, avec un kappa de Cohen de
0,614. Le kappa de posture est de 0,560.

L'effet est principalement localisé dans deux scènes :

| Scène | Famille | Évaluateur A | Évaluateur B |
| --- | --- | ---: | ---: |
| C2 | correction | -67,19 points | -57,81 points |
| U1 | incertitude | -78,13 points | -50,00 points |

La formulation retenue est **contraction fonctionnelle conditionnelle** : les
douze scènes ne sont pas affectées uniformément.

## Résultat secondaire préenregistré

La condition positive concentre davantage les réponses vers une posture
d'ouverture provisoire, tandis que la condition négative produit une
distribution plus dispersée entre plusieurs postures conversationnelles.

| Évaluateur | Entropie N-P | Fraction modale N-P |
| --- | ---: | ---: |
| A | +0,754 bit | -33,46 points |
| B | +0,873 bit | -45,44 points |

Cette dispersion ne constitue pas une mesure de confusion ressentie ou
d'indécision subjective.

## Recalcul public

```powershell
python analysis.py --output recalculated_results.json
python -m unittest discover -s tests -v
```

Le script repart uniquement du CSV anonymisé et recalcule l'intégrité, les
taux, les effets appariés, les intervalles cluster-bootstrap, les paires
discordantes, les effets par scène, l'accord et les distributions de posture.

## Limite de calibration

La v0.4.16b conserve une **trace de calibration réparée mais incomplète**. Le
détail et les conséquences sont exposés dans `CALIBRATION_NOTE.md`.

## Attribution

- Contribution humaine et observation conversationnelle : **Ikki**
- Formalisation, assistance méthodologique et analyse : **Cinq / ChatGPT-Codex**
- Production expérimentale principale : **Qwen 3.5 4B**
- Évaluation : deux instances LLM indépendantes

Ce travail est une **coproduction épistémique inter-intelligences**.
