from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ally import Ally
    from jeu.Item import Item
    from WorldElement import WorldElement


from events import RECUP_EVENT, ALLY_EVENT, OPEN_INVENTORY_EVENT, CLOSE_INVENTORY_EVENT, KEYS
from Entity import Entity
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

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, allies: list[Ally] = None, inventory = None) -> None:
        """Initialize a player with allies and inventory state.
        
        Args:
            hp (int): Initial health points for the player. Must be a positive integer.
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
            coordinates (pygame.Vector2): The initial position of the player.
            allies (list[Ally], optional): List of allies to initialize with. Defaults to None.
            inventory (list, optional): List of items to initialize the inventory with. Defaults to None.
        """
        super().__init__(hp, sprites, coordinates, " ")
        self.allies: list["Ally"] = list(allies) if allies is not None else []
        self.inventory: Inventory = Inventory(list(inventory)) if inventory is not None else Inventory([])

    def attack(self, attacked: "Entity"):
        pass
        
    def combat(self):
        pass
    
    def interact(self, target: "Entity") -> bool:
        return False

    def use_item(self):
        """add the logic of using an item to the player(ex: shot with firegun ...)"""
        self.inventory.use_held_item()

    def switch_item(self, item_id):
        """switch the item in the hand
        Args:
            item_id (int): The index of the item in the inventory to switch to.
        """
        self.inventory.switch_item(item_id)

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

    def update(self, dt: float, events: list[pygame.event.Event], target: "Player" = None):
        """Update player movement from keyboard input and update allies.
        Args:
            dt (float): Time delta since last update, used for timing animations and movements."""
        self.animation_timer += dt
        
        keys = pygame.key.get_pressed()

        self.handle_events(events)
        self.handle_keys(keys)
        self.move(dt)

        for ally in self.allies:
            ally.update(dt, events, self)

    def handle_events(self, events: list[pygame.event.Event]):
        """Check for player-specific events such as item pickup or ally interaction.
        Args:
            events (list[pygame.event.Event]): List of events to process for interactions.
        """
        for event in events:
            if event.type == ALLY_EVENT:
                self.add_ally(event.dict["target"])
            if event.type == RECUP_EVENT:
                self.add_Item(event.dict["target"])

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
    
    def add_Item(self, item: Item):
        """add an item to the player's inventory.
        Args:
            item (Item): The item to be added to the player's inventory.
        
        Returns:
            bool: True if the item was successfully added to the inventory, False otherwise.
        """
        if item is not None:
            self.inventory.add_item(item)
            return True
        else:
            return False
        
    def load(self, sprites = None):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.

        Args:
            sprites (list[str], optional): List of sprite identifiers or paths to load. If None, uses existing sprite paths. Defaults to None.
        """
        if sprites is not None:
            self.sprite_paths = list(sprites)
        self.sprite = [pygame.image.load(s).convert_alpha() for s in self.sprite_paths]
        for ally in self.allies:
            ally.load()
        
    @property
    def get_allies(self):
        return self.allies

    @property
    def getPosition(self) -> pygame.Vector2:
        """Return the current position of the player as pygame.Vector2."""
        return self.coordinates
            
    
class Inventory:
    """Class to manage the player's inventory, including item storage and usage.
    
    Attributes:
        items (list[Item]): The list of items in the inventory.
        held_item (int | None): The index of the item currently held, or None if no item is held.
    """

    def __init__(self, items: list[Item]):
        """Class to manage the player's inventory, including item storage and usage.
        
        Args:
            items (list[Item]): The initial list of items in the inventory.
        """
        self.items = items
        #Held item is the index of the item in the inventory, None if no item is held
        self.held_item: int | None = 0

    def add_item(self, item: Item):
        """Add an item to the inventory.
        
        Args:            
            item (Item): The item to be added to the inventory.
        """
        self.items.append(item)

    def remove_item(self, item: Item):
        """Remove an item from the inventory.
        
        Args:
            item (Item): The item to be removed from the inventory.
        """
        
        if item in self.items:
            if self.items.index(item) == self.held_item:
                self.held_item = None
            self.items.remove(item)

    def switch_item(self, item_id: int | None):
        """Switch the currently held item to a different one in the inventory.
        
        Args:
            item_id (int | None): The index of the item to be held, or None if no item is held.
        """
        self.held_item = item_id
    
    def get_held_item(self):
        """Get the currently held item.
        
        Returns:
            Item | None: The currently held item, or None if no item is held.
        """
        if self.items and self.held_item is not None and 0 <= self.held_item < len(self.items):
            return self.items[self.held_item]
        else:
            return None
        
    def use_held_item(self):
        """Use the currently held item, if any.
        This method calls the use() method of the currently held item, if it exists."""
        held_item = self.get_held_item()
        if held_item is not None:
            held_item.use()

    def open_inventory(self):
        """Transition into the inventory scene."""
        pygame.event.post(pygame.event.Event(OPEN_INVENTORY_EVENT))
    
    def close_inventory(self):
        """Transition out of the inventory scene."""
        pygame.event.post(pygame.event.Event(CLOSE_INVENTORY_EVENT))
