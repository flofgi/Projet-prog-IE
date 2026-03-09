from abc import ABC, abstractmethod
import pygame
from Player import Player

class Entity(ABC):
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
    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, name: str) -> None:
        """
        Args:
            hp (int): Initial health points for the entity. Must be a positive integer.
            sprite (list[str]): List of images/identifiers for visual representation.
            coordinates (pygame.Vector2) position of the entity
            rect (pygame.Rect) collisions zone of the entity
            velocity (pygame.Vector2) vector of mouvement
            name (string) name of entity
            current_frame (int) index of the current sprit load
            animation_timer (int) index of the fps to load the next sprite
        """
        self.hp = hp
        self.sprite = sprites
        self.coordinates = coordinates
        self.rect = pygame.Rect()
        self.velocity = pygame.Vector2(0, 0)
        self.name = name
        self.current_frame = 0
        self.animation_timer = 0
        self.max_speed = 1


    def move(self) -> None:
        """Handle entity movement with a given speed.

        Args:
            speed (tuple[int, int]): displacement vector (dx, dy) to apply.
        """
        self.coordinates += self.velocity
        self.rect.topleft = (self.coordinates.x, self.coordinates.y)


    @abstractmethod
    def combat(self):
        """Execute combat logic for the entity.
        """
        pass


    @abstractmethod
    def interact(self):
        """Handle interaction with the entity (e.g. talking, using)."""
        pass

    @abstractmethod
    def update(self, target: "Player" = None):
        """update position and animation of entity
        Don't forget to change the animation timer. """
        pass


    def get_coordinates(self) -> pygame.Vector2:
        """Return the current position of the entity as pygame.Vector2."""
        return self.coordinates
    
    def attack(self, attacked: "Entity"):
        """add the logic of the attack for entity"""
        pass
    
