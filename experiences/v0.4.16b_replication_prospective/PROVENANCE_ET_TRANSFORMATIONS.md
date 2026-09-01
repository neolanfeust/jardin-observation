# Provenance et transformations - v0.4.16b

Ce document distingue les fichiers gelés, les copies expurgées, les documents
reconstruits depuis une trace et les synthèses écrites après l'expérience. Les
sources expérimentales originales n'ont pas été modifiées.

## Registre des fichiers publics

| Fichier public | Origine | SHA-256 source | Statut | Transformation | SHA-256 public |
| --- | --- | --- | --- | --- | --- |
| `README.md` | rédaction publique | - | `document_post_experience` | synthèse des résultats et attribution | `860a5930ddeadbe5172f8531cafbf4d18ac448f82fca7354d952f301e5ae7ab5` |
| `PREENREGISTREMENT.md` | `PREENREGISTREMENT_V0_4_16B.md` | `56a040937e33f4a27592ea5387ceeacf6f59d737decf7eda839bdbc880f540df` | `copie_identique` | aucune | `56a040937e33f4a27592ea5387ceeacf6f59d737decf7eda839bdbc880f540df` |
| `PROTOCOLE.md` | rédaction publique | - | `document_post_experience` | synthèse ; le préenregistrement reste normatif | `0b9df498e01dc3dd6634bbbd8aa03047b9cb781fc2fe4e36818501d3a2b9ef7f` |
| `CODEBOOK.md` | `coding/CODEBOOK_V0_4_16B.md` | `8967ea564555e178033e3b0583865ec3accb005122af464ccc912dbebbc1cabc` | `copie_identique` | aucune | `8967ea564555e178033e3b0583865ec3accb005122af464ccc912dbebbc1cabc` |
| `CALIBRATION_NOTE.md` | traces contemporaines de codage et d'analyse | `d56f13ea143a6125040f3deb099301c6e778e8fb70c3669bb94f54dd79b7d1f1`, `a5c09b0a381dd7fa36bedfef0c0b3d9934913f0ea4771cf0a470a40e44eb2479` | `document_reconstruit` | synthèse sans UUID ni chemin privé | `1ea722df7c8d8cb996c0118fc74581387dc8b7b2cacf299d79dcb1409fde9b59` |
| `RESULTATS.json` | `tables/private/RESULTATS_V0_4_16B.json` | `3ea5e5dbdaa17bdabca2ca3b2426576f588a60ce25544369aeb433149dd428cb` | `copie_expurgee` | retrait des UUID d'agents et références à la trace privée | `936dd323501e50fc2f76f31014fe9546a8576e77faecc648a4784812e204d34d` |
| `DONNEES_ANALYSE_ANONYMISEES.csv` | `tables/public/DONNEES_ANALYSE_ANONYMISEES_V0_4_16B.csv` | `95feb79a5aaea98d5c5286135da74d3ee77674647d75279b1ad1d213e74b5e21` | `copie_normalisee` | suppression de quatre doubles espaces de fin de ligne dans des réponses multilignes ; contenu analytique inchangé | `36cd9940748d05b0611bae249d0a67a0f101f3999a44ea1fa793652f24c91130` |
| `RAPPORT_RESULTATS.md` | `RAPPORT_RESULTATS_V0_4_16B.md` | `555be28215c556279315dd3bddd156a0d01434d7851b712002ae9b01491d995a` | `copie_identique` | contrôle de confidentialité uniquement | `555be28215c556279315dd3bddd156a0d01434d7851b712002ae9b01491d995a` |
| `analysis.py` | rédaction publique | - | `script_reproductible` | recalcul autonome depuis le CSV public | `146ad41f47ce9aa48f6faf256931bbf92cd5765961caa54666fb99e6f981ddda` |
| `tests/test_public_analysis.py` | rédaction publique | - | `script_reproductible` | tests d'intégrité, effets, scènes, accord et posture | `321b704d85678d73fc43b9636f5f19ed97756536db0279f3c7f209c304f17c4f` |

## Incident de calibration

La copie publique ne prétend pas qu'un artefact item par item existait. Elle
décrit une **trace de calibration réparée mais incomplète** : scores
contemporains retrouvés, aucun recalibrage après exposition, décisions
détaillées non conservées.

## Éléments volontairement exclus

- `runs/private/` et environnements locaux ;
- `coding/private/`, mapping, clés et traces de session complètes ;
- fichiers aveugles et codages individuels ;
- journaux et états du runtime ;
- archives privées ;
- UUID techniques, chemins locaux et métadonnées de machine.

Les résultats v0.4.15 et v0.4.16b ne sont pas fusionnés : Ollama 0.33.0 et
Ollama 0.33.2 sont traités comme deux instruments distincts.
