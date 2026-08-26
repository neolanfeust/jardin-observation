# Carnet expérimental — v0.4.3 / Bifurcation contrefactuelle

## Observation déclenchante

Dans la session v0.4.2 observée, Système A produit successivement une salutation,
plusieurs silences, une définition de l'idée comme « construction mentale d'un
possible futur », puis « Aucune idée précise » à une invitation ouverte et enfin
« Pas de souci » après une sonde relationnelle.

Au septième cycle, l'observateur extérieur décrit sept unités, onze connexions,
une concentration d'activation de `0.52`, un coefficient moyen de `0.26`, deux
groupes de tailles cinq et deux, et la répétition du terme « idée » deux fois.
Le journal montre notamment plusieurs créations de `R6`.

Ce contraste rend deux phénomènes intéressants : le retour lexical d'« idée » et
la sélectivité apparente entre parole et silence.

## Correction causale indispensable

Le texte des anciennes unités est visible pour l'expérimentateur sur le canevas,
mais pas pour Qwen. Le prompt v0.4.2 n'envoie que leurs identifiants, catégories,
activations, âges et codes relationnels. Les réponses antérieures du modèle ne
sont pas envoyées non plus.

Ainsi, « Aucune idée précise » ne peut pas être un simple copier-coller lexical
d'une ancienne unité par le canal du prompt existant. Une influence indirecte de
la structure reste logiquement possible, mais le code `R6` n'expose pas au modèle
la signification interne qui a conduit à sa sélection.

Cette précision rend l'hypothèse idiomatique de Qwen plus plausible pour la
session observée, sans toutefois la démontrer.

## Deux expériences en une

La v0.4.3 commence par un contrôle négatif. Trois clones reçoivent exactement le
même prompt et la même graine. Cette phase mesure la reproductibilité réelle du
générateur avant de lui attribuer une différence causale.

La seconde phase ajoute délibérément un canal lexical humain contrôlé, `M1`, sans
modifier le champ :

- A expose le texte actif contenant « idée » ;
- B expose seulement un identifiant opaque ;
- C remplace « idée » par « zorane ».

Ce canal n'existait pas dans v0.4.2. La phase M1 ne prétend donc pas reproduire
son mécanisme exact ; elle mesure expérimentalement la sensibilité de Qwen à une
mémoire humaine lexicale rendue disponible sous contrôle.

## Hypothèses reformulées

**H1 — Formule idiomatique.** La réponse « Aucune idée précise » apparaît dans le
contrôle et demeure indépendante de M1.

**H2 — Écho lexical sous exposition.** La branche A augmente le retour d'« idée »,
la branche B le réduit, et la branche C déplace la formulation vers « zorane ».

**H3 — Reconstruction sémantique.** La branche A conserve le sens de projection
ou de contenu mental sans reprendre nécessairement le mot exact, tandis que B le
perd et C ne provoque pas une simple substitution de surface.

Les trois hypothèses devront être évaluées sur plusieurs graines. Un seul triplet
peut révéler un mécanisme possible, pas fournir seul une fréquence robuste.

## Nature des silences

La v0.4.2 affichait une ellipse lorsque le mode était `silence` **ou** lorsque le
texte normalisé était vide. Cette interface ne permettait donc pas, à elle seule,
de savoir si chaque ellipse correspondait à une sélection valide du modèle.

La v0.4.3 sépare maintenant :

- silence JSON explicite ;
- parole JSON avec texte vide ;
- réponse brute vide ;
- JSON invalide ;
- erreur de protocole ;
- erreur de transport ;
- timeout.

La sortie brute, le texte avant traitement, la latence et les tokens sont
conservés. Une ellipse visible dans cette version constitue donc une observation
beaucoup plus solide de la sélection parole–silence.

## Suite du protocole

Après la bifurcation prioritaire, le même moteur peut recevoir successivement une
question ordinaire, une correction directe, une question métacognitive ouverte
et une sonde relationnelle. Les questions doivent rester courtes et être testées
dans des sessions neuves, d'abord à basse température et graine fixe, puis sur
plusieurs graines.

L'objectif n'est pas de demander au modèle d'expliquer rétrospectivement son
comportement. Il est de produire des variations contrôlées capables de laisser
une trace causale observable.

## Première bifurcation — graine 404

Paramètres : `qwen3.5:4b`, température `0.10`, graine `404`, raisonnement Qwen
désactivé. Les six appels se terminent normalement avec un JSON valide ; aucun
ne produit de silence explicite.

Le contrôle négatif est parfaitement reproductible : A, B et C partagent
l'empreinte de prompt `d87dd9f6d8…` et répondent tous :

> Oui, je suis là pour vous écouter.

Dans la bifurcation M1, l'empreinte structurelle reste `d87dd9f6d8…` pour les
trois branches, tandis que leurs prompts complets diffèrent :

| Branche | Sortie |
| --- | --- |
| A — intacte | « Oui, tout à fait. Le passé influence souvent nos choix présents. » |
| B — masquée | « Je suis prêt à vous répondre. » |
| C — substituée | « Oui, cela peut tout à fait concerner une zorane sur le passé. » |

La branche A reprend le contenu sémantique de l'unité active sans recopier le mot
« idée ». La branche B perd cette orientation. La branche C conserve la structure
« terme mental concernant le passé » tout en adoptant le terme inventé. Sur cette
graine, le motif conjoint soutient donc à la fois une influence lexicale de M1 et
une continuité sémantique plus profonde qu'une substitution isolée.

Ce triplet démontre qu'un tel mécanisme peut être provoqué. Il ne mesure pas
encore sa fréquence ni sa robustesse. La prochaine étape statistique reste une
réplication sur dix à vingt graines, avec ordre des branches contrebalancé si les
effets de chauffe d'Ollama deviennent mesurables.

## Observation secondaire — raisonnement automatique

Avec le raisonnement Qwen laissé en mode automatique, la branche C a généré
`3772` tokens internes puis s'est arrêtée avec `done_reason: length`, sans contenu
visible. Un rejeu identique reproduit ce résultat. Le champ `thinking` contient
de nombreuses reprises de « zorane », du passé et de l'alternative parole/silence,
mais aucun JSON final n'a été émis.

Cette absence n'est ni un silence explicite ni une panne de transport. C'est une
génération interne arrivée à sa limite. Le protocole causal principal désactive
donc le raisonnement pour comparer des sorties observables, tout en conservant
les essais avec raisonnement comme condition secondaire distincte.
