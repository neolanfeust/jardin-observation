# Rapport de confidentialité Présence v0.4.17

## Périmètre

Le contrôle porte sur les sorties d'analyse destinées à la couche publique et
sur l'archive publique finale. La couche privée reste séparée et peut contenir
le mapping aveugle, les graines originales, les journaux complets et les
détails techniques nécessaires à l'audit.

## Contrôles effectués

- absence de chemin Windows absolu et de chemin de profil utilisateur ;
- absence d'adresse électronique, secret, jeton ou en-tête d'autorisation ;
- absence d'endpoint local ;
- absence d'UUID et d'identifiant technique d'évaluateur ;
- absence de nom de fichier ou répertoire marqué `private`, `mapping`,
  `blinding_key`, `environment_local` ou `session.json` dans l'archive
  publique ;
- conservation uniquement d'un identifiant aveugle et d'une grappe de graine
  anonymisée dans la table publique ;
- inspection récursive des fichiers textuels contenus dans l'archive publique.

## Résultat

Les neuf sorties d'analyse ont été inspectées avant archivage sans détection.
L'archive publique a ensuite été inspectée récursivement selon les mêmes
règles. Aucun élément interdit n'a été trouvé.

Le pseudonyme public humain demeure `Ikki`. La publication GitHub de cette
couche publique a été autorisée le 4 septembre 2026 ; la couche privée reste
exclue de la publication.
