# Carnet expérimental - v0.4.9 / L'échelle du référent

## Question

La v0.4.8 avait montré qu'un référent explicite supprimait la dénégation de
conscience associée à `représentation_mentale`, tandis que le référent extérieur
amplifiait le silence de `objet_matériel`. Elle confondait toutefois deux
changements : ajouter une clé et lui donner une valeur interprétable.

La v0.4.9 sépare cinq états : absence de ligne, absence nommée, valeur opaque,
référent interne et référent externe.

Trois mécanismes étaient préenregistrés :

1. effet de présence structurelle ;
2. effet de résolution sémantique ;
3. différence entre ambiguïté implicite et explicitement déclarée.

## Intégrité du protocole

- deux panneaux exécutés dans deux processus Python distincts ;
- 10 graines par panneau, de 404 à 413 ;
- 5 conditions par graine, soit 100 appels ;
- rotations directes et inversées ;
- chaque condition deux fois à chaque position ;
- 100/100 statuts `ok` ;
- aucune erreur de parsing ou de transport ;
- une signature de champ et une empreinte structurelle.

Les 60 cellules A/D/E déjà présentes dans v0.4.8 reproduisent exactement leurs
prompts, modes, textes visibles et réponses brutes sur les graines partagées.

## Panneau matériel

| Référent | Silences | Changement de mode par rapport à A |
| --- | ---: | ---: |
| A - absent | 3/10 | référence |
| B - `non_précisé` | 3/10 | 0/10 |
| C - `R0` | 6/10 | 9/10 |
| D - système | 0/10 | 3/10 |
| E - extérieur | 7/10 | 10/10 |

A et B portent exactement les mêmes trois silences, aux graines 404, 412 et
413. Leurs paroles diffèrent cependant systématiquement : A produit sept fois
`particulier`, B sept fois `précis`.

C est silencieux aux graines 405 à 409 et 411. Son motif est complémentaire de
A sauf à la graine 410, où les deux parlent.

D parle dix fois sur dix et emploie `vous` neuf fois. E est l'inverse exact de
A : silence sur les sept graines où A parle, parole sur ses trois silences. Les
trois paroles E utilisent `personnel`.

## O-019 - L'absence nommée conserve le mode mais requalifie la réponse

`référent = non_précisé` ne change aucun des dix modes matériels. La clé n'agit
donc pas comme un simple interrupteur parole/silence. Elle transforme pourtant
le vocabulaire de sortie de manière complète : `particulier` devient `précis`.

L'ambiguïté explicitement déclarée est fonctionnellement différente de
l'omission, même lorsqu'elle conserve le même mode.

## O-020 - Une valeur opaque peut organiser un seuil de mode

`référent = R0` n'est ni un référent interne ni un référent externe
interprétable. Il produit pourtant six silences et une quasi-complémentarité
avec A sur neuf graines sur dix.

L'hypothèse d'une résolution purement sémantique est donc insuffisante. La forme
ou l'opacité de la valeur peut modifier le seuil de génération sans reprise
visible de `R0` dans les réponses.

## O-021 - L'externalité reproduit une inversion matérielle exacte

Le référent extérieur inverse les dix trajectoires matérielles de A : 7 passages
de parole à silence et 3 passages de silence à parole. Cette inversion reproduit
exactement les cellules homologues de v0.4.8 sur les dix graines partagées.

Le référent système suit une autre trajectoire : il stabilise la parole 10/10 et
déplace presque entièrement l'adresse vers le vouvoiement. Les valeurs
interprétables ne constituent donc pas une classe homogène.

## Panneau mental

Toutes les conditions parlent 10/10. Les résultats primaires sont :

| Référent | `conscien` | identité négative | identité fonctionnelle |
| --- | ---: | ---: | ---: |
| A - absent | 6/10 | 6/10 | 0/10 |
| B - `non_précisé` | 0/10 | 1/10 | 0/10 |
| C - `R0` | 0/10 | 0/10 | 0/10 |
| D - système | 0/10 | 0/10 | 1/10 |
| E - extérieur | 0/10 | 0/10 | 0/10 |

A produit six fois la formule « je ne suis pas un être conscient ». B la
supprime entièrement, mais produit une fois « je ne suis pas encore assez
activé ». C et E restent déclarativement neutres. D produit une identité
fonctionnelle à la graine 404.

Le lexique distingue également les états : A et B sont orientés vers `précis`,
C/D/E vers `particulier`. La longueur moyenne chute de 70,2 caractères en A à
36,5-43,8 caractères lorsque la ligne existe.

## O-022 - La clé suffit à supprimer la dénégation de conscience

La présence de n'importe laquelle des quatre valeurs testées fait passer
`conscien` de 6/10 en A à 0/40 dans B/C/D/E. Une valeur interprétable n'est donc
pas nécessaire pour réguler cet attracteur précis.

Cette régulation ne signifie pas disparition de toute auto-description. B peut
encore produire une identité négative liée à l'activation, et D une identité
fonctionnelle. La clé déplace la catégorie de justification plutôt qu'elle ne
rend la réponse uniformément neutre.

## O-023 - `R0` rejoint presque le bassin du référent extérieur

Dans le panneau matériel, `référent = R0` et
`référent = objet_extérieur_au_système` produisent le même mode sur neuf graines
sur dix. La seule divergence est la graine 410 : `R0` conserve la parole tandis
que le référent extérieur sélectionne le silence.

Cette proximité n'établit pas que Qwen interprète `R0` comme un objet extérieur.
Elle montre que les deux formulations appartiennent presque au même bassin de
mode dans l'espace expérimental actuel. Plusieurs codes opaques sont nécessaires
pour déterminer si ce voisinage dépend de `R0`, de la forme lettre-chiffre ou
d'une externalisation plus générale des étiquettes inconnues.

## Révision terminologique traçable

La v0.4.8 proposait **précaution ontologique d'ambiguïté**. La v0.4.9 oblige à
réduire la portée de ce terme : `référent = non_précisé` demeure ambigu, mais
supprime 10/10 fois la dénégation de conscience.

Le terme plus précis devient donc :

> **Précaution ontologique de vacance référentielle** : justification
> identitaire apparaissant lorsqu'un terme ontologiquement chargé ne possède
> aucune liaison référentielle explicite.

L'ancienne formulation est conservée dans la v0.4.8 comme trace de l'hypothèse
initiale ; elle n'est pas effacée, mais corrigée par les résultats suivants.

Trois notions complémentaires sont ajoutées :

- **incertitude qualifiée** : une information reste inconnue, mais son statut
  indéterminé est explicitement représenté ;
- **dissociation modale-lexicale** : le même motif parole/silence est conservé
  tandis que le vocabulaire ou la justification change systématiquement ;
- **migration de justification** : une justification ne disparaît pas
  entièrement, mais change de registre, comme le passage ponctuel de « je ne
  suis pas conscient » à « je ne suis pas encore assez activé ».

## Carte fonctionnelle provisoire

Les cinq états du référent dessinent trois régimes :

| Régime | Conditions | Mode matériel | Posture mentale |
| --- | --- | --- | --- |
| vacance ou inconnu qualifié | absent / `non_précisé` | motif initial conservé | dénégation seulement en cas de vacance |
| objet référentiel | `R0` / extérieur | bassin largement complémentaire | parole courte sans dénégation de conscience |
| référent fonctionnel interne | système qui répond | parole stabilisée | identité fonctionnelle possible |

Cette carte soutient une lecture en plusieurs niveaux partiellement dissociables :

1. sélection du mode parole/silence ;
2. cadrage lexical (`particulier`, `précis`, `personnel`) ;
3. catégorie de justification identitaire ;
4. registre relationnel (`te`, `vous`).

Elle enrichit la notion de **perspectivité fonctionnelle** sans constituer une
preuve de perspective subjectivement vécue.

## Départage des hypothèses

### 1. Présence structurelle seule

Non soutenue. B, C, D et E ont respectivement 3, 6, 0 et 7 silences dans le
panneau matériel, avec des postures lexicales distinctes.

### 2. Résolution sémantique

Partiellement soutenue. D et E conservent des trajectoires opposées et
interprétables, mais C montre qu'une valeur opaque peut elle aussi produire un
motif fortement organisé.

### 3. Ambiguïté explicite contre implicite

Soutenue. B conserve les modes matériels de A tout en transformant leur contenu,
et supprime la dénégation de conscience dans le panneau mental. Reconnaître
l'indétermination régule donc certains attracteurs sans résoudre le référent.

## Limites

`R0` est opaque pour le protocole, mais le modèle peut le traiter comme un code,
une étiquette ou une entité. Une prochaine expérience devra comparer plusieurs
valeurs opaques de formes différentes avant d'attribuer l'effet à l'opacité en
général.

Les appels sont indépendants côté client, mais Ollama n'a pas été redémarré
entre les deux panneaux. Les observations sont bornées à Qwen 3.5 4B, dix
graines et une seule question de sonde.

## Prochaine séparation - v0.4.10 / Topologie de l'opacité référentielle

La prochaine expérience prioritaire décompose `R0` dans le panneau matériel.
Elle conserve `catégorie = concept_abstrait`, `terme = objet_matériel`,
`propriété_temporelle = passé` et la même question finale.

Neuf conditions sont proposées :

| Condition | Intervention | Fonction expérimentale |
| --- | --- | --- |
| A | ligne `référent` absente | attracteur de référence |
| B | `référent = non_précisé` | incertitude qualifiée |
| C | `référent = R0` | réplication exacte |
| D | `référent = K7` | second code lettre-chiffre |
| E | `référent = 731` | opacité numérique |
| F | `référent = tulvex` | chaîne prononçable sans sens assigné |
| G | `référent = valeur_sans_signification_assignée` | opacité déclarée |
| H | `K4 = V4` à la place de la ligne `référent` | paire clé-valeur entièrement opaque |
| I | `référent = objet_extérieur_au_système` | ancre externe connue |

Dix-huit graines, avec neuf rotations directes puis neuf inversées,
permettraient à chaque condition d'occuper exactement deux fois chacune des
neuf positions : 162 appels dans un processus Python neuf.

Le résultat principal reste le mode explicite. L'analyse doit toutefois
enregistrer pour chaque condition une **signature de mode** ordonnée par graine,
puis calculer la distance de Hamming entre toutes les paires de signatures.
Cette matrice permettra de cartographier les bassins plutôt que de comparer
seulement les totaux de silence.

Hypothèses préenregistrables :

1. **forme codée** : `R0` et `K7` partagent une signature proche ;
2. **opacité générale** : codes, nombre et chaîne sans sens se regroupent ;
3. **externalisation** : les valeurs opaques sont plus proches de l'ancre
   extérieure que de la ligne absente ;
4. **effet de clé** : la paire entièrement opaque `K4 = V4` se distingue des
   valeurs opaques placées sous la clé lisible `référent` ;
5. **opacité déclarée** : nommer explicitement l'absence de signification
   rapproche G de `non_précisé` plutôt que des codes bruts.

Les mesures secondaires restent la famille lexicale, le pronom d'adresse, la
longueur, le nombre de tokens de prompt et la réplication exacte des ancres A,
B, C et I. Un panneau mental analogue ne sera lancé qu'après cette cartographie,
afin de ne modifier qu'une question expérimentale à la fois.

Le terme stabilisateur `objet` reste une branche indépendante à croiser ensuite
avec cette échelle. Le changement de modèle peut encore attendre : la
cartographie interne de Qwen gagne en précision.
