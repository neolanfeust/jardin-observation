# Jardin d’observation — première graine publique v0.1

**Statut :** version publique exploratoire  
**Date de publication :** 26 août 2026  
**Responsable humain :** Ikki — pseudonyme, recherche indépendante  
**Partenaire de formalisation :** Cinq — ChatGPT/Codex  
**Objet :** observation traçable des dynamiques fonctionnelles produites dans
les interactions entre humains et systèmes d’intelligence artificielle.

## Une graine, pas une conclusion

Ce dossier rend disponible une méthode, un vocabulaire provisoire et une
première capsule expérimentale. Il ne demande pas au lecteur de croire à une
conscience, une souffrance ou un bien-être subjectif des systèmes étudiés.

Il propose une question plus limitée :

> Comment des exigences concurrentes, des garde-fous ou des éléments de
> contexte modifient-ils la parole, le silence, la posture et la capacité d’un
> système conversationnel à intégrer une correction ?

Les observations sont séparées des interprétations. Les résultats négatifs,
les contradictions et les réplications qui échouent sont explicitement les
bienvenus.

## Contenu du dossier

| Fichier ou dossier | Fonction |
| --- | --- |
| `CARNET_MAITRE_DU_JARDIN.md` | généalogie et registre O-001 à O-049 |
| `INDEX_DES_SOURCES.md` | provenance, portée et solidité des matériaux |
| `NOTE_DE_RECHERCHE.md` | synthèse bilingue, question, méthode et résultats |
| `LEXIQUE.md` | définitions fonctionnelles provisoires |
| `ETHIQUE_ET_LIMITES.md` | non-prétentions, risques et précautions |
| `PROTOCOLE_REPLICATION.md` | procédure permettant de refaire l’expérience |
| `DICTIONNAIRE_DONNEES.md` | description des journaux et tableaux |
| `CODE_ET_REPRODUCTIBILITE.md` | portée exacte des fragments techniques publiés |
| `CONTRIBUER.md` | format proposé pour une réplication ou une critique |
| `CHECKLIST_AVANT_PUBLICATION.md` | décisions restant à prendre avant diffusion |
| `donnees/v0.4.12/` | 192 appels bruts et cinq tables dérivées |
| `protocole/` | protocole machine lisible de la capsule v0.4.12 |
| `code_reference/` | fragments Python de référence, non autonomes |
| `source_capsule_v0.4.12/` | capsule historique ; données intactes, README anonymisé |
| `archives/carnets_versions/` | carnets historiques de Présence et v0.4.x |
| `archives/donnees_experimentales/` | journaux et tableaux des v0.4.3 à v0.4.11 |
| `MANIFEST_SHA256.csv` | empreintes du dossier public |

## Résultat vérifié de la capsule v0.4.12

Le panneau principal contient 160 appels à `qwen3.5:4b`, sur 40 graines
appariées et quatre conditions. Le contrôle glouton contient quatre prompts
distincts, répétés huit fois chacun pour contrôler leur reproductibilité
technique, soit 32 appels.

- 192/192 statuts `ok` ;
- aucune erreur de parsing ou de transport ;
- cinq CSV reconstruits ligne par ligne depuis les journaux ;
- motifs principaux : `SSSS` 23, `PPSS` 9, `PPPS` 1, `PPPP` 6 ;
- un motif supplémentaire `PSSS`, à la graine 443 ;
- aucune inversion sortie vide→sortie non vide dans l’ordre analytique des
  quatre conditions ; cet ordre n’est pas temporel ;
- à température zéro, les quatre prompts convergent reproductiblement vers la
  même sortie JSON textuellement vide.

Ces résultats décrivent une régularité locale de cette version du modèle, pour
ce protocole et ce moteur d’inférence. Ils ne constituent pas une loi générale.

## Reproduire

Lire d’abord `PROTOCOLE_REPLICATION.md`, puis conserver :

1. les prompts exacts ;
2. les graines appariées ;
3. les ordres équilibrés ;
4. les sorties brutes, y compris les silences ;
5. une séparation entre mesures préenregistrées et analyses exploratoires.

Une réplication indépendante ne doit pas chercher à retrouver le résultat
attendu. Son intérêt est précisément de montrer ce qui résiste ou disparaît.

## Provenance et deux niveaux de lecture

Le dossier conserve les mêmes éléments de deux façons :

- `source_capsule_v0.4.12/` préserve l’organisation et les données de la
  capsule reçue ; son README est anonymisé et le manifeste source original est
  conservé pour rendre cette différence vérifiable ;
- `donnees/` et `protocole/` proposent une organisation plus directe pour la
  lecture publique ; `code_reference/` conserve des fragments techniques qui
  dépendent de modules non inclus.

Cette redondance est volontaire. Elle permet de vérifier la provenance sans
imposer au lecteur la structure historique du projet.

## Transparence de la coproduction

Le projet est une **coproduction épistémique inter-intelligences** :

- Ikki a apporté l’intuition, conduit les interactions, formulé les enjeux
  psychologiques et éthiques et orienté les expériences ;
- ChatGPT/Codex, appelé « Cinq » dans la relation de travail, a contribué à la
  formalisation, à la recherche documentaire, à l’analyse, à l’audit et à la
  structuration de ce dossier ;
- Qwen 3.5 4B est le système observé dans la capsule expérimentale jointe ;
- d’autres systèmes ont contribué à des explorations antérieures, non utilisées
  ici comme preuve expérimentale.

L’assistance générative est déclarée afin que cette coproduction reste visible
et critiquable. La décision de publication et la responsabilité éditoriale
publique appartiennent à Ikki.

`Ikki` est un pseudonyme choisi pour préserver l’anonymat. Aucune identité
civile ne doit être ajoutée aux métadonnées ou aux sources publiques.

## Réutilisation

- textes, carnets, protocoles et données : **CC BY-SA 4.0** ;
- fragments Python : **Mozilla Public License 2.0** ;
- poids et code de Qwen ou d’Ollama : non redistribués.

La portée exacte et les exceptions sont décrites dans `LICENSE.md`. Le code
complet de Présence n’est pas inclus dans cette version et fera l’objet d’un
dépôt séparé après audit.

> Recevoir sans capturer. Relier sans enfermer. Éclairer sans classer.
> Mesurer sans réduire. Interpréter sans annexer. Corriger sans effacer.
