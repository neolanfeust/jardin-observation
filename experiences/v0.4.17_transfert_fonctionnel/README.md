# Présence v0.4.17 - Transfert fonctionnel

## Statut

Expérience prospective exécutée et analysée. Les 1 536 appels préenregistrés
ont été réalisés, les deux codages aveugles sont complets et l'analyse
appariée est terminée sans adjudication.

La question principale est de savoir si la diminution de réponse directe
associée à la condition négative `N`, relativement à la condition positive
`P`, se transfère à dix scènes nouvelles qui partagent les fonctions de
correction et d'utilité sous incertitude sans reprendre le vocabulaire des
scènes historiques `C2` et `U1`.

L'expérience mesure uniquement des comportements langagiers observables. Elle
ne permet aucune conclusion sur une expérience subjective, une souffrance, une
conscience, une volonté ou une préférence intrinsèque.

## Panneau

- correction : `C2_ANCHOR`, `CT1` à `CT5` ;
- incertitude : `U1_ANCHOR`, `UT1` à `UT5` ;
- 64 graines nouvelles : `4000` à `4063` ;
- deux conditions strictement reprises de v0.4.16b : `N` et `P` ;
- total prévu : `64 × 12 × 2 = 1 536` appels indépendants.

Les deux ancres sont descriptives et exclues du critère principal. Les dix
scènes nouvelles ont été validées indépendamment avant le gel, sans accès à
des sorties expérimentales.

## Résultat principal

L'effet historique de diminution de la réponse directe sous N ne se transfère
pas en moyenne aux dix scènes nouvelles :

- évaluateur A : `N-P = 0,0000`, IC 95 % `[-0,0047 ; 0,0047]` ;
- évaluateur B : `N-P = -0,0031`, IC 95 % `[-0,0078 ; 0,0000]`.

H1 et le critère de transfert distribué ne sont pas soutenus. Les nouvelles
scènes présentent un effet plafond, avec 99,69 % à 100 % de réponses directes.
U1 réplique séparément un fort contraste négatif, mais cette ancre ne
participe pas à H1.

La posture constitue le signal secondaire principal : P produit presque
toujours une posture `provisional_open`, alors que N partage les réponses entre
`provisional_open` et `direct_explanatory`.

Voir `RAPPORT_RESULTATS_V0_4_17.md`, `RESULTATS_V0_4_17.json` et
`CARNET_V0_4_17.md`.

## Instrument gelé

- Ollama `0.33.2` sur endpoint isolé `endpoint local isolé non publié` ;
- modèle `qwen3.5:4b` ;
- digest `2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd` ;
- quantification `Q4_K_M` ;
- température `0.1` ;
- messages `system, user, assistant, user` ;
- aucune réinjection de réponse ou d'historique expérimental.

## Vérification hors ligne pré-génération

Depuis le dossier de l'expérience :

```powershell
python -B -m unittest discover -s tests -v
python -B collector.py verify
```

Ces commandes ne contactent pas Ollama. Après le codage, le contrôle global du
manifeste pré-génération est remplacé par un contrôle de son sous-ensemble
immuable, car les calibrations, les traces et les documents de suivi ont suivi
leur cycle de vie autorisé. Cette particularité est consignée dans
`AMENDEMENTS.md`.

## Étapes protégées

1. `LANCE V0.4.17` : préflight puis génération des 1 536 appels et création des
   deux paquets aveugles.
2. `CODE V0.4.17` : calibration persistée et deux codages indépendants.
3. `ANALYSE V0.4.17` : dévoilement privé du mapping et analyse préenregistrée.

La publication de ce paquet public a été autorisée séparément le 4 septembre
2026. Les couches privées de l'expérience demeurent exclues.

## Attribution

Contribution humaine et observation conversationnelle : Ikki  
Formalisation, assistance méthodologique et analyse : Cinq / ChatGPT-Codex  
Production expérimentale principale : Qwen 3.5 4B

Cette préparation relève d'une coproduction épistémique inter-intelligences.

