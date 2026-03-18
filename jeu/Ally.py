from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player


from Entity import Entity
import pygame
from random import uniform, randint
from math import pi, cos, sin


class Ally(Entity):
    """class for player's Ally.
    

    Attributes:
        hp (int): The entity's health points. When this reaches zero, the entity dies.
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the entity
        rect (pygame.Rect) collisions zone of the entity
        velocity (pygame.Vector2) vector of mouvement
        name (string) name of entity
    """

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2) -> None:
        """Initialize an ally with follow and wandering parameters."""
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.wandering_point = pygame.Vector2(0, 0)
        self.target_coordinates = coordinates
        self.ALERT_ZONE = 400
        self.CONFORT_ZONE = 20
        self.WANDERING_ZONE = 200

    def interaction(self):
        pass


    def attack(self, attacked: Entity):
        pass

    def combat(self):
        pass

    def interact(self):
        pass


    def update(self, dt: float, events: list[pygame.event.Event], target: Player = None):
        """Update ally behavior to follow or wander around a target."""
        self.animation_timer += dt
        
        if target is not None:
            self.target_coordinates = target.get_coordinates()

            distance_player_ally = self.target_coordinates.distance_to(self.coordinates) 
            
            if distance_player_ally < self.CONFORT_ZONE:
                self.velocity = pygame.Vector2(0, 0)
            
            elif distance_player_ally > self.ALERT_ZONE:
                self.coordinates = self.target_random_point(self.CONFORT_ZONE, self.CONFORT_ZONE+10, self.target_coordinates)
                self.velocity = pygame.Vector2(0, 0)

            else:
                self.wandering(target.get_coordinates())
        else:
            self.wandering(self.target_coordinates)
        self.move(dt)

    def wandering(self, target: pygame.Vector2):
        """Move ally toward a random wandering point near the target."""
        if self.animation_timer > 100 / self.BASE_FPS:
            self.animation_timer = 0
            if randint(0, 1) == 1:
                self.wandering_point = self.target_random_point(self.CONFORT_ZONE, self.WANDERING_ZONE, target)

        direction = self.wandering_point - self.coordinates
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * (self.max_speed * 0.5)

    def set_zones(self, ALERT_ZONE = 400, CONFORT_ZONE = 20, WANDERING_ZONE = 200):
        """Update ally distance thresholds for follow and wandering zones."""
        self.ALERT_ZONE = ALERT_ZONE
        self.CONFORT_ZONE = CONFORT_ZONE
        self.WANDERING_ZONE = WANDERING_ZONE


    def target_random_point(self, min_rayon_limite, max_rayon_limite, target: pygame.Vector2 = None) -> pygame.Vector2:
        """Return a random point around target within radius limits."""
        if target is not None:
            target = self.coordinates
        
        rayon = uniform(min_rayon_limite, max_rayon_limite)
        angle = uniform(0, pi*2)
        return pygame.Vector2(cos(angle)*rayon, sin(angle)*rayon)+target
