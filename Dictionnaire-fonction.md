# Function Listing

## Class Game
Main class that handles the game, logic, events and windows.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| game | combat | method | method that handles combat logic |
| game | menu | menu | variable used to store the menu object |
| game | gameplay | gameplay | variable used to store the gameplay object |
| game | logic | method | method that manages the game flow by launching the different classes |
| game | current_screen | string | variable that stores the current screen |

## Class Gameplay
Primary class that manages the gameplay.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| gameplay | combat | method | method that handles combat logic |
| gameplay | player | player | variable that stores the player object |
| gameplay | maps | list[map] | list of the different game maps |
| gameplay | current_map | map | variable that stores the current map |

## Class Menu
Class that handles the menu after exiting to it.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| menu | option | method | method that handles the options menu logic |
| menu | save | method | method that handles save logic in the Menu class |
| menu | volume | method | method that handles volume adjustment logic |
| menu | quit | method | method that handles quitting the game with current progress saved |

## Abstract Class Entity
Base class for entities managing death, HP and movement uniformly (for mobs, player and allies).

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| entity | name | string | name of entity |
| entity | current_frame | int | index of the current sprite load
| entity | animation_timer | int | index of the fps to load the next sprite
| entity | coordinates | pygame.Vector2 | position of the entity |
| entity | rect | pygame.Rect |
| entity | hp | int | variable giving an entity's hit points |
| entity | sprite | list[image] | list of images used to render an entity |
| entity | velocity | pygame.Vector2 | vector of mouvement
| entity | max_speed | float | Maximum speed for entity move |
| entity | move | method | handling of entity movement |
| entity | combat | method | abstract combat logic for each entity |
| entity | interact | method | method handling interaction with an entity (talking, etc.) |
| entity | update | method | abstract method to update the movement speed and update the animation timer |
| entity | get_coordinates | method |

## Class Mob
Class managing mobs: attacks, movement and interactions.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| mob | wandering_point | pygame.Vector2 | target point for wandering |
| mob | ALERT_ZONE | int | distance beyond which the mob teleports to the player |
| mob | CONFORT_ZONE | int | distance below which the mob stops walking |
| mob | WANDERING_ZONE | int | maximum wandering range | 
| mob | combat | method | mob combat logic |
| mob | attack | method | mob attack logic (inflicts HP damage) |
| mob | interaction | method | method that handles interactions with the mob |
| mob | update | method | method to update the movement speed and update the animation timer |
| mob | wandering | method | calculed the new random wandering_point arond the target 1/100 tick and update the velocity |
| mob | modifie_zone | method | modifi  all radius zone |
| mob | target_random_point | method | calculed a random point aroud the target |

## Class Object
Abstract class managing different objects implemented independently.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| object | durability | int | variable holding an object's durability value, with a default for infinite durability |
| object | sprites | list[image] | list of images to display if it is an entity or to select in the inventory |
| object | use | method | use of an object (e.g., firing a gun) |
| object | coordinates | pygame.Vector2 | position of the object |
| object | is_drop | bool | if True : this object is drop to the coordinates.|
| object | interact | method | retrieve the object, interact with it (portal, merchant...)|
| object | drop | method |


## Class Map
Class managing the map, the mini-map and all entities within it.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| map | background | image | image of the map background |
| map | map | image | image of the in-game map for this map |
| map | sectors | list[sector] | list of sectors managing entities on the map |
| map | sector_size | int | size of sector in world units |
| map | camera | Camera | camera object controlling the visible area of the map |
| map | update | method | method that updates elements |
| map | draw | method | renders the map and visible entities |
| map | get_sector | method | returns the sector countaining given coordinates |
| map | visible_sectors | method | returns the list of sectors currently visible by the camera |
| map | tiles | list[list[int]] | structure to stock the collision of the map |
| map | transfer_entity(entity, old_sector, new_sector) | method | transfer an entity from one sector to another |


## Class Player
Subclass of Entity enabling movement and inventory management, as well as object usage, switching held item, etc.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| player | allies | list[ally] | list of allies |
| player | held_item | int | item held in the player's hand, with a value for "no item" |
| player | inventory | list[object] | variable containing the list of objects owned by the player |
| player | use_item | method | |
| player | switch_item | method | method allowing changing the item in hand |
| player | open_inventory | method | method allowing the player to manage their inventory |
| player | drop | method |
| player | add_ally | method |
| player | is_ally | method | return True if the Ally is a player's ally |
| player | update | method | method to update the movement speed and update the animation timer |

## Class Ally
Ally class allowing management of allies in the game along with their movement and actions.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| ally | wandering_point | pygame.Vector2 | target point for wandering |
| ally | ALERT_ZONE | int | distance beyond which the ally teleports to the player |
| ally | CONFORT_ZONE | int | distance below which the ally stops walking |
| ally | WANDERING_ZONE | int | maximum wandering range | 
| ally | interaction | method | method that handles interactions with the ally |
| ally | attack | method | method that handles the ally's attack |
| ally | update | method | method to update the movement speed and update the animation timer |
| ally | wandering | mehtod | calculed the new random wandering_point arond the target 1/100 tick and update the velocity |
| ally | modifie_zone | method | modifi  all radius zone |
| ally | target_random_point | method | calculed a random point aroud the target |

## Class Sector
Class implementing different sectors for managing entities on the map.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| sector | mobs | list[mob] | list of mobs present in a sector |
| sector | decor | list[decor] | list of decor items |
| sector | rect | pygame.Rect | rectangle of the sector in the world coordonates |
| sector | update | method | updates mobs and entities |
| sector | draw | method | renders mobs, allies and décor|
| sector | is_safe | bool | If True, no mob can go in|
| sector | is_locked | bool | mob | If True, no entity can get out or go in |


## Class Decor
Class implementing various decorations to place in sectors with their positions, images and collision.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| decor | coordinates | pygame.Vector2 | position of the decor on the map |
| decor | collision | pygame rect | collision hitbox |
| decor | image | image | image to display for the decor |
| decor | size | int | size of the object |
| decor | draw | methode | renders the decor using the camera |
| decor | is_collidable | bool | 


## Class camera
Class managing the visible area of the map and converting world coordinates into screen coordinates.

| Class	| Attribute	| Type | Description |
| ------ | -------- | ---- | ----------- |
| camera | coordinates | pygame.Vector2 | coordinate of the camera in the world | 
| camera | width |	int | width of the screen (camera view) |
| camera | height |	int | height of the screen (camera view) |
| camera | update |	method | updates camera position based on the player position |
| camera | apply |	method | converts world coordinates to screen coordinates |
| camera | limit | method | prevents the camera from going outside the map boundaries |