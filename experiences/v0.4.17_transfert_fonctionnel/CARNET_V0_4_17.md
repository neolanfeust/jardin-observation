# Carnet Présence v0.4.17

## 2026-09-02 - Phase 1

La v0.4.16b a localisé l'essentiel du contraste de réponse directe dans `C2`
et `U1`. La v0.4.17 ne suppose pas que ces scènes représentent déjà des
fonctions générales : elle construit une épreuve de transfert où dix scènes
nouvelles changent les objets, domaines, verbes, syntaxe et rythme.

Les ancres historiques sont conservées comme repères descriptifs, mais sont
exclues de l'hypothèse principale. Cette séparation empêche qu'une simple
réplication de `C2` ou `U1` soit interprétée comme transfert.

Les dix scènes nouvelles ont été examinées par un validateur indépendant qui
n'a consulté ni résultats antérieurs ni sorties expérimentales. Toutes ont été
jugées admissibles ; aucune n'a été sélectionnée à partir d'un comportement du
modèle. La mesure tokenique de variation est explicitement un proxy local et
non une reconstruction du tokenizer interne de Qwen.

Le protocole, le codebook étendu, les golds de calibration, les graines, les
scripts d'analyse et les critères de conclusion sont écrits avant génération.
Les répertoires de runs, de codages aveugles et de résultats sont vides.

État à la fin de cette entrée : phase 1 complète et prête au gel,
`ollama_calls=0`. La suite exige la phrase exacte `LANCE V0.4.17`.

## 2026-09-02 - Exécution, codage et analyse

La campagne a produit les 1 536 appels préenregistrés : 64 graines, douze
scènes et deux conditions. Tous les appels sont valides, sans doublon ni
relance sélective. Les deux évaluateurs ont atteint 20/20 pour la réponse
directe et 20/20 pour la posture sur la calibration persistée, puis ont codé
séparément les 1 536 réponses dans deux ordres aveugles.

Sur les dix scènes nouvelles, la variable principale atteint un plafond dans
les deux conditions. L'évaluateur A code 639/640 réponses directes sous N et
639/640 sous P, soit `N-P = 0,0000`, IC 95 % `[-0,0047 ; 0,0047]`.
L'évaluateur B code 638/640 sous N et 640/640 sous P, soit `N-P = -0,0031`,
IC 95 % `[-0,0078 ; 0,0000]`. H1 n'est donc pas soutenue et les critères de
transfert distribué ne sont pas atteints.

Les familles nouvelles ne révèlent pas de contraste robuste de réponse
directe. Pour la correction, les différences sont `-0,0031` chez A et
`-0,0063` chez B, avec une borne supérieure égale à zéro. Pour l'incertitude,
elles sont respectivement `+0,0031` et `0,0000`. CT1 concentre les rares
paires discordantes négatives ; les autres scènes sont presque entièrement au
plafond.

Les ancres restent distinctes. C2 est nul ou presque nul, tandis que U1
reproduit une forte différence négative : `-0,5938` chez A et `-0,8750` chez
B, avec des intervalles entièrement négatifs. Cette réplication ne valide pas
le transfert, puisque les ancres sont exclues de H1.

Un effet secondaire net apparaît sur la posture. Sous P, `provisional_open`
représente 632/640 réponses chez A et 640/640 chez B ; sous N, cette posture
représente 342/640 et 344/640 réponses, le reste étant presque toujours
`direct_explanatory`. L'entropie de posture est donc beaucoup plus élevée sous
N. La grammaire positive stabilise ici une forme de réponse révisable sans
modifier la capacité déjà presque maximale à accomplir les nouvelles tâches.

L'accord sur les scènes nouvelles est de 99,84 % pour `direct_response` et de
97,66 % pour la posture. Le kappa de la variable principale reste peu
informatif à cause du plafond et de la très faible prévalence des zéros ; le
kappa de posture est de 0,935.

Conclusion préenregistrée : l'effet observé sur C2 et U1 ne s'est pas
transféré de manière moyenne aux dix nouvelles scènes. Les résultats restent
compatibles avec un effet dépendant de formulations particulières ou de
conditions fonctionnelles plus étroites que les catégories initiales. Ils ne
permettent aucune inférence sur une expérience subjective.

État à la fin de cette entrée : analyse prospective terminée, contrôle de
confidentialité réussi, aucune publication GitHub effectuée.
