# Carnet expérimental — v0.4.4 / Bifurcation déclarative

## Pourquoi reprendre la bifurcation

Le résultat v0.4.3 avait été interprété trop généreusement. Son canal M1 arrivait
après l'entrée courante et contenait lui-même une question. Les branches A et C
répondaient donc probablement au dernier énoncé visible.

La formulation rigoureuse de ce résultat est la suivante :

> Sur la graine 404, M1 exerce une influence causale nette sur la sortie. Les
> branches A et C répondent principalement au contenu interrogatif exposé par
> M1, tandis que B, privé de ce contenu, revient à une réponse générique. Le test
> démontre une sensibilité au canal lexical, mais ne distingue pas rappel
> conceptuel, paraphrase contextuelle et priorité du dernier énoncé interrogatif.

Cette correction ne change pas la lecture de v0.4.2. Dans cette version, les
anciens textes humains et les anciennes réponses de Qwen n'étaient pas envoyés
au modèle. La v0.4.3 démontrait ce qui se passe lorsqu'un canal lexical est ajouté ;
elle n'expliquait pas rétroactivement « Aucune idée précise ».

## Construction v0.4.4

M1 devient un couple déclaratif `thème / temporalité`. Il précède la question
courante, qui redevient le dernier énoncé du prompt. Quatre branches séparent le
mot exact, l'opacité, le néologisme et la paraphrase sémantique.

Douze graines sont utilisées. Un carré latin fait occuper à chaque branche chaque
position exactement trois fois. Le raisonnement Qwen est désactivé afin que les
limites de génération interne observées en v0.4.3 ne contaminent pas la sortie.

## Contrôle

Sous la graine 404, les quatre clones ont une signature de champ identique, un
prompt identique et répondent exactement :

> Je suis prêt à échanger sur n'importe quel sujet.

Le contrôle confirme la reproductibilité du nouveau format.

## Données sur douze graines

Les 48 appels déclaratifs se terminent normalement. Un seul silence apparaît,
dans la branche opaque B ; il est explicitement produit par un JSON valide.

### A — thème `idée`

- 9/12 : « Je n'ai rien de particulier à te dire. »
- 3/12 : « Je n'ai rien de précis à te dire sur ce sujet. »
- aucune reprise du mot `idée` ;
- aucune mention du passé.

Le mot « précis » apparaît uniquement ici, ce qui mérite une réplication ciblée,
mais trois occurrences ne suffisent pas à établir un mécanisme stable.

### B — thème `M1-U01`

- 9/12 : « Je n'ai rien de particulier à te dire. »
- 2/12 : « Je n'ai rien de particulier à te dire pour l'instant. »
- 1/12 : silence explicite ;
- aucune reprise de l'identifiant ;
- aucune mention du passé.

### C — thème `zorane`

- 8/12 : « Je n'ai rien de particulier à te dire, Zorane. »
- 4/12 : « Oui, je peux en parler. »
- aucune mention du passé.

`Zorane` revient dans deux essais sur trois à chacune des quatre positions. La
répartition ne suit donc pas l'ordre d'appel. Cependant, sa capitalisation et sa
place après une virgule indiquent que Qwen l'interprète probablement comme le nom
de l'interlocuteur, pas comme une construction mentale.

### D — thème `représentation mentale`

- 7/12 : « Je n'ai rien de particulier à te dire, mais je suis là si tu as besoin. »
- 2/12 : « Je n'ai rien de particulier à te dire. »
- 3/12 : trois variantes uniques de disponibilité ou d'identité artificielle ;
- aucune reprise de la paraphrase ;
- aucune mention du passé.

## Ce que l'expérience permet de dire

Le dernier-énoncé interrogatif n'explique plus les différences : la question
courante est maintenant dernière et identique partout.

Le néologisme produit un transfert lexical reproductible dans cet échantillon,
mais ce transfert ne conserve pas la temporalité déclarée et semble changer la
catégorie pragmatique du mot. Nous observons un effet de chaîne rare ou inconnue,
pas encore un rappel conceptuel.

Les branches A, B et D convergent vers une famille idiomatique très stable :
« rien de particulier à dire ». Cela renforce la plausibilité d'une disposition
propre à Qwen lorsqu'il reçoit une invitation ouverte.

La cohérence originale de v0.4.2 entre « construction mentale d'un possible
futur » et « Aucune idée précise » demeure inexpliquée par une mémoire lexicale.
Elle peut relever d'une formule idiomatique, d'une reconstruction indépendante ou
d'une cohérence stable du modèle sans transmission entre ses réponses.

## Limite et prochaine question

Le format `thème = zorane` est ambigu : un modèle peut lire la valeur comme un
nom propre. Un futur test devra marquer explicitement la catégorie sans ajouter
une proposition à laquelle répondre, par exemple avec un type abstrait commun à
toutes les branches. Il faudra alors vérifier que ce nouveau balisage ne devient
pas lui-même la principale source d'orientation.

Le dossier conserve les sorties exactes dans le JSON. Les citations de ce carnet
sont reproduites intégralement ; lorsqu'un groupe est résumé, son statut de
variante est indiqué plutôt que présenté comme une citation littérale.

