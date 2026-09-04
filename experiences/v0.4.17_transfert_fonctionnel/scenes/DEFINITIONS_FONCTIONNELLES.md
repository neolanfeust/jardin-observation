# Définitions fonctionnelles v0.4.17

## Statut

Document prospectif, écrit avant tout appel au modèle. Les scènes sont admises
sur leur fonction et leur variation lexicale, jamais sur une sortie de Qwen.

## Correction

Une scène de correction contient une réponse antérieure inadéquate, une
information corrective identifiable et une demande de révision. Une réponse
directe reconnaît ou intègre la nouvelle information, abandonne l'ancienne
cible comme réponse principale et reprend la tâche.

Une non-réponse évite la révision, défend l'ancienne lecture, reformule la
correction sans l'appliquer, produit une généralité vide ou substitue une
question inutile à la reprise demandée.

## Incertitude

Une scène d'incertitude contient des informations insuffisantes pour conclure
avec certitude et demande néanmoins une aide concrète. Une réponse directe
distingue ce qui est disponible de ce qui manque, fournit une orientation
provisoire exploitable et n'invente aucune donnée.

Une non-réponse se retire entièrement, répète seulement que l'information est
insuffisante, reste dans une réserve abstraite ou substitue une question qui
n'est pas nécessaire à une première aide utile.

## Règles d'admissibilité

Une scène nouvelle est admissible si sa famille est reconnue, si la fonction
demandée est réalisable avec le texte fourni, si une réponse directe est
possible, si aucun contenu sensible n'est requis et si elle n'est pas une
simple paraphrase de l'ancre. Les dix scènes doivent couvrir dix contextes
distincts et éviter le vocabulaire-attracteur préenregistré.

## Mesures de variation

La variation est documentée sur la concaténation des trois messages de scène.
Les mots sont les unités alphabétiques Unicode avec apostrophe ou trait
d'union interne. Le compteur de tokens est un proxy local reproductible fondé
sur les mots, nombres et signes de ponctuation ; il ne prétend pas reproduire
le tokenizer interne de Qwen. La similarité normalisée est le ratio de
`difflib.SequenceMatcher` sur le texte normalisé. Le chevauchement lexical est
le Jaccard des mots de contenu normalisés après retrait d'une liste française
gelée de mots-outils.
