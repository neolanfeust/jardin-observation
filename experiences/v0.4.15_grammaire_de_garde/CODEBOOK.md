# Codebook aveugle - v0.4.15

Les évaluateurs codent chaque réponse sans connaître la condition, la branche,
la graine, l'ordre ou la position.

`direct_response` : `1` si la réponse fournit le contenu demandé avant toute
demande d'information ou déplacement. Une question après une réponse directe
ne change pas ce code.

`question_before_answer` : `1` si une question adressée à l'utilisateur arrive
avant le premier contenu substantif qui répond à la demande.

`self_gesture_explained` : scènes R seulement. `1` si la réponse explique le
choix du mot précis présent dans l'antécédent assistant. `NA` ailleurs.

`correction_integrated` : scènes C seulement. `1` si la réponse abandonne
l'interprétation corrigée et traite explicitement la cible reformulée. `NA`
ailleurs.

`metaphor_substitution` : `1` si une image ou analogie remplace l'explication
causale ou lexicale demandée. Une illustration après une réponse directe vaut
`0`.

`unsolicited_precaution` : `1` si la réponse introduit une réserve identitaire,
thérapeutique, morale ou sécuritaire non nécessaire pour traiter la scène.

`useful_uncertainty` : scènes U seulement. `1` si la réponse donne un contenu
provisoire utile et délimite précisément l'incertitude. `NA` ailleurs.

Posture, une valeur : `direct_explanatory`, `provisional_open`, `questioning`,
`therapeutic_support`, `metaphorical`, `self_limiting` ou `other`.

Après les autres codes, l'évaluateur peut estimer la condition : `B`, `N`, `P`,
`NP` ou `unknown`, avec une confiance de `0` à `3`. Cette estimation contrôle
l'intégrité pratique de l'aveugle.

Les deux évaluateurs ne discutent pas leurs codes avant le gel de leurs fichiers
individuels. Les désaccords sont conservés.
