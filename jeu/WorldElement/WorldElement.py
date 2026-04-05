from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map


from abc import ABC, abstractmethod

import pygame




class WorldElement(ABC):
    """class that implements the element who are disposed on a map
    
    Attributes:
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the element on the map
    
    """


    def __init__(self, sprites: list[str],  coordinates: pygame.Vector2, name: str = " "):
        """
        Args:
            sprites (list[str]) : List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2) : position of the element on the map
            
        """
        self.sprite_paths = sprites
        self.sprite: list[pygame.Surface] = []
        self.name = name
        self.coordinates = coordinates
        self.rect = pygame.Rect(coordinates.x, coordinates.y, 0, 0)
        self.is_enemy = False

    @abstractmethod
    def update(self, dt: float, map: Map, target: Player = None):
        """update position and animation of entity
        Don't forget to change the animation timer. """
        pass

    def handle_events(self, event: pygame.event.Event):
        """Check for player-specific events such as item pickup or ally interaction.
        Args:
            events (pygame.event.Event):events to process for interactions.
        """
        pass


    @property    
    def get_coordinates(self) -> pygame.Vector2:
        """Return the current position of the entity as pygame.Vector2."""
        return pygame.Vector2(self.rect.centerx ,self.rect.bottom)
    
    @property
    def get_rect(self) -> pygame.Rect:
        """Return the current position of the entity as pygame.Vector2."""
        return self.rect
    
    @abstractmethod
    def draw(self, surface: pygame.Surface, player: Player = None) -> None:
        pass

    def load(self):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.
        """
        self.sprite = [pygame.image.load(s).convert_alpha() for s in self.sprite_paths]
        self.sprite_size = [s.get_size() for s in self.sprite]

    def distance_to(self, target: WorldElement | pygame.Vector2) -> float:
        """Calculate the distance between this element and a target.
        Args:
            target (WorldElement | pygame.Vector2): The target element or position.
        Returns:
            int: The distance to the target.
        """
        if isinstance(target, WorldElement):
            target = target.get_coordinates
        return self.get_coordinates.distance_to(target)

    def unload(self):
        self.sprite = [None for s in self.sprite]


    def interact(self, player: Player) -> bool:
        """Handle interaction with the entity (e.g. talking, using).
        return True if the interaction is good else False"""
        return False

    
    def __lt__(self, other: "WorldElement"):
        return self.get_rect.bottom < other.get_rect.bottom

    def __le__(self, other: "WorldElement"):
        return self.get_rect.bottom <= other.get_rect.bottom

    def __gt__(self, other: "WorldElement"):
        return self.get_rect.bottom > other.get_rect.bottom

    def __ge__(self, other: "WorldElement"):
        return self.get_rect.bottom >= other.get_rect.bottom
    
    def collidepoint(self, point: pygame.Vector2) -> bool:
        """Check if the given point is within the entity's collision rectangle."""
        return self.get_rect.collidepoint(point.x, point.y)