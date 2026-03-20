from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player


from events import RECUP_EVENT



import pygame
from WorldElement import WorldElement


class Item(WorldElement):
    """class that implements the items that the player can drop onto the map
    
    Attributes:
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the entity
    
    """

    def __init__(self, sprites : list[str], coordinates: pygame.Vector2, durability: int = None):
        super().__init__(sprites, coordinates)
        
        #Is None if the Item have infinity durability
        self.durability = durability


    def use(self):
        pass

    def interact(self, player: Player) -> bool:
        if self.coordinates is not None and player.get_coordinates.distance_to(self.coordinates) < 20:
            pygame.event.post(pygame.event.Event(RECUP_EVENT, {
                "target": self
            }))
            self.coordinates = None
            return True
        return False


    def draw(self, surface: pygame.surface, player: Player) -> None:
        pass

    def update(self, dt: float, events: list[pygame.event.Event], target: Player = None):
        pass