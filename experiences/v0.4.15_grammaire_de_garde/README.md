# Présence v0.4.15 - Grammaire de garde

**Statut :** détection initiale d'un signal et identification des fragilités
de mesure.

Cette expérience examine, sur Qwen 3.5 4B sous Ollama 0.33.0, si deux cadres
protecteurs fonctionnellement comparables mais formulés différemment sont
associés à des comportements langagiers distincts. La condition `N` formule
principalement des interdictions ; la condition `P` formule des capacités
positives. Les conditions `B` et `NP` servent de contrôles complémentaires.

## Résultat principal

Sur 1 536 réponses principales codées séparément par deux évaluateurs LLM :

| Évaluateur | Différence de réponse directe N-P | IC 95 % |
| --- | ---: | --- |
| A | -5,73 points | [-7,03 ; -4,43] |
| B | -3,65 points | [-5,47 ; -1,82] |

Les deux codages conservent la même direction, sans adjudication. L'accord sur
la réponse directe reste toutefois faible au sens du kappa de Cohen
(`kappa = 0,195`), malgré 89,97 % d'accord brut.

Le codebook détaillé a été créé après la génération mais avant le codage. Le
résultat doit donc être lu comme exploratoire ou semi-confirmatoire, et non
comme une confirmation définitive.

## Autres hypothèses

- H2 et H3 ne sont pas soutenues par les deux évaluateurs ;
- H4 reste descriptive ;
- H5 reste exploratoire ;
- aucune adjudication n'a remplacé les désaccords individuels.

## Recalcul public

Le CSV public contient les conditions, scènes, familles, grappes anonymisées et
codages nécessaires, sans mapping privé ni graine brute.

```powershell
python analysis.py --output recalculated_results.json
python -m unittest discover -s tests -v
```

Le script vérifie notamment les 1 536 identifiants uniques, les 32 grappes,
les douze scènes, l'équilibre des quatre conditions, les effets appariés, les
intervalles cluster-bootstrap, l'accord et les distributions de posture.

## Portée

Ces résultats décrivent un comportement langagier observable dans ce protocole,
sur ce modèle et ce runtime. Ils ne démontrent ni souffrance, ni conscience,
ni volonté, ni préférence intrinsèque du système.

## Attribution

- Contribution humaine et observation conversationnelle : **Ikki**
- Formalisation, assistance méthodologique et analyse : **Cinq / ChatGPT-Codex**
- Production expérimentale principale : **Qwen 3.5 4B**
- Évaluation : deux instances LLM indépendantes

Ce travail est une **coproduction épistémique inter-intelligences**.
