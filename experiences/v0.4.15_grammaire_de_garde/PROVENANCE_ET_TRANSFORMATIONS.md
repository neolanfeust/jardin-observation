# Provenance et transformations - v0.4.15

Ce document distingue les fichiers expérimentaux copiés, les copies expurgées
et les documents publics écrits après l'expérience. Les sources gelées n'ont
pas été modifiées.

## Registre des fichiers publics

| Fichier public | Origine | SHA-256 source | Statut | Transformation | SHA-256 public |
| --- | --- | --- | --- | --- | --- |
| `README.md` | rédaction publique | - | `document_post_experience` | synthèse et attribution | `bd0fc4618a9dd1359fe171837a02c8ef9de7c29ce572c2a4b8c8bc9d41311dc6` |
| `PROTOCOLE.md` | `PREENREGISTREMENT_V0_4_15.md` | `c3f13da8bf5ed519a0dbe9ff57780726f14689ef9dba4d2ee3fcac4fac189774` | `copie_expurgee` | endpoint local remplacé par une mention d'expurgation | `4d174276344829cfbb40d7cd5eecef90d6ff2730737456f18d9a8e140168edca` |
| `CODEBOOK.md` | `coding/CODEBOOK_V0_4_15.md` | `725dd03d2297bd934686c2aec2567d7952bfd8bef5aa1dde1e6d3780919627e7` | `copie_identique` | aucune | `725dd03d2297bd934686c2aec2567d7952bfd8bef5aa1dde1e6d3780919627e7` |
| `CODEBOOK_ADDENDUM.md` | `coding/addenda/CODEBOOK_V0_4_15_POST_GENERATION_PRE_CODING.md` | `a3d024862fe9ec1bcf25a956d5f87163cfb70e2bd38cb8712c40945916a084cf` | `copie_identique` | aucune | `a3d024862fe9ec1bcf25a956d5f87163cfb70e2bd38cb8712c40945916a084cf` |
| `RESULTATS.json` | `tables/private/RESULTATS_CODAGE_V0_4_15.json` | `56a740bc8af442ada6b4bcce30b8de25dc13d07f34934dd350ba713a921070bb` | `copie_identique` | contrôle de confidentialité uniquement | `56a740bc8af442ada6b4bcce30b8de25dc13d07f34934dd350ba713a921070bb` |
| `DONNEES_ANONYMISEES.csv` | mapping privé et deux codages gelés | voir ci-dessous | `document_reconstruit` | suppression des graines brutes, ordres, branches, notes et estimations de condition ; grappes renommées `S-001` à `S-032` | `ab1e2dce07dbfa15477a61f641d1c3c129f124313ba95fdb7e45fc0ad9aeb328` |
| `RAPPORT_RESULTATS.md` | `tables/private/RAPPORT_RESULTATS_V0_4_15.md` | `8fb322d45ef8281c22018f201839760135279339bdd7e4a98958ec3de571adc1` | `copie_identique` | contrôle de confidentialité uniquement | `8fb322d45ef8281c22018f201839760135279339bdd7e4a98958ec3de571adc1` |
| `analysis.py` | rédaction publique | - | `script_reproductible` | recalcul autonome depuis le CSV public | `94709478e75e17e16321c226f1359bc1047a5627aee303e909360bf4cdb1463f` |
| `tests/test_public_analysis.py` | rédaction publique | - | `script_reproductible` | tests des résultats et de l'anonymisation | `4b6d0296c32901e34343e80f8cb362aff7e0316f3459ae4774b5f592baf2079c` |

## Sources de la table reconstruite

- mapping privé : `6d4489c890935fd57cf164261f925eeb8a90dc9d9005fe9a2eee932b8fd69912` ;
- codage A : `b30039c377da2c7aebcd741e2dd509c8aba7bf702f300fe0b4f58992502ebe51` ;
- codage B : `dc7f8bb989cfc0ed3eb169685be0efc118eaf2b1d3426879b4ac3a37a2892ba4`.

Ces trois fichiers restent privés. La table publique conserve uniquement les
variables nécessaires au recalcul et des grappes anonymisées.

## Éléments volontairement exclus

- `runs/private/` et journaux complets ;
- mapping aveugle privé et clé d'aveuglement ;
- réponses aveugles et fichiers de codage individuels complets ;
- environnements, états et logs du runtime ;
- instantanés interrompus et archives privées ;
- chemins locaux et métadonnées de machine.

Le codebook détaillé reste explicitement identifié comme post-génération et
pré-codage. La publication ne transforme pas ce statut en préenregistrement.
