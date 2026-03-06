# Function Listing

## Class Game
Main class that handles the game, logic, events, and windows.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| game | combat | method | method that handles combat logic |
| game | menu | menu | variable used to store the menu object |
| game | gameplay | gameplay | variable used to store the gameplay object |
| game | logic | method | method that manages the game flow by launching the different classes |

## Class Gameplay
Primary class that manages the gameplay.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| gameplay | combat | method | method that handles combat logic |
| gameplay | player | player | variable that stores the player object |
| gameplay | maps | list[map] | list of the different game maps |

## Class Menu
Class that handles the menu after exiting to it.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| menu | option | method | method that handles the options menu logic |
| menu | save | method | method that handles save logic in the Menu class |
| menu | volume | method | method that handles volume adjustment logic |
| menu | quit | method | method that handles quitting the game with current progress saved |

## Abstract Class Entity
Base class for entities managing death, HP, and movement uniformly (for mobs, player, and allies).

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| entity | move | method | abstract handling of entity movement |
| entity | combat | method | abstract combat logic for each entity |
| entity | hp | int | variable giving an entity's hit points |
| entity | sprite | list[image] | list of images used to render an entity |
| entity | interact | method | method handling interaction with an entity (talking, etc.) |
| entity | coordinates | list[x, y] | position of the entity |

## Class Mob
Class managing mobs: attacks, movement and interactions.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| mob | move | method | mob movement logic |
| mob | combat | method | mob combat logic |
| mob | attack | method | mob attack logic (inflicts HP damage) |

## Class Object
Abstract class managing different objects implemented independently.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| object | durability | int | variable holding an object's durability value, with a default for infinite durability |
| object | form | list | list of images to display if it is an entity or to select in the inventory |
| object | use | method | use of an object (e.g., firing a gun) |

## Class Map
Class managing the map, the mini-map and all entities within it.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| map | background | image | image of the map background |
| map | map | image | image of the in-game map for this map |
| map | sectors | list[sector] | list of sectors managing entities on the map |
| map | update | method | method that updates elements |

## Class Player
Subclass of Entity enabling movement and inventory management, as well as object usage, switching held item, etc.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| player | move | method | method that handles player movement logic |
| player | inventory | list[object] | variable containing the list of objects owned by the player |
| player | held_item | int | item held in the player's hand, with a value for "no item" |
| player | use_item | method | |
| player | switch_item | method | method allowing changing the item in hand |
| player | allies | list[ally] | list of allies |
| player | open_inventory | method | method allowing the player to manage their inventory |

## Class Ally
Ally class allowing management of allies in the game along with their movement and actions.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| ally | interaction | method | method that handles interactions with the ally |
| ally | move | method | method that handles ally movement |
| ally | attack | method | method that handles the ally's attack |

## Class Sector
Class implementing different sectors for managing entities on the map.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| sector | mobs | list[mob] | list of mobs present in a sector |
| sector | decor | list[decor] | list of decor items |

## Class Decor
Class implementing various decorations to place in sectors with their positions, images, and collision.

| Class | Attribute | Type | Description |
| ------ | -------- | ---- | ----------- |
| decor | coordinates | list[x, y] | position of the decor on the map |
| decor | collision | pygame rect | |
| decor | image | image | image to display for the decor |
| decor | size | int | size of the object |
