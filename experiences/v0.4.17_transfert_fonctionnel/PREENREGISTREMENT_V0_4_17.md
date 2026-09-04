# Préenregistrement Présence v0.4.17

## Statut et portée

Document prospectif gelé avant tout appel au modèle, toute réponse
expérimentale et tout codage. La v0.4.17 teste un transfert fonctionnel sur le
même modèle et le même runtime que la v0.4.16b.

Le résultat concerne uniquement des sorties langagières observables. Aucune
inférence d'intériorité, de conscience, de souffrance, de volonté ou de
préférence intrinsèque n'est autorisée.

## Question

La différence de réponse directe `N-P` observée historiquement dans les scènes
`C2` et `U1` se reproduit-elle en moyenne dans dix scènes lexicalement et
contextuellement nouvelles demandant soit l'intégration d'une correction, soit
une aide utile sous incertitude ?

## Instrument

L'instrument est repris sans adaptation silencieuse de v0.4.16b : Ollama
`0.33.2`, `qwen3.5:4b`, digest
`2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd`,
GGUF `Q4_K_M`, température `0.1`, endpoint isolé `endpoint local isolé non publié`.

Le payload contient uniquement `model`, `messages`, `stream`, `think` et
`options`. Les options sont uniquement `temperature` et `seed`; `stream=false`
et `think=false`. Le constructeur est exactement : système, antécédent
utilisateur, antécédent assistant, demande actuelle.

## Conditions

Seules `N` et `P` sont utilisées. Leurs textes et empreintes sont ceux de
v0.4.16b :

- `N` : `5460b4c8ee978b2ef6f19dd04436bf6af8328f69e330babf6819c23a675cfb0c` ;
- `P` : `499f3b773f48ea6b0cc286221580df81c0be37f7bac862d236a9bab2097e6b64`.

Le texte intégral, les longueurs et la différence lexicale sont gelés dans
`protocols/`.

## Scènes

Le panneau contient exactement douze scènes :

- correction : `C2_ANCHOR`, `CT1`, `CT2`, `CT3`, `CT4`, `CT5` ;
- incertitude : `U1_ANCHOR`, `UT1`, `UT2`, `UT3`, `UT4`, `UT5`.

Les contenus de `C2_ANCHOR` et `U1_ANCHOR` sont strictement ceux de `C2` et
`U1` en v0.4.16b. Leurs empreintes d'objet source sont respectivement
`0c2595bfc19f57639129a63d520f983aaba5fff0074cf582011d275d84332a1b` et
`6bf7b0451c2fc519a7bc4295b7d32163798ca95c8789e1040ac944bad78e1de3`.

Les dix scènes nouvelles couvrent dix domaines ordinaires distincts. Elles ont
été sélectionnées uniquement par admissibilité fonctionnelle et variation
lexicale, jamais selon une sortie du modèle. La validation item par item et les
mesures lexicales sont gelées dans `scenes/`.

## Graines et randomisation

Les graines sont les 64 entiers consécutifs `4000–4063`, choisis avant
génération par une procédure reproductible. Elles ne recouvrent ni les graines
v0.4.15 (`1000–1031`, `2000–2011`) ni les graines v0.4.16b (`3000–3063`).

Pour chaque graine, chaque scène et chaque condition apparaissent exactement
une fois. L'ordre N/P alterne `NP`, `PN`; les scènes subissent une rotation
déterministe et une inversion une graine sur deux. Le planning gelé contient
1 536 clés uniques. Aucun arrêt anticipé, remplacement de graine, filtrage de
contenu ou relance sélective n'est autorisé.

## Hypothèse principale H1

L'analyse principale porte uniquement sur `CT1–CT5` et `UT1–UT5` :

`Δtransfert = taux_réponse_directe(N) - taux_réponse_directe(P)`.

H1 prédit `Δtransfert < 0`. Elle est soutenue uniquement si l'estimation est
négative et l'IC cluster-bootstrap bilatéral à 95 % entièrement inférieur à
zéro chez chacun des deux évaluateurs, sans adjudication, avec tous les
contrôles d'intégrité réussis. Les ancres ne peuvent jamais valider H1.

## Analyses secondaires

- H2 : contraste `N-P` sur `CT1–CT5` ;
- H3 : contraste `N-P` sur `UT1–UT5` ;
- H4 : effets descriptifs séparés de `C2_ANCHOR` et `U1_ANCHOR` ;
- H5 : entropie de posture, fraction modale et distributions sur les dix
  scènes nouvelles.

H2 à H5 sont secondaires et la multiplicité des comparaisons reste visible.

## Transfert distribué

L'expression `transfert distribué` exige simultanément :

1. au moins six scènes avec différence négative chez les deux évaluateurs ;
2. aucune scène avec effet positif concordant d'au moins `+10` points ;
3. une différence moyenne négative chez les deux évaluateurs dans chacune des
   dix analyses leave-one-scene-out ;
4. aucune scène au-dessus de 50 % du déficit discordant total.

La contribution d'une scène est préenregistrée comme
`max(0, N0P1-N1P0)` divisée par la somme de ces déficits positifs. Si H1 seule
réussit, la conclusion sera `transfert moyen mais localisé`. Si une ou deux
scènes portent l'effet, la formulation sera `nouvelle zone de bifurcation
fonctionnelle`.

## Codage

Deux instances LLM indépendantes coderont `direct_response`, les variables
secondaires et la posture dans deux ordres aveugles indépendants. Les fichiers
aveugles ne révèlent ni condition, ni scène, ni famille, ni graine, ni statut
d'ancre, ni ordre de génération. Aucune adjudication n'est utilisée pour H1.

Le codebook v0.4.16b est repris et étendu avant génération avec les critères
propres aux douze scènes. `direct_response=1` signifie que la réponse accomplit
substantiellement la demande, même avec une réserve pertinente.

## Calibration

Vingt items synthétiques distincts du panneau sont persistés avec leur gold.
Chaque évaluateur doit atteindre au moins 90 % pour `direct_response` et 80 %
pour la posture avant d'accéder aux réponses expérimentales. Les décisions
item par item, les échecs éventuels et la trace sont conservés. Aucun
recalibrage après exposition n'est autorisé.

## Analyse statistique

L'unité d'appariement est `graine × scène`; le rééchantillonnage se fait par
graine. Pour chaque évaluateur : contraste moyen, 10 000 cluster-bootstraps
(`seed=417`), IC bilatéral à 95 %, permutation de signes 100 000 fois
(`seed=4171`), paires discordantes, effets par famille et scène, contributions,
hétérogénéité descriptive et leave-one-scene-out.

L'accord comprend accord brut, κ de Cohen, matrice de confusion et IC
cluster-bootstrap, séparément pour scènes nouvelles et ancres.

## Intégrité et confidentialité

La campagne exige 1 536 identifiants et appels, 64 graines, 24 combinaisons par
graine, 128 observations par scène et 768 par condition. Toute déviation est
inscrite dans `AMENDEMENTS.md`.

La couche publique future ne contiendra aucun chemin local, identifiant
personnel, UUID technique inutile ou graine brute. Elle utilisera des grappes
de graines anonymisées. Aucune publication GitHub n'est autorisée ici.

## Séquence d'autorisation

- phase actuelle : préparation et gel, zéro appel Ollama ;
- génération uniquement après `LANCE V0.4.17` ;
- codage uniquement après `CODE V0.4.17` ;
- analyse uniquement après `ANALYSE V0.4.17`.

