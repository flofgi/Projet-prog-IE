from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ally import Ally
    from Map import Map
    from Camera import Camera
    from Mob import Mob
    
    from WorldElement import WorldElement
from Entity import Entity

from Item import Item
from utilitary import RECUP_EVENT, ALLY_EVENT, STATE_POP, STATE_PUSH

from assets.keys_dictionary import KEYS

import pygame
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

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, camera:Camera, allies: list[Ally] = None, inventory = None) -> None:
        """Initialize a player with allies and inventory state.
        
        Args:
            hp (int): Initial health points for the player. Must be a positive integer.
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
            coordinates (pygame.Vector2): The initial position of the player.
            allies (list[Ally], optional): List of allies to initialize with. Defaults to None.
            inventory (dict, optional): List of items to initialize the inventory with. Defaults to None.
        """
        super().__init__(hp, sprites, coordinates, " ")
        self.allies: list["Ally"] = list(allies) if allies is not None else []
        self.inventory: Inventory = Inventory(dict(inventory)) if inventory is not None else Inventory({})
        self.camera = camera
        self.shot_distance = 20
        self.shot_angle = 100
        self.damage = 1
        self.max_speed = 10

        
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
            if event.button == 1:
                if self.inventory.held_item is not None:
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
            self.velocity = pygame.Vector2(0, 0)

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

    def load(self,map: Map ,sprites = None):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.

        Args:
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
        """
        self.map = map
        if sprites is not None:
            self.sprite_paths = list(sprites)
        super().load()


        
        for ally in self.allies:
            ally.load()
        
        if self.inventory.held_item is not None:
            self.inventory.held_item.load()
        
    @property
    def get_allies(self) -> list[Ally]:
        return self.allies

    


    def draw(self, surface: pygame.Surface, camera: Camera, player = None):
        frame = self.sprite[self.current_frame]
        draw_pos = self.get_coordinates - camera.get_coordinates
        surface.blit(frame, draw_pos)
        if self.inventory.held_item is not None:
            self.inventory.held_item.draw_equip(surface, camera, player)

        
class Inventory:
    """Class to manage the player's inventory, including item storage and usage.
    
    Attributes:
        items (list[Item]): The list of items in the inventory.
        held_item (int | None): The index of the item currently held, or None if no item is held.
    """

    def __init__(self, items: dict[Item, list[int]]):
        """Class to manage the player's inventory, including item storage and usage.
        
        Args:
            items (dict[Item: list[int]]): The initial list of items in the inventory
            the first int is for the number of item store and seconde is for the position in the inventory.
        """
        self.items: dict[Item, list[int]] = {item: [info[0], info[1]] for item, info in items.items()}
        self.max_slot = 15
        self.slot_size = 64
        self.margin = (9, 12)
        self.slot_margin = (11, 14)
        self.max_stack = 10
        self.COUNT_INDEX = 0
        self.SLOT_INDEX = 1

    def get_count(self, item: Item) -> int:
        return self.items[item][self.COUNT_INDEX]
    
    def set_count(self, item: Item, value: int) -> int:
         self.items[item][self.COUNT_INDEX] = value

    def get_slot(self, item: Item) -> int:
        return self.items[item][self.SLOT_INDEX]

    def set_slot(self, item: Item, slot: int) -> None:
        self.items[item][self.SLOT_INDEX] = slot

    def swap_slots(self, first: Item | None, second: Item | None) -> None:
        """Swap the inventory slots of two items. If one item is None, 
        it means that the other item is being moved to an empty slot."""
        if first is None and second is None:
            return
        elif first is None:
            first_slot = self.first_empty_slot
            second_slot = self.get_slot(second)
        elif second is None:
            first_slot = self.get_slot(first)
            second_slot = self.first_empty_slot
        else:
            first_slot = self.get_slot(first)
            second_slot = self.get_slot(second)
        self.set_slot(first, second_slot)
        self.set_slot(second, first_slot)

    def load(self):
        """Load sprites for all items in the inventory."""
        pass

    @property
    def number_slot(self) -> int:
        """Return the number of occupied slots in the inventory.
        Item can be stack by 10 objects, so the number of occupied slots is the sum of unique items in the inventory, not the total number of items.
        
        Returns:
            int: The number of occupied slots in the inventory.
        """
        return len(self.items)


    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory.
        
        Args:            
            item (Item): The item to be added to the inventory.
        Returns:
            bool: True if the item was successfully added to the inventory, False otherwise.
        
        """
        if (item in self.items and self.get_count(item) < self.max_stack) or self.first_empty_slot is not None:
            if item in self.items:
                if self.get_count(item) < self.max_stack:
                    self.items[item][self.COUNT_INDEX] += 1
            else:
                self.items[item] = [1, self.first_empty_slot]
            return True
        return False

    def remove_item(self, item: Item):
        """Remove an item from the inventory.
        
        Args:
            item (Item): The item to be removed from the inventory.
        """
        
        if item in self.items:
            self.items.pop(item, None)
    
    @property
    def held_item(self) -> Item:
        """Get the currently held item.
        
        Returns:
            Item | None: The currently held item, or None if no item is held.
        """
        for item in self.items:
            if self.get_slot(item) == 0:
                return item
        return None
    
    @held_item.setter
    def held_item(self, value: Item | None) -> None:
        """Set the currently held item.
        
        Args:
            value (Item | None): The item to be held, or None if no item is to be held.
        """
        if self.held_item is not None:
            self.swap_slots(self.held_item, value)
        elif self.held_item is None:
            self.set_slot(value, 0)

    def use_held_item(self, player, map):
        """Use the currently held item, if any.
        This method calls the use() method of the currently held item, if it exists."""
        held_item: Item = self.held_item
        if held_item is not None:
            held_item.use(player, map)
            if held_item.be_stackable:
                if held_item is not None and self.get_count(held_item) > 1:
                    self.set_count(held_item, self.get_count(held_item) - 1)
                else:
                    self.remove_item(held_item)
            else:
                if held_item.durability is not None:
                    held_item.durability -= 1
                    if held_item.durability < 1:
                        self.remove_item(held_item)

                        
    def open_inventory(self):
        """Transition into the inventory scene."""
        pygame.event.post(pygame.event.Event(STATE_PUSH, state="inventory"))
    
    def close_inventory(self):
        """Transition out of the inventory scene."""
        pygame.event.post(pygame.event.Event(STATE_POP))

    @property
    def first_empty_slot(self) -> int | None:
        """return the first empty slot in the inventory"""
        used = {v[self.SLOT_INDEX] for v in self.items.values()}

        for slot in range(self.max_slot):
            if slot not in used:
                return slot
                
        return None
    
    
    def get_item(self, id: int) -> Item:
        """Get the currently item in the id slot.

        Args:
            id (int): The number of the slot who are the item
        
        Returns:
            Item | None: The currently item in the id slot, or None if no item in the slot.
        """
        for item in self.items:
            if self.get_slot(item) == id:
                return item
        return None
    
    def __contains__(self, item: Item) -> bool:
        """Check if an item is in the inventory.
        
        Args:
            item (Item): The item to check for in the inventory.
        
        Returns:
            bool: True if the item is in the inventory, False otherwise.
        """
        return item in self.items

    def __getitem__(self, key: Item) -> int:
        """Get the count of a specific item in the inventory.
        
        Args:
            key (Item): The item for which to get the count.
        
        Returns:
            int: The count of the specified item in the inventory.
        """
        return self.get_count(key)
    
    def __setitem__(self, key: Item, value: int) -> None:
        """Set the count of a specific item in the inventory.
        
        Args:
            key (Item): The item for which to set the count.
            value (int): The new count for the specified item.
        """
        if key in self.items:
            self.items[key][self.COUNT_INDEX] = value

    def __len__(self):
        """Return the number of unique items in the inventory."""
        return len(self.items)
    
    def __bool__(self):
        """Return True if the inventory has any items, False otherwise."""
        return len(self.items) > 0
    
    def __iter__(self):
        """Return an iterator over the items in the inventory."""
        return iter(self.items)
