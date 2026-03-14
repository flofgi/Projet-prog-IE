from Entity import Entity
from Player import Player
import pygame
from random import uniform, randint
from math import pi, cos, sin


class Mob(Entity):
    """class for mob.
    

    Attributes:
        hp (int): The entity's health points. When this reaches zero, the entity dies.
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the entity
        rect (pygame.Rect) collisions zone of the entity
        velocity (pygame.Vector2) vector of mouvement
        name (string) name of entity
        ALERT_ZONE (int) radius of the player detection by the mob
        CONFORT_ZONE (int) radius of the collision zone with player
        WANDERING_ZONE (int) radius of the wandering circle where the mob moves around
    """

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2) -> None:
        """Initialize a mob with tracking and wandering parameters."""
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.wandering_point = pygame.Vector2(0, 0)
        self.target_coordonnees = coordinates
        self.ALERT_ZONE = 200
        self.CONFORT_ZONE = 20
        self.WANDERING_ZONE = 200

    def interact(self):
        pass


    def attack(self):
        pass

    def update(self, target: Player = None):
        """Update mob behavior depending on distance to target."""
        self.animation_timer += 1
        
        if target != None:
            self.target_coordonnees = target.get_coordinates()

            distance_player_mob = self.target_coordonnees.distance_to(self.coordinates) 
            
            if distance_player_mob < self.CONFORT_ZONE:
                self.velocity = pygame.Vector2(0, 0)
            
            if distance_player_mob > self.ALERT_ZONE:
                self.wandering(target)

            else:
                self.coordinates = self.target_coordonnees
                self.velocity = pygame.Vector2(0, 0)
        else:
            self.wandering(self.target_coordonnees)
        self.move()

    def wandering(self, target: pygame.Vector2):
        """Add the wandering logic: the mob moves towards a random point within a circle of radius WANDERING_ZONE,
          with the point wandering_point as its center.
          Every 100 ticks, the point has a 50% chance of changing; otherwise, it stays in place."""
        if self.animation_timer > 100:
            self.animation_timer = 0
            if randint(0, 1) == 1:
                self.wandering_point = self.target_random_point(0, self.WANDERING_ZONE, self.wandering_point)
            else:
                self.velocity = pygame.Vector2(0, 0)

        direction = self.wandering_point - self.coordinates
        if self.velocity != pygame.Vector2(0, 0):
            self.velocity = direction.normalize() * (self.max_speed * 0.5)

    def modifie_zone(self, ALERT_ZONE = 200, CONFORT_ZONE = 20, WANDERING_ZONE = 200):
        """modifie the raduis of the different zone
        ALERT_ZONE
        CONFORT_ZONE
        WANDERING_ZONE"""
        self.ALERT_ZONE = ALERT_ZONE
        self.CONFORT_ZONE = CONFORT_ZONE
        self.WANDERING_ZONE = WANDERING_ZONE


    def target_random_point(self, min_rayon_limite, max_rayon_limite, target: pygame.Vector2 = None) -> pygame.Vector2:
        """Return a random point around target within radius limits."""
        if target == None:
            target = self.coordinates
        
        rayon = uniform(min_rayon_limite, max_rayon_limite)
        angle = uniform(0, pi*2)
        return pygame.Vector2(cos(angle)*rayon, sin(angle)*rayon)+target
