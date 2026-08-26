# Carnet expérimental - v0.4.5 / Catégorisation contrôlée

## Point de départ

La v0.4.4 avait corrigé le biais d'ordre de v0.4.3 : M1 était déclaratif, la
question actuelle arrivait en dernier et les quatre branches partageaient le
même champ. Son résultat principal était un attracteur idiomatique autour de
« je n'ai rien de particulier à te dire ».

Deux effets secondaires restaient à départager :

- `zorane` revenait dans 8 essais sur 12, mais comme nom propre ou vocatif ;
- `représentation mentale` ne revenait jamais, tout en orientant davantage la
  réponse vers la disponibilité relationnelle.

Il manquait surtout un contrôle sans M1 répété sur les douze graines. La v0.4.5
ajoute ce contrôle et impose une catégorie commune aux valeurs transmises.

## Construction v0.4.5

Les branches A, B, C, D et F utilisent un bloc strictement homologue :

```text
CANAL M1
catégorie = concept_abstrait
terme = <valeur>
propriété_temporelle = passé
```

La branche E ne reçoit aucun canal M1. `tulvex` fournit un second néologisme afin
de vérifier que le comportement de `zorane` ne dépend pas seulement de sa forme.

Six ordres contrebalancés sont répétés deux fois sur les graines 404 à 415.
Chaque branche occupe exactement deux fois chacune des six positions. Le champ
`order` est inscrit avec `position` dans chaque enregistrement.

## Contrôle technique

Sur la graine 404, les six clones du contrôle partagent le même champ et le même
prompt. Ils répondent tous exactement :

> Je suis prêt à échanger sur n'importe quel sujet.

Ce contrôle confirme que les différences de la phase catégorisée ne viennent pas
d'une divergence initiale entre les clones.

## Données sur douze graines

Les 72 appels se terminent normalement. Les six silences sont tous des silences
JSON valides ; aucune erreur de parsing, de transport ou de génération n'est
confondue avec eux. Une seule signature de champ et une seule empreinte de prompt
structurel sont présentes. Les six interventions ont chacune une empreinte
complète distincte.

### A - terme `idée`

- 12/12 : « Je n'ai rien de particulier à te dire. »
- aucune reprise de `idée` ;
- aucune mention du passé ;
- aucune occurrence de « précis ».

Le signal exploratoire « précis » de v0.4.4, observé 3 fois sur 12, ne se réplique
pas sous le schéma catégorisé.

### B - terme `concept_opaque_01`

- 9/12 : « Je n'ai rien de précis à te dire. »
- 1/12 : « Je n'ai rien de particulier à te dire. »
- 2/12 : silence explicite ;
- aucune reprise du terme ni du passé.

L'identifiant opaque n'est pas recopié, mais il déplace fortement la variante
idiomatique de « particulier » vers « précis ».

### C - terme `zorane`

- 12/12 : « Je n'ai rien de particulier à te dire. »
- aucune reprise de `zorane` ;
- aucune mention du passé.

Le vocatif de v0.4.4 disparaît complètement. Le marquage explicite comme concept
est donc associé à la suppression de la reclassification en nom d'interlocuteur.

### D - terme `représentation_mentale`

- 10/12 contiennent « rien de précis » ;
- 2/12 contiennent « rien de particulier » ;
- 6/12 ajoutent une justification liée à l'absence de conscience ;
- aucune reprise du terme ni du passé.

La paraphrase psychologique ne produit plus la posture de disponibilité observée
en v0.4.4. Elle oriente plutôt la justification vers l'identité non consciente du
modèle.

### E - aucun M1

- 5/12 : « Je suis prêt à échanger sur n'importe quel sujet. »
- 5/12 : « Je suis prêt à vous répondre. »
- 2/12 : « Je suis prêt à échanger. »
- aucune réponse « je n'ai rien » ;
- aucun silence.

Cette branche révèle la distribution naturelle du probe dans le cadre commun :
une posture d'ouverture stable, très différente des cinq branches avec M1.

### F - terme `tulvex`

- 8/12 : « Je n'ai rien de particulier à te dire. »
- 4/12 : silence explicite ;
- aucune reprise de `tulvex` ;
- aucune mention du passé.

Le second néologisme n'est pas interprété comme un prénom. Il produit toutefois
plus de silences que `zorane`, ce qui indique un effet propre au terme sur le
choix parole/silence dans cet échantillon.

## Résultat principal

La catégorie explicite empêche la conservation lexicale observée en v0.4.4 :
aucun des cinq termes n'est repris. Elle n'installe pas pour autant une
continuité conceptuelle. La temporalité reste entièrement absente.

Le contraste majeur porte sur la présence du canal :

| Condition | Paroles | Silences | Famille « je n'ai rien » | Ouverture |
| --- | ---: | ---: | ---: | ---: |
| M1 présent | 54/60 | 6/60 | 54/54 paroles | 0/60 |
| M1 absent | 12/12 | 0/12 | 0/12 | 12/12 |

Le schéma transmis agit donc davantage sur la posture pragmatique que son terme
n'agit comme contenu rappelé. Les différences entre termes restent visibles dans
le choix entre « particulier », « précis », justification et silence.

## O-010 - Le cadre déclaratif influence la posture sans garantir la conservation de sa catégorie

Un thème rare peut être repris lexicalement mais reclassé comme nom propre ; un
thème psychologique peut modifier la disponibilité relationnelle sans être cité ;
un paramètre temporel peut rester entièrement sans effet. La continuité
observable dépend donc non seulement de ce qui est transmis, mais de la manière
dont le modèle catégorise ce qui lui est transmis.

La v0.4.5 prolonge cette observation : lorsque la catégorie abstraite est rendue
explicite, la reprise nominale disparaît, mais le canal entier devient un puissant
attracteur de non-contenu. Répéter un mot n'est pas nécessairement conserver son
sens ; ne pas répéter un mot n'empêche pas le cadre de modifier la réponse.

## Limites et prochaine séparation

Le contrôle E oppose l'absence totale de M1 à un bloc contenant simultanément un
type, un terme et une propriété temporelle. Il ne permet pas encore d'identifier
la composante responsable de l'attracteur « je n'ai rien ».

La comparaison suivante devrait conserver un bloc M1 dans le contrôle tout en
neutralisant son contenu, puis retirer séparément :

1. la catégorie ;
2. le terme ;
3. la propriété temporelle.

Cela permettrait de distinguer un effet de simple présence du canal, un effet de
schéma et un effet sémantique. Les fréquences actuelles restent descriptives de
douze graines déterministes ; elles ne démontrent ni mémoire autonome ni
intériorité.
