from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Camera import Camera

from abc import ABC, abstractmethod
import pygame

from WorldElement.WorldElement import WorldElement
from utilitary import DEAD, vec_to_list, list_to_vec


DEFAULT_VELOCITY = pygame.Vector2(0, 0)
DEFAULT_FRAME = 0
DEFAULT_ANIMATION_TIMER = 0
DEFAULT_MAX_SPEED = 1
MIN_HP = 0
DEFAULT_NAME = " "


class Entity(WorldElement):
    """Abstract base class for all game entities.
    
    This parent class provides a unified interface for managing entity lifecycle,
    including health (hp), visual representation through sprites, and spatial
    positioning. Foundation for various entity types such as mobs,
    players, and allies.

    Attributes:
        hp (int): The entity's health points. When this reaches zero, the entity dies.
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the entity
        rect (pygame.Rect) collisions zone of the entity
        velocity (pygame.Vector2) vector of mouvement
        name (string) name of entity
    """

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, name: str, BASE_FPS: int = 60) -> None:
        """
        Args:
            hp (int): Initial health points for the entity. Must be a positive integer.
            sprite (list[str]): List of images/identifiers for visual representation.
            coordinates (pygame.Vector2) position of the entity
            rect (pygame.Rect) collisions zone of the entity
            velocity (pygame.Vector2) vector of mouvement
            name (string) name of entity
            current_frame (int) index of the current sprite load
            animation_timer (int) index of the fps to load the next sprite
        """
        super().__init__(sprites, coordinates, name)
        self.hp = hp
        self.velocity = DEFAULT_VELOCITY.copy()
        self.current_frame = DEFAULT_FRAME
        self.animation_timer = DEFAULT_ANIMATION_TIMER
        self.max_speed = DEFAULT_MAX_SPEED
        self.BASE_FPS = BASE_FPS


    def move(self, dt: float, mouvement: pygame.Vector2 = None) -> None:
        """Handle entity movement with a given speed in self.velocity.

        dt is expected in seconds. Multiplying by BASE_FPS preserves legacy
        tuning where max_speed was effectively calibrated per frame at 60 FPS.
        """
        if mouvement is not None:
            self.velocity = mouvement
        self.coordinates += self.velocity * dt * self.BASE_FPS
        self.rect.topleft = (
            int(self.coordinates.x + self.hitbox_offset.x),
            int(self.coordinates.y + self.hitbox_offset.y),
        )

    @abstractmethod
    def combat(self):
        """Execute combat logic for the entity.
        """
        pass

    
    def is_attack(self, dommage: float):
        self.hp -= dommage
        if self.hp <= MIN_HP:
            pygame.event.post(pygame.event.Event(DEAD, target = self))

    def save(self, map_name, data: dict = {}) -> dict[str, dict]:
        data = super().save(map_name, data)
        
        
        data.update(
            {
                "hp": self.hp,
                "velocity": [self.velocity.x, self.velocity.y],
                "current_frame": self.current_frame,
                "animation_timer": self.animation_timer,
                "max_speed": self.max_speed,
            }
        )
        return data
    
    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> Entity:
        """Create an Entity instance from saved data.
        
        Args:
            data (dict): A dictionary containing the entity's saved state, including health points, velocity, animation state, and position.
            """
        
        coordinates_data = data.get(map_name, {}).get("coordinates")

        entity = self(
            hp=data.get("hp", 100),
            sprites=data.get("sprites", []),
            coordinates=list_to_vec(coordinates_data),
            name=data.get("name", DEFAULT_NAME)
        )
        entity.scale = data.get("scale", 1.0)

        
        entity.velocity = pygame.Vector2(data.get("velocity", [0, 0]))
        entity.current_frame = data.get("current_frame", 0)
        entity.animation_timer = data.get("animation_timer", 0)
        entity.max_speed = data.get("max_speed", 0)

        return entity




    def draw(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        if self.sprite:
            frame = self.sprite[self.current_frame]
            draw_pos = pygame.Vector2(self.rect.topleft) - self.hitbox_offset - camera.get_coordinates
            surface.blit(frame, draw_pos)

