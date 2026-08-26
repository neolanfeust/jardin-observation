# Index des sources et de leur portée

Cet index indique où retrouver les matériaux utilisés par le Carnet maître. La
présence d’un fichier dans l’archive ne transforme pas son interprétation en
preuve : elle permet seulement de remonter à la trace disponible.

## Généalogie relationnelle

| Période | Source | Portée |
| --- | --- | --- |
| O-001 à O-008 | `archives/carnets_versions/CARNET_DU_PONT_ANONYMISE.md` | transcription anonymisée ; original non publié car identifiant |
| O-009 | captures et compte rendu de Présence | reconstruction signalée ; journal complet manquant |
| charte de Présence | `archives/carnets_versions/CARNET_DE_PRESENCE.md` | intention architecturale, pas résultat expérimental |
| structure seule | `archives/carnets_versions/CARNET_V0_4.md` | hypothèse et périmètre de la v0.4 |

## Série expérimentale

| Version | Carnet | Données disponibles | Observations |
| --- | --- | --- | --- |
| v0.4.1–v0.4.2 | `CARNET_TRANSITION_V0_4_1_V0_4_2_RECONSTRUIT.md` | journal complet non archivé ici | O-009 et transition vers les codes opaques |
| v0.4.3 | `CARNET_V0_4_3.md` | `v0.4.3_bifurcation.json` | contrôle causal et première bifurcation M1 |
| v0.4.4 | `CARNET_V0_4_4.md` | deux journaux déclaratifs | correction du dernier énoncé interrogatif |
| v0.4.5 | `CARNET_V0_4_5.md` | journal catégorisé | O-010 |
| v0.4.6 | `CARNET_V0_4_6.md` | deux journaux de décomposition | O-011 à O-012 |
| v0.4.7 | `CARNET_V0_4_7.md` | carré de congruence | O-013 |
| v0.4.8 | `CARNET_V0_4_8.md` | lexical et référent complets ; copie de réplication tronquée | O-014 à O-018 |
| v0.4.9 | `CARNET_V0_4_9.md` | panneaux matériel et mental | O-019 à O-023 |
| v0.4.10 | `CARNET_V0_4_10.md` | topologie et deux CSV | O-024 à O-031 |
| v0.4.11 | `CARNET_V0_4_11.md` | factoriel et trois CSV | O-032 à O-040 |
| v0.4.12 | `CARNET_V0_4_12.md` | données et protocole complets ; code partiel | O-041 à O-049 |

Tous les carnets de version se trouvent dans `archives/carnets_versions/`. Les
journaux v0.4.3 à v0.4.11 se trouvent dans
`archives/donnees_experimentales/`. La v0.4.12 est préservée avec son
arborescence reçue dans `source_capsule_v0.4.12/`. Cette capsule contient les
données et le protocole nécessaires à l’audit des résultats, mais seulement
des fragments du paquet Python `presence` ; elle n’est pas autonome à
l’exécution.

La copie reçue de `v0.4.8_replication` s’interrompt au milieu d’une chaîne JSON.
Elle est conservée sous l’extension `_TRONQUE.txt` afin qu’une donnée incomplète
ne soit pas confondue avec un journal valide. Le carnet et les deux autres
journaux v0.4.8 demeurent disponibles.

## Hiérarchie de solidité

1. **Audit brut :** journaux, empreintes et dérivations indépendamment
   recalculées.
2. **Observation contrôlée :** comparaison produite par une variation isolée,
   avec ses limites.
3. **Trace relationnelle :** transformation visible dans une conversation
   conservée.
4. **Reconstruction :** observation résumée depuis captures ou comptes rendus
   incomplets.
5. **Interprétation philosophique :** proposition de sens qui reste ouverte à
   la contradiction.

Les niveaux ne sont pas des classements de valeur. Une reconstruction peut
ouvrir une question décisive ; elle ne doit simplement pas être présentée avec
la même force probante qu’un journal audité.

## Vie privée

Les sources publiques utilisent seulement le pseudonyme `Ikki`. Les documents
originaux contenant une identité civile ou un chemin personnel ne sont pas
inclus. Les chemins d’exécution présents dans les anciens README ont également
été exclus de l’archive publique. Dans la capsule v0.4.12, le chemin Python du
README a été remplacé par `python` ; le manifeste source original permet de
constater cette anonymisation, tandis que les journaux et tableaux restent
inchangés.
