from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Camera import Camera
    from Map import Map

from abc import ABC, abstractmethod
import pygame
from random import random

from WorldElement.WorldElement import WorldElement
from utilitary import DEAD, vec_to_list, list_to_vec



DEFAULT_VELOCITY = pygame.Vector2(0, 0)
DEFAULT_FRAME = 0
DEFAULT_ANIMATION_TIMER = 0
DEFAULT_MAX_SPEED = 1
MIN_HP = 0
DEFAULT_NAME = " "
HEIGH_COLLISION = 10
COLLISION_COEF = 2


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
        self.collision_rect = self.rect.copy()


    def update_collision_rect(self) -> None:
        """Rebuild the collision hitbox at the entity's feet."""
        self.collision_rect = pygame.Rect(
            self.rect.left,
            self.rect.bottom - HEIGH_COLLISION,
            self.rect.width,
            HEIGH_COLLISION,
        )


    def move(self, dt: float, mouvement: pygame.Vector2 = None) -> None:
        """Handle entity movement with a given speed in self.velocity.

        dt is expected in seconds. Multiplying by BASE_FPS preserves legacy
        tuning where max_speed was effectively calibrated per frame at 60 FPS.
        """
        if mouvement is not None:
            self.velocity = mouvement
        
        self.get_coordinates += self.velocity * dt * self.BASE_FPS
        self.rect.bottom = self.get_coordinates.y
        self.rect.centerx = self.get_coordinates.x
        self.update_collision_rect()

        
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
        entity.update_collision_rect()
        
        entity.velocity = pygame.Vector2(data.get("velocity", [0, 0]))
        entity.current_frame = data.get("current_frame", 0)
        entity.animation_timer = data.get("animation_timer", 0)
        entity.max_speed = data.get("max_speed", 0)

        return entity




    def draw(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        if self.sprite:
            frame = self.sprite[self.current_frame]
            draw_pos = pygame.Vector2(self.rect.topleft) - camera.get_coordinates
            surface.blit(frame, draw_pos)


    def load(self):
        super().load()
        self.update_collision_rect()


    def handle_entity_collision(self, dt, other: Entity) -> None:
        """Handle collision with another world element.
        
        This method can be overridden by subclasses to implement specific collision
        responses, such as taking damage, bouncing off, or triggering events.
        """
        direction = (pygame.Vector2(self.collision_rect.center) - pygame.Vector2(other.collision_rect.center))
        if direction.length() == 0:
            direction = pygame.Vector2(random(),random()) 
        else:
            direction = direction.normalize()

        self.velocity += direction * COLLISION_COEF * dt
        other.velocity -= direction * COLLISION_COEF * dt 

    def handle_wall_collision(self, dt, wall: pygame.Rect, map: Map) -> None:
        """Handle collision with a wall using AABB logic.
        
        Check if next position would collide, and if so, resolve along the axis
        of minimum penetration depth.
        """
        next_rect = self.collision_rect.copy()
        next_rect.topleft = self.collision_rect.topleft + self.velocity * dt * self.BASE_FPS

        if not next_rect.colliderect(wall):
            return

        # Penetration depths (toujours positifs si collision réelle)
        overlap_left   = next_rect.right  - wall.left   # entité dépasse à droite du mur
        overlap_right  = wall.right  - next_rect.left   # entité dépasse à gauche du mur
        overlap_top    = next_rect.bottom - wall.top     # entité dépasse en bas du mur
        overlap_bottom = wall.bottom  - next_rect.top   # entité dépasse en haut du mur

        # Axe de correction = pénétration minimale
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            # Entité vient de la gauche → recule à gauche
            self.get_coordinates.x -= overlap_left
            self.velocity.x = 0
        elif min_overlap == overlap_right:
            # Entité vient de la droite → recule à droite
            self.get_coordinates.x += overlap_right
            self.velocity.x = 0
        elif min_overlap == overlap_top:
            # Entité vient du haut → recule vers le haut
            self.get_coordinates.y -= overlap_top
            self.velocity.y = 0
        elif min_overlap == overlap_bottom:
            # Entité vient du bas → recule vers le bas
            self.get_coordinates.y += overlap_bottom
            self.velocity.y = 0

        self.rect.bottom  = self.get_coordinates.y
        self.rect.centerx = self.get_coordinates.x
        self.update_collision_rect()