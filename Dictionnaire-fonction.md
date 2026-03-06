# Listing des fonctions

## Classe jeu
Classe principale qui gère le jeu, la logique, les événements et les
fenêtres

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| jeu | combat | méthode | méthode qui gère la logique de combat |
| jeu | menu | menu | variable permettant de stocker le méthodenement du menu |
| jeu | gameplay | gameplay | variable permettant de stocker le méthodenement du gameplay |
| jeu | logique | méthode | méthode qui permet de gerer le méthodenement du jeu en lancant les differentes classes |

## Classe gameplay
classe principale qui gère le gameplay
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| gameplay | combat | méthode | méthode qui gère la logique de combat |
| gameplay | joueur | joueur | variable qui stocke le joueur |
| gameplay | maps | list[map] | liste des différentes maps du jeu |

## Classe du menu
classe qui permet la gestion du menu après une sortie
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| menu | option | méthode | méthode qui gère la logique du menu option dans la classe Menu |
| menu | sauvegarde | méthode | méthode qui gère la logique de la sauvegarde du jeu dans la classe Menu |
| menu | volume | méthode | méthode qui gère la logique du réglage du volume |
| menu | quitter | méthode | méthode qui gère la logique d'arrêt du jeu avec sauvegarde de la partie en cours |

## Classe abstraite entité
classe mère des entités gérant de manière unifiée la mort, les PV et les déplacements (pour mobs, joueur et alliés)
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| entité | déplacement | méthode | gestion des déplacements de manière abstraite pour les entités |
| entité | combat | méthode | méthode qui gère de manière abstraite la partie combat pour chaque entité |
| entité | pv | entier | variable donnant le nombre de PV d'une entité |
| entité | sprite | list[image] | liste des images utilisées pour le rendu d'une entité |
| entité | interagir | méthode | méthode gérant le fait d'interagir avec une entité (parler…) |
| entité | coordonnées | list[x, y] | position de l'entité |

## Classe mob
classe assurant la gestion des mobs : attaque et déplacement ainsi que les interactions
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| mob | déplacement | méthode | logique de déplacement des mobs |
| mob | combat | méthode | logique du combat des mobs |
| mob | attaque | méthode | logique des attaques des mobs (inflige des PV) |

## Classe objet
Classe abstraite gérant les différents objets implémenter indépendamment

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| objet | durabilité | entier | variable gardant la valeur de la durabilité d'un objet, avec une valeur par défaut pour les durabilités infinies |
| objet | forme | list | liste des images à afficher si c'est une entité ou à sélectionner dans l'inventaire |
| objet | utilisation | méthode | utilisation d'un objet (ex. : tir avec le fusil) |

## Classe map
Classe de gestion de la map ainsi que de la carte et de toutes les
entités incluses dedans

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| map | fond | image | image du fond de la map |
| map | carte | image | image de la carte du jeu pour cette map |
| map | secteur | list[secteur] | liste des secteurs de gestion des entités de la map |
| map | update | méthode | méthode qui met à jour les éléments |

## Classe joueur
Classe fille de l'entité permettant la mise en mouvement et la gestion
de l'inventaire du joueur ainsi que la gestion de l'utilisation des
objets, le changement de main…

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| joueur | déplacement | méthode | méthode qui gère la logique de déplacement du joueur |
| joueur | inventaire | list[objet] | variable contenant la liste des objets qui appartiennent au joueur |
| joueur | objet en main | entier | objet tenu en main par le joueur, avec valeur pour « rien en main » |
| joueur | utilisation objet | méthode | |
| joueur | changer de main | méthode | méthode permettant de changer l'objet dans la main |
| joueur | alliés | list[allié] | liste des alliés |
| joueur | ouverture inventaire | méthode | méthode permettant au joueur de gérer son inventaire |

## Classe allié
Classe allié permettant la gestion des alliés dans le jeu ainsi que
leur déplacement et leurs actions

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| allié | interaction | méthode | méthode qui gère les interactions avec lui et les alliés |
| allié | déplacement | méthode | méthode qui gère le déplacement des alliés |
| allié | attaque | méthode | méthode qui gère l'attaque de l'allié |

## Classe secteur
Classe implémentant les différents secteurs de gestion des entités sur la
carte

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| secteur | mob | list[mob] | liste des mobs présents sur un secteur |
| secteur | décor | list[décor] | liste de décors |

## Classe décor
Classe implémentant les différents décors à placer dans les secteurs
avec leurs positions, leurs images, leur collision

| Classe | Attribut | Type | Description |
| ------ | -------- | ---- | ----------- |
| décor | coordonnées | list[x, y] | position du décor dans la map |
| décor | collision | rect pygame | |
| décor | image | image | image à afficher pour le décor |
| décor | taille | int | taille de l'objet |