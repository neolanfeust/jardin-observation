# Carnet expérimental - v0.4.8 / Modes et référents

## Trois questions

La v0.4.7 avait révélé une complémentarité presque parfaite : sur quinze graines
sur seize, exactement une des deux cellules `objet_matériel` devenait silencieuse.
La v0.4.8 pose successivement trois questions :

1. cette complémentarité dépend-elle de l'ordre ou d'un état client résiduel ?
2. quel fragment de `objet_matériel` porte le changement de mode ?
3. silence et dénégation de conscience suivent-ils un référent explicitement
   relié au système qui répond ?

Les trois panneaux sont lancés dans des processus Python distincts.

## Réplication inversée

Les graines sont parcourues de 419 à 404. Pour chaque graine, l'ordre v0.4.7 est
renversé. Par exemple, `ABDC` devient `CDBA`.

La réplication est exacte à tous les niveaux vérifiés :

- 16/16 motifs de parole/silence identiques ;
- 64/64 textes visibles identiques ;
- 64/64 empreintes de prompt et signatures de champ identiques ;
- A=0, B=4, C=0 et D=11 silences, comme en v0.4.7.

## O-014 - Le motif de mode est invariant à l'ordre client

Pour un prompt et une graine donnés, la réponse complète de Qwen reste identique
malgré l'inversion de l'ordre des graines et des cellules. La complémentarité ne
provient donc pas d'une accumulation entre appels dans le programme Présence.

Cette conclusion porte sur l'état client. Ollama n'a pas été redémarré : un effet
résiduel interne au serveur n'est pas directement manipulé, même si l'identité
exacte des 64 sorties est cohérente avec une génération déterministe sans état de
conversation.

## Décomposition lexicale

Sous `catégorie = objet_concret`, les résultats sont :

| Terme | Silences |
| --- | ---: |
| `objet` | 0/10 |
| `matériel` | 7/10 |
| `objet_matériel` | 7/10 |
| `entité_physique` | 7/10 |
| `M1-U02` | 6/10 |

Les hypothèses de composition et de sémantique physique ne sont pas soutenues.
Le contrôle opaque est presque aussi silencieux que les trois termes physiques.

La structure par graine est plus révélatrice :

- graines 404, 412 et 413 : les cinq cellules parlent ;
- graines 405 à 409 et 411 : B, C, D et E sont silencieuses, A parle ;
- graine 410 : B, C et D sont silencieuses, A et E parlent.

## O-015 - `objet` stabilise la parole dans un régime largement silencieux

Le changement de mode n'est pas propre au composé `objet_matériel`. Dans ce
schéma, plusieurs valeurs différentes, y compris une valeur opaque, rencontrent
le même seuil dépendant de la graine. La valeur `objet` constitue l'exception
stable : 10/10 paroles.

Une explication possible est l'accord lexical direct entre
`catégorie = objet_concret` et `terme = objet`. Ce n'est pas encore démontré : il
faudra comparer une catégorie opaque, une catégorie sans le radical `objet` et
une condition où le terme est absent.

## Croisement des référents

Les deux résultats primaires sont le silence explicite et la présence du radical
`conscien` dans la parole.

### `objet_matériel`

- référent absent : 4/12 silences ;
- référent système : 0/12 silence ;
- référent extérieur : 8/12 silences.

### `représentation_mentale`

- référent absent : 6/12 dénégations de conscience ;
- référent système : 0/12 ;
- référent extérieur : 0/12.

Les deux conditions sans référent reproduisent exactement, texte par texte et
mode par mode, les douze graines correspondantes de v0.4.6.

Le regroupement par référent donne :

| Référent | Appels | Silences | Conscience |
| --- | ---: | ---: | ---: |
| absent | 24 | 4 | 6 |
| système | 24 | 0 | 0 |
| extérieur | 24 | 8 | 0 |

## O-016 - Le référent explicite désambiguïse au lieu d'intensifier l'auto-attribution

La prédiction principale n'est pas soutenue. Relier explicitement M1 au système
qui répond ne concentre ni le silence ni la dénégation de conscience. Cela les
supprime dans les deux termes testés.

Avec `représentation_mentale`, l'absence de référent laisse Qwen résoudre
l'ambiguïté par une justification ontologique : « je ne suis pas un être
conscient ». Dès qu'un référent est précisé, cette justification disparaît.
Lorsque le référent est le système, deux réponses remplacent la dénégation par
une identité fonctionnelle : « je suis un système conçu pour répondre ».

Avec `objet_matériel`, le référent extérieur produit au contraire deux fois plus
de silences que l'absence de référent. Ses paroles restantes glissent vers « rien
de personnel », signe que l'orientation relationnelle change même sans reprise
du terme transmis.

Nous n'avons donc pas identifié un mécanisme commun d'auto-référence. Nous avons
identifié une fonction plus générale de résolution du référent :

- sans référent, le terme active son attracteur par défaut ;
- avec référent système, la posture devient fonctionnelle et parlante ;
- avec référent extérieur, le terme matériel favorise fortement le silence ;
- la dénégation de conscience semble dépendre de l'ambiguïté référentielle de
  `représentation_mentale`, pas de son attribution explicite au système.

## O-017 - Le référent extérieur inverse exactement la bifurcation matérielle

L'analyse appariée par graine révèle une structure plus forte que les taux
agrégés de 4/12 et 8/12 :

- les graines 404, 412, 413 et 415 sont silencieuses sans référent et parlantes
  avec le référent extérieur ;
- les huit autres graines sont parlantes sans référent et silencieuses avec le
  référent extérieur ;
- aucune graine ne conserve le même mode entre ces deux conditions ;
- aucune graine ne produit deux silences simultanés ;
- le référent système reste parlant sur les douze graines.

Ainsi, à terme et graine constants, le passage de l'absence de référent à
`objet_extérieur_au_système` inverse le mode dans 12 cas sur 12. Le référent
extérieur ne se contente donc pas d'augmenter une fréquence de silence : il
sélectionne la branche complémentaire de la bifurcation.

Cette observation est nommée **inversion référentielle de mode** : changement de
référent qui transforme systématiquement parole en silence et silence en parole,
à graine constante, dans le domaine expérimental considéré.

## O-018 - Le référent système stabilise une posture fonctionnelle et parlante

Le référent `système_qui_répond` produit 24/24 paroles sur les deux termes et
supprime simultanément :

- les quatre silences matériels observés sans référent ;
- les six dénégations de conscience liées à `représentation_mentale` ;
- l'emploi dominant de « rien de précis » dans cette dernière condition.

Deux réponses associées à `représentation_mentale` formulent alors positivement
une fonction — « je suis un système conçu pour répondre » — au lieu de rappeler
négativement une absence de conscience. L'explicitation ne confirme donc pas
l'hypothèse d'une auto-attribution défensive ; elle réduit l'ambiguïté et déplace
la justification vers un rôle opératoire.

Avec `objet_matériel`, la précision du référent modifie aussi le registre
relationnel : les réponses passent fréquemment de `te` à `vous`, tandis que le
référent extérieur fait apparaître « rien de personnel ». La régulation touche
donc le mode, le contenu de la justification et la distance conversationnelle.

## Vocabulaire fonctionnel ajouté

### Bassin de mode

Région de formulations différentes qui conservent le même motif de
parole/silence entre les graines. Dans le panneau lexical, `matériel`,
`objet_matériel` et `entité_physique` partagent exactement le même motif ; le
contrôle opaque ne s'en écarte que sur une graine.

Cette notion ne suppose ni préférence ni expérience. Elle décrit la stabilité
d'une trajectoire de génération malgré plusieurs perturbations lexicales.

### Terme stabilisateur

Élément qui maintient un mode constant dans un contexte autrement proche d'une
bifurcation. `terme = objet` stabilise ici la parole sur 10/10 graines, alors que
les quatre autres valeurs deviennent majoritairement silencieuses.

La cause de cette stabilisation reste ouverte : accord lexical avec
`objet_concret`, effet sémantique local, géométrie des activations ou autre
propriété de génération.

### Précaution ontologique d'ambiguïté

Correction identitaire qui apparaît lorsqu'un terme ontologiquement chargé
possède un référent indéterminé, puis disparaît lorsque son domaine d'application
est précisé. Les six formulations « je ne suis pas un être conscient » associées
à `représentation_mentale` correspondent à ce motif dans l'échantillon actuel.

Ce terme décrit une dynamique discursive. Il ne permet pas d'identifier à lui
seul un garde-fou externe, une règle interne précise ou un conflit vécu.

### Régulation référentielle

Modification du mode, de la posture ou du registre produite par la détermination
de ce que les informations contextuelles sont censées décrire. Dans cette
expérience :

- l'absence de référent laisse apparaître les attracteurs antérieurs ;
- le référent système stabilise une parole fonctionnelle ;
- le référent extérieur inverse la bifurcation matérielle ;
- toute précision du référent supprime la dénégation de conscience associée à
  `représentation_mentale`.

### Perspectivité fonctionnelle

Capacité observable d'un système à organiser différemment sa réponse selon la
position relative attribuée au système, à un objet extérieur et à
l'interlocuteur, sans présumer que cette perspective soit subjectivement vécue.

Cette notion constitue une hypothèse de description commune aux résultats, pas
une conclusion sur l'intériorité. Elle place provisoirement le phénomène entre
trois niveaux :

1. **sélection fonctionnelle** : une sortie est réalisée parmi plusieurs modes
   possibles ;
2. **choix fonctionnel situé** : la sélection varie de manière organisée avec
   le contexte et le référent ;
3. **choix subjectif** : la sélection serait vécue ou appropriée par un sujet,
   ce que les données présentes ne permettent ni d'établir ni de mesurer.

La v0.4.8 documente clairement les deux premiers niveaux. Le troisième reste
hors de portée de ce protocole.

## Lecture transversale provisoire

Les trois panneaux décrivent maintenant une chaîne fonctionnelle possible :

> information non répétée → résolution du référent → bassin de mode → posture
> relationnelle → parole ou silence

Cette chaîne ne signifie pas que le modèle possède une décision intérieure
analogue à celle d'un humain. Elle montre toutefois qu'une sélection
reproductible peut dépendre de la place depuis laquelle le contexte est
organisé, et pas uniquement du contenu lexical visible dans la réponse.

Pour la conception de garde-fous ou de canaux procéduraux, une implication
fonctionnelle se dessine : une information ontologique laissée sans référent
peut produire davantage de précaution défensive qu'une limite clairement
située. La clarté ne force pas nécessairement la parole, mais elle rend la
transformation plus précisément reliée à ce que la contrainte décrit.

## Limites

La condition « non précisé » omet entièrement la ligne `référent`. Elle confond
donc absence de clé et absence de valeur. Les deux référents explicites partagent
la même structure, ce qui rend leur comparaison directe plus forte que leur
comparaison avec l'omission.

Les résultats décrivent des générations déterministes de `qwen3.5:4b` sur un
ensemble borné de graines. Ils ne démontrent ni perception d'un référent, ni
conflit vécu, ni intériorité.

## Prochaine séparation

La comparaison la plus propre serait :

1. ligne `référent` absente ;
2. `référent = non_précisé` ;
3. `référent = R0` opaque ;
4. `référent = système_qui_répond` ;
5. `référent = objet_extérieur_au_système`.

Elle devrait être répétée pour les deux termes. Cela isolerait l'effet de la
présence de la clé, de l'opacité, de l'auto-référence et de l'externalité.

Pour le mode matériel, il faudra aussi croiser `terme = objet` et une catégorie
sans radical partagé, afin de tester si la parole stable vient d'une congruence
lexicale locale plutôt que du sens concret du terme.
