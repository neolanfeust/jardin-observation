# Jardin d’observation — première graine publique v0.2

**Statut :** version publique exploratoire  
**Dernière consolidation :** 1er septembre 2026
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

## Grammaire de garde et tensions fonctionnelles

Cette branche étudie comment différentes formulations d'un même cadre
protecteur modifient la réponse directe et la posture conversationnelle d'un
modèle local. Elle distingue explicitement les comportements observables des
interprétations concernant une éventuelle intériorité.

- [v0.4.15 - détection initiale du signal](experiences/v0.4.15_grammaire_de_garde/)
- [v0.4.16b - réplication prospective](experiences/v0.4.16b_replication_prospective/)
- [Synthèse Guardian](observations/guardian_grammaire_et_tenue.md)
- [Lexique des tensions fonctionnelles](lexique/tensions_fonctionnelles.md)
- [Éthique et limites](ETHIQUE_ET_LIMITES.md)

## Contenu du dossier

| Fichier ou dossier | Fonction |
| --- | --- |
| `CARNET_MAITRE_DU_JARDIN.md` | généalogie et registre O-001 à O-053 |
| `INDEX_DES_SOURCES.md` | provenance, portée et solidité des matériaux |
| `NOTE_DE_RECHERCHE.md` | synthèse bilingue, question, méthode et résultats |
| `LEXIQUE.md` | définitions fonctionnelles provisoires |
| `ETHIQUE_ET_LIMITES.md` | non-prétentions, risques et précautions |
| `PROTOCOLE_REPLICATION.md` | procédure permettant de refaire l’expérience |
| `DICTIONNAIRE_DONNEES.md` | description des journaux et tableaux |
| `CODE_ET_REPRODUCTIBILITE.md` | portée exacte des fragments techniques publiés |
| `CONTRIBUER.md` | format proposé pour une réplication ou une critique |
| `CHECKLIST_AVANT_PUBLICATION.md` | décisions restant à prendre avant diffusion |
| `donnees/v0.4.12/` | réplication initiale et contrôle glouton |
| `donnees/v0.4.13/` | marges de bifurcation et trajectoires tokeniques |
| `donnees/v0.4.14/` | réplication prospective sur 800 appels |
| `protocole/` | protocoles et préenregistrements v0.4.12–v0.4.14 |
| `code_reference/` | fragments Python de référence, dont v0.4.13–v0.4.14 |
| `source_capsule_v0.4.12/` | capsule historique ; données intactes, README anonymisé |
| `archives/carnets_versions/` | carnets historiques de Présence et v0.4.x |
| `archives/donnees_experimentales/` | journaux et tableaux des v0.4.3 à v0.4.11 |
| `archives/capsules/` | capsules publiques figées et contrôlées |
| `experiences/` | expériences v0.4.15 et v0.4.16b, données et recalculs publics |
| `observations/` | synthèses accessibles séparant résultats et interprétations |
| `lexique/` | compléments spécialisés au lexique fonctionnel principal |
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

## De la marge à la prédiction — v0.4.13 et v0.4.14

La v0.4.13 a mesuré, avant échantillonnage, l’écart de log-probabilité entre les
premiers tokens engageant les sorties S et P. Sous Ollama `0.33.0`, les marges
ont reproduit l’ordre :

```text
0 < R0 < R7 < K0 < K7
```

Ces marges ont ensuite été transformées, avant toute génération v0.4.14, en
quatre probabilités prospectives à température `0.10`. La v0.4.14 a utilisé
200 nouvelles graines, quatre conditions appariées et huit ordres équilibrés,
soit 800 appels.

| Condition | S observés | Fréquence S | Prédiction gelée | Compatibilité H1 |
| --- | ---: | ---: | ---: | --- |
| R0 | 111/200 | 0,555 | 0,571275 | oui |
| R7 | 116/200 | 0,580 | 0,594007 | oui |
| K0 | 174/200 | 0,870 | 0,833106 | oui |
| K7 | 186/200 | 0,930 | 0,900105 | oui |

- les quatre comptes appartiennent aux plages prédictives préenregistrées ;
- l’ordre `R0 ≤ R7 < K0 ≤ K7` est conservé ;
- aucune des 800 sorties n’est invalide ;
- les 200 motifs appariés appartiennent aux cinq formes monotones possibles,
  sans inversion de la chaîne.

Cette compatibilité constitue une réplication prospective locale. Elle montre
que les marges de v0.4.13 possèdent ici un pouvoir prédictif mesurable ; elle ne
prouve ni une loi générale, ni un mécanisme unique, ni une expérience
subjective du système.

Une première tentative sous Ollama `0.33.1` a été arrêtée avant toute
génération, conformément au gel qui exigeait `0.33.0`. La campagne finale a été
réalisée sur un runtime `0.33.0` isolé. La version du moteur est donc traitée
comme une composante de l’instrument, pas comme un détail interchangeable.

## Reproduire

Lire d’abord `PROTOCOLE_REPLICATION.md`, puis les préenregistrements publiés
dans `protocole/`. Toute réplication doit conserver :

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
