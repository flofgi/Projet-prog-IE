# Listing des fonctions

## Classe jeu
classe principale qui gère le jeu, la logique, les événements et les fenêtres
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| jeu | combat | fonction | fonction qui gère la logique de combat |
| jeu | menu | menu | variable permettant de stocker le fonctionnement du menu |
| jeu | menu | gameplay | variable permettant de stocker le fonctionnement du gameplay |
| jeu | logique | fonction | fonction qui permet de gerer le fonctionnement du jeu en lancant les differentes classes |

## Classe gameplay
classe principale qui gère le gameplay
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| gameplay | combat | fonction | fonction qui gère la logique de combat |
| gameplay | joueur | joueur | variable qui stocke le joueur |
| gameplay | maps | list[map] | liste des différentes maps du jeu |

## Classe du menu
classe qui permet la gestion du menu après une sortie
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| menu | option | fonction | fonction qui gère la logique du menu option dans la classe Menu |
| menu | sauvegarde | fonction | fonction qui gère la logique de la sauvegarde du jeu dans la classe Menu |
| menu | volume | fonction | fonction qui gère la logique du réglage du volume |
| menu | quitter | fonction | fonction qui gère la logique d'arrêt du jeu avec la sauvegarde de la partie en cours |

## Classe abstraite entité
classe mère des entités gérant de manière unifiée la mort, les PV et les déplacements (pour mobs, joueur et alliés)
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| entité | déplacement | fonction | gestion des déplacements de manière abstraite pour les entités |
| entité | combat | fonction | fonction qui gère de manière abstraite la partie combat pour chaque entité |
| entité | pv | entier | variable donnant un nombre de PV à une entité |
| entité | sprite | list[image] | liste des images utilisées pour le rendu d'une entité |
| entité | interagir | fonction | fonction gérant le fait d'interagir avec une entité (parler …) |
| entité | coordonnées | list[x, y] | position de l'entité |

## Classe mob
classe assurant la gestion des mobs : attaque et déplacement ainsi que les interactions
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| mob | déplacement | fonction | logique de déplacement des mobs |
| mob | combat | fonction | logique du combat des mobs |
| mob | attaque | fonction | logique des attaques des mobs (inflige des PV) |

## Classe objet
classe abstraite gérant les différents objets
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| objet | durabilité | entier | variable gardant la valeur de la durabilité d'un objet avec une valeur par défaut pour les durabilités infinies |
| objet | forme | list | liste des images à afficher si c'est une entité ou sélectionnées dans l'inventaire |
| objet | utilisation | fonction | utilisation d'un objet (ex : tir avec le fusil) |

## Classe map
classe de gestion de la map ainsi que de la carte et de toutes les entités incluses dedans
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| map | fond | image | image du fond de la map |
| map | carte | image | image de la carte du jeu pour cette map |
| map | secteur | list[secteur] | liste des secteurs de gestion des entités de la map |
| map | update | fonction | fonction qui met à jour les éléments |

## Classe joueur
classe fille de l'entité permettant la mise en mouvement et la gestion de l'inventaire du joueur ainsi que la gestion de l'utilisation des objets, le changement de main …
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| joueur | déplacement | fonction | fonction qui gère la logique de déplacement du joueur |
| joueur | inventaire | list[objet] | variable contenant la liste des objets qui appartiennent au joueur |
| joueur | objet en main | entier | objet tenu en main par le joueur avec valeur pour « rien en main » |
| joueur | utilisation objet | fonction |
| joueur | changer de main | fonction | fonction permettant de changer l'objet dans la main |
| joueur | alliés | list[allié] | liste des alliés |
| joueur | ouverture inventaire | fonction | fonction permettant au joueur de gérer son inventaire |

## Classe allié
classe allié permettant la gestion des alliés dans le jeu ainsi que leur déplacement et leurs actions
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| allié | interaction | fonction | fonction qui gère les interactions avec lui et les alliés |
| allié | déplacement | fonction | fonction qui gère le déplacement des alliés |
| allié | attaque | fonction | fonction qui gère l'attaque de l'allié |

## Classe secteur
classe implémentant les différents secteurs de gestion des entités sur la carte
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| secteur | mob | list[mob] | liste des mobs présents sur un secteur |
| secteur | décor | list[décor] | liste de décors |

## Classe décor
classe implémentant les différents décors à placer dans les secteurs avec leurs positions, leurs images, leur collision
| Classe                | Attribut | Type | Description |
| -------------------- | ------ |------------|------------|
| décor | coordonnées | list[x, y] | position du décor dans la map |
| décor | collision | rect pygame |
| décor | image | image | image à afficher pour le décor |
| décor | taille | int | taille de l'objet |