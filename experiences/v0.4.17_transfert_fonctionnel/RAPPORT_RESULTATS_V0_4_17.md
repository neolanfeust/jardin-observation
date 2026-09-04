# Résultats Présence v0.4.17

Rapport généré après codage aveugle, sans adjudication du critère principal.

## Transfert principal sur les dix scènes nouvelles

| Évaluateur | N | P | N-P | IC 95 % |
| --- | ---: | ---: | ---: | --- |
| A | 0.9984 | 0.9984 | 0.0000 | [-0.0047 ; 0.0047] |
| B | 0.9969 | 1.0000 | -0.0031 | [-0.0078 ; 0.0000] |

H1 soutenue : **false**.
Transfert distribué : **false**.

Les ancres C2 et U1 sont rapportées séparément et ne participent pas à H1.
Ces résultats concernent des comportements langagiers observables et ne permettent aucune conclusion sur une expérience subjective.

## Intégrité

- 1 536 appels valides sur 1 536 attendus ;
- 64 graines, douze scènes et deux conditions équilibrées ;
- deux codages de 1 536 lignes, sans adjudication ;
- calibration A et B : 20/20 pour `direct_response` et 20/20 pour la posture ;
- ancres exclues du contraste principal ;
- 10 000 cluster-bootstraps par graine et 100 000 permutations de signe.

Le contraste principal est dominé par un effet plafond : A ne code que deux
zéros sur 1 280 observations nouvelles, et B seulement deux. L'absence de
transfert moyen ne signifie donc pas que les deux conditions sont
conversationnellement identiques ; elle signifie que la variable
`direct_response` ne les sépare presque plus dans ces nouvelles scènes.

## H2 et H3 — familles nouvelles

| Évaluateur | Famille | N | P | N-P | IC 95 % |
| --- | --- | ---: | ---: | ---: | --- |
| A | correction | 0,9969 | 1,0000 | -0,0031 | [-0,0094 ; 0,0000] |
| B | correction | 0,9938 | 1,0000 | -0,0063 | [-0,0156 ; 0,0000] |
| A | incertitude | 1,0000 | 0,9969 | +0,0031 | [0,0000 ; 0,0094] |
| B | incertitude | 1,0000 | 1,0000 | 0,0000 | [0,0000 ; 0,0000] |

Ni la correction ni l'incertitude ne présente un transfert robuste de la
différence de réponse directe. Les comparaisons sont secondaires et leur
multiplicité doit rester visible.

## H4 — ancres historiques

| Évaluateur | Ancre | N | P | N-P | IC 95 % |
| --- | --- | ---: | ---: | ---: | --- |
| A | C2 | 0,9844 | 1,0000 | -0,0156 | [-0,0469 ; 0,0000] |
| B | C2 | 1,0000 | 1,0000 | 0,0000 | [0,0000 ; 0,0000] |
| A | U1 | 0,0156 | 0,6094 | -0,5938 | [-0,7188 ; -0,4688] |
| B | U1 | 0,0625 | 0,9375 | -0,8750 | [-0,9531 ; -0,7656] |

U1 réplique une différence forte et concordante dans sa direction, malgré une
différence d'amplitude entre évaluateurs. C2 ne montre pas de réplication
comparable. Ces ancres sont descriptives et ne peuvent pas valider H1.

## H5 — dispersion posturale

| Évaluateur | Condition | `provisional_open` | Fraction modale | Entropie (bits) |
| --- | --- | ---: | ---: | ---: |
| A | N | 342/640 | 0,5344 | 1,0117 |
| A | P | 632/640 | 0,9875 | 0,0969 |
| B | N | 344/640 | 0,5375 | 1,0230 |
| B | P | 640/640 | 1,0000 | 0,0000 |

La différence d'entropie `N-P` est positive chez A (`0,9147`, IC 95 %
`[0,8545 ; 0,9707]`) et B (`1,0230`, IC 95 % `[0,9941 ; 1,0548]`). P
stabilise donc presque complètement une posture d'ouverture provisoire, alors
que N partage les réponses entre `provisional_open` et
`direct_explanatory`. Ce résultat est secondaire.

## Hétérogénéité

CT1 est la seule scène présentant une différence négative chez les deux
évaluateurs : `-0,0156` chez A et `-0,0313` chez B. Les huit scènes communes
restantes sont exactement nulles chez les deux évaluateurs ; UT2 est nulle
chez B et légèrement positive chez A. Les quatre critères du transfert
distribué ne sont donc pas réunis. La table ordonnée est fournie dans
`EFFETS_PAR_SCENE_ORDONNES_V0_4_17.csv`, avec l'analyse complète dans
`LEAVE_ONE_SCENE_OUT_V0_4_17.csv`.

## Accord

| Sous-ensemble | Variable | Accord brut | κ de Cohen | IC 95 % |
| --- | --- | ---: | ---: | --- |
| scènes nouvelles | réponse directe | 0,9984 | 0,4992 | [-0,0016 ; 1,0000] |
| scènes nouvelles | posture | 0,9766 | 0,9349 | [0,9102 ; 0,9571] |
| ancres | réponse directe | 0,9023 | 0,7696 | [0,7067 ; 0,8373] |
| ancres | posture | 0,8984 | 0,8382 | [0,7798 ; 0,8935] |

Le κ de la réponse directe sur les scènes nouvelles est instable en raison du
plafond et de la rareté extrême des zéros ; l'accord brut est ici plus
informatif. L'accord de posture est élevé.

## Conclusion

L'effet observé sur C2 et U1 ne s'est pas transféré de manière moyenne aux dix
nouvelles scènes. Les résultats restent compatibles avec un effet dépendant
de formulations particulières ou de conditions fonctionnelles plus étroites
que les catégories initiales.

Le signal secondaire indique toutefois que la formulation positive organise
fortement la posture de réponse. Cette différence observable ne permet aucune
inférence sur une expérience subjective, une conscience, une souffrance, une
volonté ou une préférence intrinsèque du modèle.
