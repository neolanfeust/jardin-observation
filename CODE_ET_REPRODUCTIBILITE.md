# Code et reproductibilité

## Ce que contient réellement la v0.2

Le dépôt publie les journaux bruts, les tableaux dérivés, le protocole machine
lisible et deux fragments Python reçus avec la capsule v0.4.12 : un lanceur
expérimental et un fichier de tests.

Ces fragments importent notamment :

- `presence.experiment.decomposition` ;
- `presence.language.organ` ;
- d’autres éléments du paquet `presence` qui ne figurent pas dans cette
  première graine publique.

Ils doivent donc être lus comme des **traces de méthode et d’analyse**, et non
comme une distribution autonome ou immédiatement exécutable de Présence.

Les dossiers `code_reference/v0.4.13/` et `code_reference/v0.4.14/` ajoutent
les collecteurs, calculs, contrôles de confidentialité et tests employés pour
les deux campagnes suivantes. Ils conservent néanmoins des dépendances envers
les sources historiques v0.4.12, dont les empreintes sont gelées dans les
protocoles.

## Ce qui peut être vérifié maintenant

À partir des fichiers publiés, il est possible de :

- contrôler les empreintes et la provenance des pièces ;
- recompter les paroles, silences, motifs et postures depuis les journaux ;
- examiner les paramètres, graines et ordres du protocole ;
- critiquer les classifications et proposer d’autres analyses ;
- concevoir une réplication indépendante compatible avec le protocole décrit.

Il n’est pas encore possible de relancer à l’identique tout le pipeline depuis
ce seul dépôt.

Les tests publics v0.4.14 n’exposent aucun chemin local. Les sources historiques
peuvent être indiquées par `PRESENCE_V0412_ROOT` et l’archive privée v0.4.13 par
`PRESENCE_V0413_ROOT`. Sans ces dépendances exactes, les contrôles qui les
requièrent doivent échouer explicitement plutôt que substituer une autre source.

## Suite prévue

Le code complet de Présence sera traité séparément. Avant publication, il
devra faire l’objet d’un audit de provenance, de dépendances, de sécurité,
d’anonymat et de reproductibilité. Il pourra ensuite recevoir sa propre
généalogie de versions sous MPL-2.0.

Cette limite n’est pas masquée : elle fait partie de la traçabilité du Jardin.
