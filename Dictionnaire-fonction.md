# Listing des fonctions

## Classe jeux
classe principal qui gère le jeux, la logique, les evenements et les fentres
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| jeux | combat | fonction | fonction qui gère la logique de combat |


## Classe du menu
classe qui permets la gestion du menu après un exit
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
|menu | option | fonction | Fonction qui gère le fonctionnement de la logique du menu option dans la classe menu |
| menu | sauvegarde | fonction | Fonction qui gère le fonctionnement de la logique de la sauvegarde du jeux dans la classe menu |
|menu | volume | fonction | fonction qui gère le fonctionnement de la logique du reglage du volume |
| menu | quitter | fonction | fonction qui gère le fonctionnement de la logique d'arret du jeux avec la sauvegarde de la partie en cour |


## Classe entité
Classe mère des entité gerant de manière unifié la mort, les pv et les déplacements
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| entité | déplacement | fonction | gestion des déplacement de manière abstraite pour les entités |
| entité | combat | fonction | fonction qui gère de manière abstraite la partie combat pour chaque entité |
| entité | pv | entier | variable donnant un nombre de pc à une entité |
| entité | sprite | list[image] | listes des images utilisé pour le rendu d'une entité |
| entité | interagir | fonction | fonction gérant le faite d'interagir avec une entité (parler ...) |

## Classe mob
classe assurant la gestion des mobs : attaque et déplacement ainsi que les interactions
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| mob | déplacement | fonction | logique de déplacement des mobs|
| mob | combat | fonction | logique du combat des mobs |
| mob | attaque | fonction | logique des attaques des mobs (inflige des pv) |

## Classe objet
classe abstraite gerant les differents objets
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| objet | durabilité | entier | variable gardant la valeur de la durabilité d'un objet avec une valeur par defaut pour les durabilités infini |
| objet | forme | list | listes des images à afficher si c'est une entité ou selectionner dans l'inventaire |
| objet | utilisation | fonction | utilisation d'un objet (ex : tir avec le fusil)

## Classe map
classe de gestion de la map ainsi que de la carte et de toutes les entitées inclues dedans
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| map | fond | image | image du fond de la map |
| map | carte | image | image de la carte du jeux pour cette map |
| map | secteur | list[secteur] | liste des secteur de gestions des entités de la map |




## Classe joueur
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|


## Classe amis
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|


## Classe secteur
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|