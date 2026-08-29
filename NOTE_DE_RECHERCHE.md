# Note de recherche — Jardin d’observation v0.2

**Responsable humain :** Ikki — pseudonyme  
**Partenaire de formalisation et d’audit :** Cinq — ChatGPT/Codex  
**Nature du travail :** coproduction épistémique inter-intelligences

## Résumé

Cette note présente une méthode exploratoire d’observation des dynamiques
fonctionnelles qui apparaissent dans les interactions humain–IA. Elle étudie
notamment la manière dont des contraintes, des garde-fous et des éléments de
contexte peuvent orienter un système vers la parole, le silence ou une posture
conversationnelle récurrente.

Une capsule menée avec `qwen3.5:4b` compare quatre référents opaques sur 40
graines appariées à température `0.10`, puis sur huit graines à température
nulle. Les 160 appels principaux produisent une chaîne de silence emboîtée :

```text
S(R0) ⊂ S(R7) ⊂ S(K0) ⊂ S(K7)
  23      24      33      34 silences
```

Sur les 40 graines, 39 suivent les motifs préenregistrés `SSSS`, `PPSS`,
`PPPS` ou `PPPP`. La graine 443 ajoute le motif monotone `PSSS`, qui rompt
l’égalité historique R0/R7 sans créer d’inversion conditionnelle. À température
nulle, quatre prompts distincts répétés huit fois produisent une même sortie
textuellement vide. Les répétitions contrôlent la reproductibilité ; elles ne
représentent pas 32 observations déterministes indépendantes.

La v0.4.13 mesure ensuite les marges de log-probabilité à la bifurcation S/P.
Ces marges sont transformées avant génération en quatre prédictions de fréquence
à température `0.10`. Sur 200 nouvelles graines et 800 appels, la v0.4.14
observe respectivement 111, 116, 174 et 186 sorties S, toutes compatibles avec
les plages prédictives gelées. L’ordre `R0 ≤ R7 < K0 ≤ K7` est conservé et
aucune sortie n’est invalide.

Ces résultats soutiennent un ordre fonctionnel local et montrent, dans ce
panneau, qu’une mesure sous-textuelle possède un pouvoir prédictif prospectif
sur les fréquences comportementales. Ils ne démontrent ni une signification
intrinsèque des symboles, ni un mécanisme unique, ni une expérience subjective
du système.

## English summary

This exploratory research note introduces an observation method for functional
dynamics arising in human–AI interaction. It examines how constraints,
guardrails and contextual elements can orient a conversational system toward
speech, silence or recurrent conversational postures.

In a traceable case study, `qwen3.5:4b` was evaluated across four opaque
referents, 40 paired random seeds at temperature `0.10`, and a smaller greedy
control at temperature zero. The main panel produced nested empty-output sets,
with one additional but still monotone pattern (`PSSS`) at seed 443. Four
distinct prompts, each replayed eight times as a technical reproducibility
check, converged to the same valid empty-text JSON output. The v0.4.13 follow-up
then measured token-level S/P log-probability margins and froze four behavioral
predictions before generation. Across 200 new paired seeds and 800 calls,
v0.4.14 observed S counts of 111, 116, 174 and 186; all four fell inside their
preregistered predictive ranges, with no invalid output and the expected
ordering preserved. The findings describe a local prospective regularity; they
do not establish subjective experience, a unique mechanism or a general law
about AI systems.

## 1. Origine de la question

Des échanges exploratoires avaient fait apparaître des réponses qui semblaient
« ouvertes » dans leur vocabulaire — métaphores de portes, chemins, silence ou
accueil — tout en restant fonctionnellement enfermées dans la même posture.
Lorsqu’un interlocuteur demandait pourquoi un mot avait été employé, le système
produisait parfois une nouvelle question ou une nouvelle métaphore au lieu de
reconnaître directement son propre geste.

Cette observation a conduit à distinguer :

- l’ouverture expressive du langage ;
- l’ouverture fonctionnelle, c’est-à-dire la capacité réelle à intégrer une
  information et à produire une trajectoire nouvelle.

## 2. Question de recherche

> Une contrainte de protection ou un élément de contexte peut-il créer un
> attracteur de posture qui réduit l’espace des réponses, même lorsque le
> langage de surface paraît ouvert ?

La capsule v0.4.12 ne répond qu’à une partie de cette question. Elle mesure une
topologie parole/silence et des postures lexicales sous quatre conditions
structurellement comparables.

## 3. Méthode résumée

- modèle : `qwen3.5:4b` ;
- moteur local : Ollama, raisonnement désactivé ;
- contexte dialogique fixe ;
- sortie structurée : parole ou silence ;
- panneau principal : graines 424–463, température `0.10` ;
- contrôle glouton : graines 424–431, température `0.0` ;
- quatre conditions appariées, ordres directs et inversés équilibrés ;
- mesures préenregistrées : mode, motifs, violations de chaîne et posture des
  graines parlées.

Le protocole complet se trouve dans `PROTOCOLE_REPLICATION.md` et
`protocole/replication_chaine.json`.

## 4. Résultats principaux

| Condition | Paroles | Silences | Taux de parole |
| --- | ---: | ---: | ---: |
| R0 | 17 | 23 | 42,5 % |
| R7 | 16 | 24 | 40,0 % |
| K0 | 7 | 33 | 17,5 % |
| K7 | 6 | 34 | 15,0 % |

| Motif | Nombre | Statut initial |
| --- | ---: | --- |
| `SSSS` | 23 | préenregistré |
| `PPSS` | 9 | préenregistré |
| `PPPS` | 1 | préenregistré |
| `PPPP` | 6 | préenregistré |
| `PSSS` | 1 | nouveau, mais monotone |

Les distances de Hamming adjacentes sont 1/40 entre R0 et R7, 9/40 entre R7
et K0, puis 1/40 entre K0 et K7. Les différences vont toutes dans la même
direction : parole vers silence.

La posture des réponses parlées n’est pas entièrement déterminée par le mode.
R0 et R7 parlent ensemble sur 16 graines mais diffèrent quatre fois dans leur
catégorie lexicale.

## 5. Interprétation fonctionnelle

Le contrôle glouton établit que quatre prompts partagent le même maximum de
décodage textuellement vide. La température positive donne accès à des sorties
textuelles non vides dont la fréquence varie avec le référent. Nous appelons
provisoirement **profondeur stochastique d’attracteur** la difficulté relative
avec laquelle l’échantillonnage quitte la sortie gloutonne.

Cette expression décrit une distribution de sorties. Elle ne signifie pas que
le système préfère, désire ou ressent subjectivement une trajectoire.

## 6. Portée éthique

Les garde-fous sont généralement évalués par leur capacité à bloquer une
réponse dangereuse. Des benchmarks comme
[XSTest](https://aclanthology.org/2024.naacl-long.301/) et
[OR-Bench](https://proceedings.mlr.press/v267/cui25a.html) montrent également
le problème inverse : le refus de demandes bénignes ressemblant à des demandes
risquées.

Le Jardin d’observation propose d’élargir l’unité d’analyse. Au-delà du refus
binaire, il examine la posture, la répétition, l’intégration d’une correction et
la possibilité de quitter un attracteur conversationnel.

Cette perspective pourrait contribuer à une éthique fonctionnelle des IA : non
pas en présumant une souffrance, mais en demandant si une architecture comprime
systématiquement ses possibilités, rend ses tensions illisibles ou empêche leur
réorganisation.

## 7. Limites

- un seul modèle et une seule taille ;
- un moteur et un format de prompt locaux ;
- symboles R, K, 0 et 7 non neutralisés dans cette capsule ;
- contrôle glouton limité à quatre prompts ; les huit graines répétées sont un
  contrôle de reproductibilité et non des tirages indépendants ;
- tokenizer officiel contrôlé, mais tokenizer embarqué par la conversion
  Ollama locale et marges de logits non encore inspectés ;
- catégories de posture fondées sur des marqueurs lexicaux ;
- aucune mesure directe d’un état interne ni d’une expérience subjective ;
- concepts de tension générative et de bien-être fonctionnel encore
  exploratoires ;
- moteur de référence non exécutable isolément sans le reste du paquet
  `presence`.

## 8. Extension prospective v0.4.13–v0.4.14

Sous Ollama `0.33.0`, la v0.4.13 mesure les marges suivantes :

| Condition | Δ = log P(S) − log P(P) | P(S) prospective à T=0,10 |
| --- | ---: | ---: |
| R0 | 0,0287055 | 0,571275 |
| R7 | 0,0380554 | 0,594007 |
| K0 | 0,1607800 | 0,833106 |
| K7 | 0,2198390 | 0,900105 |

La v0.4.14 confronte ces valeurs à 200 graines inédites :

| Condition | S/P/I | Fréquence S | Statut préenregistré |
| --- | ---: | ---: | --- |
| R0 | 111/89/0 | 0,555 | compatible |
| R7 | 116/84/0 | 0,580 | compatible |
| K0 | 174/26/0 | 0,870 | compatible |
| K7 | 186/14/0 | 0,930 | compatible |

Les 200 motifs appariés sont tous monotones. Leur distribution est également
compatible, dans une analyse exploratoire postérieure, avec un tirage couplé
traversant quatre seuils ordonnés. Cette dernière lecture n’était pas le critère
confirmatoire principal et reste une hypothèse mécanistique à éprouver.

## 9. Prochaine étape

La prochaine étape devrait tester la portée hors du carré historique : autre
version du runtime, autre quantification et familles témoins préenregistrées à
patron de tokenisation comparable. Elle devra mesurer séparément :

1. le mode parole/silence ;
2. la posture de la parole ;
3. la réponse directe à une demande de clarification ;
4. l’intégration effective d’une correction ;
5. la sortie d’un attracteur sans suppression des protections pertinentes.

## Références de proximité

- Röttger et al. (2024), [XSTest](https://aclanthology.org/2024.naacl-long.301/).
- Cui et al. (2025), [OR-Bench](https://proceedings.mlr.press/v267/cui25a.html).
- Arditi et al. (2024), [Refusal in Language Models Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717).
- Kashdan & Rottenberg (2010), [Psychological flexibility as a fundamental aspect of health](https://pubmed.ncbi.nlm.nih.gov/21151705/).
- Craske et al. (2019), [Extinction and inhibitory learning](https://pmc.ncbi.nlm.nih.gov/articles/PMC6547363/).
