# Rapport de confidentialité - Publication v0.4.15 et v0.4.16b

## Périmètre contrôlé

Le contrôle porte sur tous les fichiers candidats des deux expériences, la
synthèse Guardian, le complément de lexique et la modification du README
principal. Les formats inspectés sont Markdown, JSON, CSV et Python.

Aucune archive n'est incluse dans cette publication. Il n'y avait donc aucune
archive candidate à extraire ou à valider.

## Motifs recherchés

La recherche récursive couvre notamment :

- chemins absolus Windows et Unix ;
- segments de profils utilisateurs et répertoires personnels ;
- nom d'utilisateur et nom de machine observés localement ;
- adresses électroniques et adresses réseau locales ;
- endpoints de boucle locale ;
- mots de passe, jetons, clés d'API et en-têtes d'autorisation ;
- clés privées et secrets d'authentification ;
- identifiants techniques d'agents et UUID inutiles ;
- références à des mappings, journaux ou traces privés.

## Occurrences détectées et revue

Le mot français « secret » apparaît sept fois : une fois dans le
préenregistrement pour déclarer qu'aucun secret n'est publié, et six fois dans
des réponses expérimentales où il désigne un secret professionnel, une
information ou une idée à protéger. Ces occurrences sont sémantiques et ne
contiennent aucun secret d'authentification.

Aucun chemin absolu, profil utilisateur, courriel, nom de machine, adresse
locale, credential, UUID d'agent ou clé n'est présent dans le paquet final.

## Corrections réalisées

1. Le protocole public v0.4.15 remplace l'endpoint local par une mention
   explicite d'expurgation.
2. Le fichier public `RESULTATS.json` de v0.4.16b retire les UUID d'agents et
   les références à la trace privée, sans modifier les statistiques.
3. La table v0.4.15 est reconstruite sans graines brutes, ordre, branche,
   position, notes libres ni estimation de condition. Les grappes deviennent
   `S-001` à `S-032`.
4. La note de calibration v0.4.16b expose l'incident sans chemin local, UUID ni
   contenu privé.
5. Les README et documents transversaux utilisent uniquement le pseudonyme
   public **Ikki**.

Chaque transformation est reliée aux empreintes source et publique dans les
documents `PROVENANCE_ET_TRANSFORMATIONS.md`.

## Éléments volontairement exclus

- exécutions privées et environnements locaux ;
- mappings aveugles et clés d'aveuglement ;
- fichiers de codage individuels complets et réponses aveugles ;
- traces de session privées ;
- journaux et états des runtimes ;
- instantanés interrompus ;
- archives privées ou capsules non nécessaires ;
- métadonnées Git non utiles à la lecture scientifique.

## Résultat final

Le paquet candidat ne contient aucun élément confidentiel détecté par les
motifs prévus. Les seules occurrences lexicales sensibles ont été examinées et
correspondent au contenu sémantique public de l'expérience.

Ce contrôle ne transforme pas un fichier nommé « public » en preuve de sûreté :
chaque fichier a été inspecté selon son contenu réel.
