from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Camera import Camera

from abc import ABC, abstractmethod
import pygame

from WorldElement.WorldElement import WorldElement
from events import DEAD


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
        self.velocity = pygame.Vector2(0, 0)
        self.current_frame = 0
        self.animation_timer = 0
        self.max_speed = 1
        self.BASE_FPS = BASE_FPS


    def move(self, dt: float) -> None:
        """Handle entity movement with a given speed in self.velocity.

        dt is expected in seconds. Multiplying by BASE_FPS preserves legacy
        tuning where max_speed was effectively calibrated per frame at 60 FPS.
        """
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
        if self.hp <= 0:
            pygame.event.post(pygame.event.Event(DEAD, target = self))

    def draw(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        if self.sprite:
            frame = self.sprite[self.current_frame]
            draw_pos = pygame.Vector2(self.rect.topleft) - self.hitbox_offset - camera.get_position
            surface.blit(frame, draw_pos)

