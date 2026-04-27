from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player


from abc import ABC, abstractmethod

import pygame




class WorldElement(ABC):
    """class that implements the element who are disposed on a map
    
    Attributes:
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the element on the map
    
    """


    def __init__(self, sprites: list[str],  coordinates: pygame.Vector2):
        """
        Args:
            sprites (list[str]) : List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2) : position of the element on the map
            
        """
        self.sprite_paths = list(sprites)
        self.sprite = []
        self.coordinates = coordinates
        if self.sprite:
            self.rect = self.sprite[0].get_rect(topleft=(self.coordinates.x, self.coordinates.y))
        else:
            self.rect = pygame.Rect(coordinates.x, coordinates.y, 0, 0)

    @abstractmethod
    def update(self, dt: float, events: list[pygame.event.Event], target: "Player" = None):
        """update position and animation of entity
        Don't forget to change the animation timer. """
        pass


    @property    
    def get_coordinates(self) -> pygame.Vector2:
        """Return the current position of the entity as pygame.Vector2."""
        return self.coordinates
    
    @property
    def get_rect(self) -> pygame.Rect:
        """Return the current position of the entity as pygame.Vector2."""
        return self.rect
    
    @abstractmethod
    def draw(self, surface: pygame.surface, player: Player) -> None:
        pass

    def load(self, sprites: list[str] | None = None):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.
        """
        if sprites is not None:
            self.sprite_paths = list(sprites)
        self.sprite = [pygame.image.load(s).convert_alpha() for s in self.sprite_paths]

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
    
    def contains_point(self, point: pygame.Vector2) -> bool:
        """Check if the given point is within the entity's collision rectangle."""
        return self.get_rect.collidepoint(point.x, point.y)