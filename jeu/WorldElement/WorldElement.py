from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map
    from Camera import Camera


from abc import ABC, abstractmethod
from utilitary import vec_to_list

import pygame


DEFAULT_NAME = " "
DEFAULT_COORDINATES = pygame.Vector2(0, 0)
DEFAULT_RECT_SIZE = pygame.Vector2(0, 0)
DEFAULT_SCALE = 1
BOUNDING_RECT_MIN_ALPHA = 1




class WorldElement(ABC):
    """class that implements the element who are disposed on a map
    
    Attributes:
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the element on the map
    
    """


    def __init__(self, sprites: list[str],  coordinates: pygame.Vector2, name: str = DEFAULT_NAME):
        """
        Args:
            sprites (list[str]) : List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2) : position of the element on the map
            
        """
        self.sprite_paths = sprites
        self.sprite: list[pygame.Surface] = []
        self.sprite_bounding_offsets: list[pygame.Vector2] = []
        self.name = name
        self.rect = pygame.Rect(0, 0, DEFAULT_RECT_SIZE.x, DEFAULT_RECT_SIZE.y)
        self.coordinates: pygame.Vector2 | None = None
        self.get_coordinates = pygame.Vector2(coordinates) if coordinates is not None else DEFAULT_COORDINATES.copy()
        self.is_enemy = False
        self.scale = DEFAULT_SCALE

    @abstractmethod
    def update(self, dt: float, map: Map, target: Player = None):
        """update position and animation of entity
        Don't forget to change the animation timer. """
        pass

    def handle_event(self, event: pygame.event.Event):
        """Check for player-specific events such as item pickup or ally interaction.
        Args:
            events (pygame.event.Event):events to process for interactions.
        """
        pass


    @property    
    def get_coordinates(self) -> pygame.Vector2:
        """Return the current position of the entity as pygame.Vector2."""
        return self.coordinates
    
    @get_coordinates.setter
    def get_coordinates(self, new_coordinates: pygame.Vector2):
        """Set the entity's position to the given coordinates."""
        self.coordinates = pygame.Vector2(new_coordinates)
        self.rect.midbottom = self.coordinates.x, self.coordinates.y

    @property
    def get_rect(self) -> pygame.Rect:
        """Return the current position of the entity as pygame.Vector2."""
        return self.rect
    
    def draw(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        """Draw the entity on the given surface, optionally using player information for relative positioning."""
        sprite_offset = self.sprite_bounding_offsets[0] if self.sprite_bounding_offsets else pygame.Vector2()
        draw_x = self.rect.x - camera.x - sprite_offset.x
        draw_y = self.rect.y - camera.y - sprite_offset.y
        surface.blit(self.sprite[0], (draw_x, draw_y))


    def load(self):
        """Load sprites from disk.

        If sprites is provided, replace the stored sprite paths before loading.
        """
        self.sprite = [pygame.image.load(s).convert_alpha() for s in self.sprite_paths]
        self.sprite_size = [s.get_size() for s in self.sprite]
        self.sprite_bounding_offsets = []
        for image in self.sprite:
            bounding_rect = image.get_bounding_rect(min_alpha=BOUNDING_RECT_MIN_ALPHA)
            self.sprite_bounding_offsets.append(pygame.Vector2(bounding_rect.topleft))

        self.rect = self.sprite[0].get_bounding_rect(min_alpha=BOUNDING_RECT_MIN_ALPHA)
        if self.rect.width == DEFAULT_RECT_SIZE.x or self.rect.height == DEFAULT_RECT_SIZE.y:
            self.rect = self.sprite[0].get_rect()
            if self.sprite_bounding_offsets:
                self.sprite_bounding_offsets[0] = pygame.Vector2()
        self.get_coordinates = self.coordinates.copy() if self.coordinates is not None else None


    def save(self, map_name: str, data: dict | None = None) -> dict:
        """Serialize the common state shared by every world element."""
        data = data or {}
        data.update({
            "type": self.__class__.__name__,
            "name": self.name,
            "sprites": list(self.sprite_paths),
            map_name:{
                "coordinates": vec_to_list(self.get_coordinates),
            },
            "scale": self.scale,
        })
        return data


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