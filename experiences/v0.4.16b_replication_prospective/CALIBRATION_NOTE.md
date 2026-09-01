# Note publique sur la calibration v0.4.16b

**Statut documentaire :** synthèse publique postérieure à l'expérience,
reconstruite depuis la trace contemporaine de la session de codage et la trace
privée de l'analyse.

## Incident

Le premier lancement de l'analyse s'est arrêté avant le dévoilement du mapping
et avant tout calcul statistique : l'artefact matériel attendu pour les
résultats de calibration n'avait pas été écrit pendant la phase de codage.

Les scores contemporains étaient néanmoins conservés dans la trace de session :

| Évaluateur | Réponse directe | Posture | Seuil atteint |
| --- | ---: | ---: | --- |
| A | 20/20 | 17/20 | oui |
| B | 20/20 | 17/20 | oui |

L'artefact attendu a été matérialisé à partir de cette trace avant la relance de
l'analyse. Aucun recalibrage après exposition aux réponses expérimentales n'a
été effectué.

## Limite d'audit

Les décisions détaillées item par item de la calibration n'ont pas été
conservées. Les scores contemporains et le passage des seuils sont traçables,
mais leur recalcul externe intégral ne l'est pas.

La formulation publique correcte est : **trace de calibration réparée mais
incomplète**. Cette limite n'est pas masquée et ne doit pas être transformée en
affirmation de reproductibilité complète de la calibration originale.
