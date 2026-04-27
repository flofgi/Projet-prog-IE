from __future__ import annotations
from typing import TYPE_CHECKING

from Item.Item import Item


if TYPE_CHECKING:
    from WorldElement.Ally import Ally
    from Map import Map
    from Camera import Camera
    
    from WorldElement.WorldElement import WorldElement


from WorldElement.Entity import Entity
from Inventory import Inventory
from Item.Sword import sword
from Item.Item import Item
from utilitary import RECUP_EVENT, ALLY_EVENT, vec_to_list
from assets.keys_dictionary import KEYS, MOUSE

import pygame




DEFAULT_NAME = " "
DEFAULT_SHOT_DISTANCE = 20
DEFAULT_SHOT_ANGLE = 100
DEFAULT_DAMAGE = 1
ZERO_VELOCITY = pygame.Vector2(0, 0)
HALF_ANGLE_DIVISOR = 2


class Player(Entity):
    """Class for player entity.

    This class extends Entity with player-specific systems such as ally
    management and inventory handling. It also handles keyboard-driven
    movement updates during gameplay.

    Attributes:
        hp (int): The entity's health points. When this reaches zero, the entity dies.
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2): Position of the entity.
        rect (pygame.Rect): Collision zone of the entity.
        velocity (pygame.Vector2): Movement vector of the entity.
        name (str): Name of the entity.
        allies (list[Ally]): List of allies currently linked to the player.
        held_item (int): Index or identifier of the currently selected inventory item.
        inventory (list): List of items owned by the player.
    """

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, name: str = DEFAULT_NAME) -> None:
        """Initialize a player with allies and inventory state.
        
        Args:
            hp (int): Initial health points for the player. Must be a positive integer.
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
            coordinates (pygame.Vector2): The initial position of the player.
            allies (list[Ally], optional): List of allies to initialize with. Defaults to None.
            inventory (dict, optional): List of items to initialize the inventory with. Defaults to None.
        """
        super().__init__(hp, sprites, coordinates, name)
        self.shot_distance = DEFAULT_SHOT_DISTANCE
        self.shot_angle = DEFAULT_SHOT_ANGLE
        self.damage = DEFAULT_DAMAGE

        
    def combat(self):
        pass
    
    def interact(self, target: "Entity") -> bool:
        return False

    def open_inventory(self):
        """transition into the inventory scene"""
        self.inventory.open_inventory()

    def close_inventory(self):
        """transition out of the inventory scene"""
        self.inventory.close_inventory()

    def drop(self, item: Item):
        """The item drops in the sector at the exact spot where the player is located
        Args:
            item (Item): The item to be dropped from the inventory.
        """
        self.inventory.remove_item(item)

    def add_ally(self, new_ally: Ally):
        """add new ally to Player base
        Args:
            new_ally (Ally): The ally to be added to the player's list of allies."""
        if new_ally not in self.allies:
            self.allies.append(new_ally)

    def update(self, dt: float, map: Map, target: "Player" = None):
        """Update player movement from keyboard input and update allies.
        Args:
            dt (float): Time delta since last update, used for timing animations and movements."""
        self.animation_timer += dt
        
        keys = pygame.key.get_pressed()

        self.handle_keys(keys)
        self.move(dt)

        for ally in self.allies:
            ally.update(dt, self)

        if self.inventory.held_item is not None:
            self.inventory.held_item.update(dt, map, self)
        else:
            self.hand.update(dt, map, self)

    def handle_events(self, event: pygame.event.Event):
        """Check for player-specific events such as item pickup or ally interaction.
        Args:
            events (pygame.event.Event):events to process for interactions.
        """
        if event.type == ALLY_EVENT:
            self.add_ally(event.dict["target"])
        if event.type == RECUP_EVENT:
            self.add_Item(event.dict["target"])
            event.dict["target"].inventory_add()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key :
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE["use_item"]:
                if self.inventory.held_item is None:
                    self.hand.use(self, self.map)
                else:
                    self.inventory.use_held_item(self, self.map)
            

    def handle_keys(self, keys):
        """Calculate the player's velocity based on keyboard input.
        This method sets the velocity vector based on directional keys and normalizes it to max_speed.
        Args:
            keys (list[bool]): The current state of all keyboard keys, as returned by pygame.key.get_pressed().
        """
        direction_x = keys[KEYS["move_right"]] - keys[KEYS["move_left"]]
        direction_y = keys[KEYS["move_down"]] - keys[KEYS["move_up"]]
        self.velocity = pygame.Vector2(direction_x, direction_y)
    
        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * self.max_speed
        else:
            self.velocity = ZERO_VELOCITY.copy()

    def is_ally(self, ally: Ally):
        """check if an ally is a player's ally
        
        Args:
            ally (Ally): The ally to check for being an ally of the player.
        
        Returns:
            bool: True if the ally is in the player's list of allies, False otherwise.
        """
        return ally in self.allies
    
    def add_Item(self, item: Item) -> bool:
        """add an item to the player's inventory.
        Args:
            item (Item): The item to be added to the player's inventory.
        
        Returns:
            bool: True if the item was successfully added to the inventory, False otherwise.
        """
        if item is not None:
            if self.inventory.add_item(item):
                return True
        return False

    def load(self,map: Map , camera: Camera, allies: list[Ally] = None, inventory = None, name: str = DEFAULT_NAME):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.

        Args:
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
        """
        self.map = map
        self.camera = camera
        self.allies: list["Ally"] = list(allies) if allies is not None else []
        self.inventory: Inventory = Inventory(dict(inventory)) if inventory is not None else Inventory({})

        super().load()
        self.hand = sword.hand()

        
        for ally in self.allies:
            ally.load()
        
        if self.inventory.held_item is not None:
            self.inventory.held_item.load()
        
        self.inventory.load()
    
    def load_new_map(self, new_map: Map, new_camera: Camera, coordinates: pygame.Vector2):
        """Update the player's map reference when transitioning to a new map."""
        self.map = new_map
        self.camera = new_camera
        self.coordinates = coordinates

    def save(self, map_name: str, data: dict | None = None) -> dict:
        data = super().save(map_name, data)
        data.update(
            {
                "shot_distance": self.shot_distance,
                "shot_angle": self.shot_angle,
                "damage": self.damage,
                "allies": [ally.save(map_name) for ally in self.allies],
                "inventory": self.inventory.save(map_name),
                f"{map_name}": {
                    "coordinates": vec_to_list(self.coordinates)
                }
            }
        )
        return data

    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> "Player":
        """Create a Player instance from saved data.
        
        Args:
            data (dict): A dictionary containing the player's saved state, including allies and inventory.
            map_name (str, optional): The name of the map to load coordinates for. Defaults to None.
        """
        player: Player = super().load_from_data(data, map_name)

        player.shot_distance = data.get("shot_distance", DEFAULT_SHOT_DISTANCE)
        player.shot_angle = data.get("shot_angle", DEFAULT_SHOT_ANGLE)
        player.damage = data.get("damage", DEFAULT_DAMAGE)

        allies_data = data.get("allies", [])
        player.allies = [Ally.load_from_data(ally_data, map_name) for ally_data in allies_data]

        inventory_data = data.get("inventory", {})
        player.inventory = Inventory.load_from_data(inventory_data)

        return player
    
    def load_map(self, map: Map, camera: Camera, player_data: dict):
        """Load a new map and update the player's position accordingly."""
        self.map = map
        self.camera = camera
        map = player_data.get(self.map.name, {})
        if map == {}:
            self.coordinates = self.map.spawn_point.copy()
        else:
            self.coordinates = list_to_vec(map.get("coordinates", vec_to_list(self.map.spawn_point)))

    @property
    def get_allies(self) -> list[Ally]:
        return self.allies

    
    def in_cone(self, target: pygame.Vector2 | WorldElement):
        """Check if a target is within the sword's attack cone."""
        mouse = pygame.Vector2(pygame.mouse.get_pos()) + self.camera.get_coordinates
        if isinstance(target, WorldElement):
            target = target.get_coordinates
        position = self.get_coordinates

        normalised_target = target + pygame.Vector2(self.camera.x, self.camera.y) - position
        mouse_target_angle = normalised_target.angle_to(mouse - position)
        return abs(mouse_target_angle) < self.shot_angle/2 and target.distance_to(position) < self.shot_distance


    def draw(self, surface: pygame.Surface, camera: Camera, player = None):
        frame = self.sprite[self.current_frame]
        draw_pos = pygame.Vector2(self.rect.topleft) - self.hitbox_offset - camera.get_coordinates
        surface.blit(frame, draw_pos)
        if self.inventory.held_item is not None:
            self.inventory.held_item.draw_equip(surface, camera, player)
        else:
            self.hand.draw_equip(surface, camera, player)
        


