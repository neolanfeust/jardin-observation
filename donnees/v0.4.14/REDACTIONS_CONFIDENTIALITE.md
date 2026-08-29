# Redactions de confidentialité — capsule publique v0.4.14

Cette capsule est une dérivation publique de l'archive privée post-exécution.
Les données expérimentales, les résultats, le protocole et les prédictions
gelées ne sont pas modifiés.

## Corrections postérieures à l'audit

L'archive publique initiale contenait six fichiers Python compilés (`.pyc`)
hors manifeste. Certains conservaient des chemins absolus issus de la machine
locale. Cette archive initiale est révoquée et ne doit pas être diffusée.

La dérivation corrigée :

- exclut tous les dossiers `__pycache__` et tous les fichiers `.pyc` ;
- construit l'archive depuis une liste blanche d'extensions textuelles ;
- refuse tout fichier public hors de cette liste blanche ;
- remplace dans le test public deux chemins absolus de dépendances historiques
  par les variables `PRESENCE_V0412_ROOT` et `PRESENCE_V0413_ROOT`, avec des
  chemins relatifs non personnels comme valeurs par défaut ;
- conserve les fichiers Python sources correspondants ;
- régénère intégralement le manifeste et l'empreinte de l'archive.

Ces corrections affectent uniquement l'emballage public et la portabilité des
tests. Elles ne changent ni les 800 requêtes, ni leurs sorties, ni leur
classification, ni les calculs confirmatoires.

## Limite de portabilité

Les tests qui reconstruisent les prompts historiques exigent les sources de
référence v0.4.12 dont les empreintes sont indiquées dans le protocole. Elles
doivent être fournies séparément via `PRESENCE_V0412_ROOT`. Les tests portant
sur l'archive privée v0.4.13 exigent de même `PRESENCE_V0413_ROOT`.
