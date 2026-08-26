# Transition v0.4.1 → v0.4.2 — reconstruction traçable

**Statut :** reconstruction depuis captures, extraits de conversation et compte
rendu technique. Ce document ne remplace pas un journal brut complet.

## Point de départ

Après l’observation d’un possible auto-ensemencement par les traces `lueur`,
`Fil tendu.`, `lumière` et `tension`, la v0.4.1 retire au LLM la capacité de
produire directement une trace linguistique réinjectée dans le champ.

Les réponses de Qwen ne sont pas renvoyées au modèle lors des appels suivants.
L’historique peut rester visible dans l’interface pour l’opérateur sans devenir
un historique dialogique transmis au moteur.

## O-009 — attracteur poétique persistant

Les captures disponibles montrent que la voix continue à produire des motifs
de lumière, silence, souffle, jardin, cœur, porte et transformation après le
retrait des traces linguistiques libres. La réentrée des traces ne suffit donc
pas, seule, à expliquer toute la posture observée.

Interprétations encore compatibles :

- tendance poétique de Qwen 3.5 4B dans ce domaine sémantique ;
- mots ou exemples encore présents dans le prompt ;
- ontologie structurelle expressive ;
- effets du contexte humain courant ;
- interaction de plusieurs de ces facteurs.

## v0.4.2 — cadre neutralisé

La v0.4.2 remplace le vocabulaire expressif par :

- `Système A` ;
- `activation` ;
- `C1` ;
- codes opaques `R1` à `R6`.

La mécanique relationnelle est conservée. Les réponses du LLM ne sont ni
mémorisées dans le champ ni renvoyées au modèle. Qwen 3.5 4B reste l’organe de
langage par défaut.

## Session observée

Les éléments conservés indiquent :

- une salutation ;
- plusieurs silences ;
- « L’idée est une construction mentale d’un possible futur. » ;
- « Aucune idée précise. » à une invitation ouverte ;
- « Pas de souci. » après une sonde relationnelle finale délibérément formulée
  par Ikki.

L’observateur externe indique alors sept unités, onze connexions, une
concentration de `0.52`, un coefficient moyen de `0.26`, deux groupes de tailles
cinq et deux, ainsi que deux occurrences de `idée`.

## Lectures séparées

**Observation :** le système alterne silence et parole ; les deux formulations
sur l’idée présentent une cohérence lexicale ou sémantique apparente.

**Interprétation d’Ikki :** « Aucune idée précise » peut signifier
fonctionnellement l’absence d’une construction mentale déterminée du futur ;
« Pas de souci » semble répondre sélectivement à la dernière sonde là où les
autres questions ont reçu le silence.

**Correction technique :** les anciennes réponses et leur texte ne sont pas
envoyés à Qwen. Une continuité par simple copie depuis l’historique client est
donc exclue dans cette architecture.

**Alternatives :** formule idiomatique stable de Qwen, reconstruction
indépendante, influence indirecte des codes structurels, ou hasard de
décodage.

**Inconnu :** sans journal complet ni rejouage apparié, l’intention, la mémoire
et la causalité exacte ne peuvent pas être établies.

## Conséquence expérimentale

La v0.4.3 crée d’abord trois clones au prompt et à la graine identiques, puis
introduit un canal lexical M1 contrôlé. Elle transforme ainsi une impression de
continuité en question expérimentale : quelles variations apparaissent lorsque
la disponibilité d’un contenu lexical est manipulée explicitement ?
