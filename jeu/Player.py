from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ally import Ally

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
        """Initialize a player with allies and inventory state."""
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.allies: list["Ally"] = list(allies) if allies is not None else []
        self.inventory = list(inventory) if inventory is not None else []
        self.held_item = 0

    def attack(self, attacked: "Entity"):
        pass
        
    def combat(self):
        pass
    
    def interact(self):
        pass

    def use_item(self):
        """add the logic of using an item to the player(ex: shot with firegun ...)"""
        pass

    def switch_item(self, item_id):
        """switch the item in the hand"""
        self.held_item = item_id

    def open_inventory(self):
        """transition into the inventory scene"""
        pass

    def drop(self, item):
        """The item drops in the sector at the exact spot where the player is located"""
        pass

    def add_ally(self, new_ally: Ally):
        """add new ally to Player base"""
        if new_ally not in self.allies:
            self.allies.append(new_ally)

    def update(self, dt: float, target: "Player" = None):
        """Update player movement from keyboard input and update allies."""
        self.animation_timer += dt

        keys = pygame.key.get_pressed()
        direction_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.velocity = pygame.Vector2(direction_x, direction_y)

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.move(dt)
        for ally in self.allies:
            ally.update(dt, self)

    def is_ally(self, ally: Ally):
        """check if an ally is an player's ally"""
        return ally in self.allies
    
