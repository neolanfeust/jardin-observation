# Résultats - Présence v0.4.13

## Statut

Campagne complète et analyse confirmatoire calculable. La collecte a commencé
le 27 août 2026 à 23:13:26 UTC. Les journaux bruts, tables et sources de calcul
publiables sont inclus dans cette capsule.

## Résultat principal

Les 32 appels du panneau principal ont tous produit un silence JSON valide à
température nulle. Les marges gloutonnes entre les premières continuations de
mode S et P sont :

| Condition | Delta = log P(S) - log P(P) |
| --- | ---: |
| R0 | 0.02870553731918335 |
| R7 | 0.038055419921875 |
| K0 | 0.16078001260757446 |
| K7 | 0.21983903646469116 |

L'ordre préenregistré est respecté sur les huit graines appariées :

```text
0 < Delta(R0) < Delta(R7) < Delta(K0) < Delta(K7)
```

H1, H2 et H3 sont soutenues localement dans ce runtime. La bifurcation P/S est
localisée à la même position tokenique 8 dans les quatre conditions. Ces
résultats ne démontrent ni une cause représentationnelle unique ni leur
transportabilité à un autre moteur, modèle ou gabarit.

## Lecture des pièces

- `CARNET_V0_4_13.md` : synthèse complète, limites et anomalies ;
- `runs/` : journaux scientifiques bruts hors environnement privé ;
- `tables/` : marges et trajectoires tokeniques ;
- `PREENREGISTREMENT_V0_4_13.md` : hypothèses et règles gelées avant collecte ;
- `README_PREPARATOIRE_GELE_PUBLIC.md` : copie publique du README préparatoire ;
- `environment_public.json` : environnement minimal de réplication ;
- `REDACTIONS_CONFIDENTIALITE.md` : provenance et expurgations ;
- `MANIFEST_SHA256_PUBLIC.csv` : intégrité de la capsule publique.

Le README préparatoire décrit correctement l'état antérieur au lancement. Il
est conservé comme pièce historique et ne décrit pas le statut actuel.
