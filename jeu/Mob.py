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
        """Initialize a mob with tracking and wandering parameters.
        Args:
            hp (int): Initial health points for the mob. Must be a positive integer.
            sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2): Position of the entity on the map.
        """
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.wandering_point = pygame.Vector2(coordinates)
        self.is_paused = False
        self.target_coordinates = coordinates
        self.ALERT_ZONE = 200
        self.CONFORT_ZONE = 20
        self.WANDERING_ZONE = 200
        self.max_speed = 0.7
        self.timer = 0

    def interact(self, player: Player) -> bool:
        """Check if player is close enough to interact and post a MOB_EVENT if so.
        
        Args:
            player (Player): The player entity to check interaction with.
        
        Returns:
            bool: True if interaction occurred, False otherwise.
        """
        return False


    def attack(self, attacked: "Entity"):
        pass

    def combat(self):
        pass


    def update(self, dt: float, events: list[pygame.event.Event], target: Player = None):
        """Update mob behavior depending on distance to target.
        Args:
            dt (float): Time delta since last update, used for timing animations and movements.
            events (list[pygame.event.Event]): List of events to process for interactions.
            target (Player, optional): The player entity to follow or wander around. Defaults to None.
        """
        self.animation_timer += dt
        self.timer += 1
        if self.timer % 15 == 0:
            if target is not None:
                self.target_coordinates = target.get_coordinates

                distance_player_mob = self.target_coordinates.distance_to(self.coordinates) 
                
                if distance_player_mob < self.CONFORT_ZONE:
                    self.velocity = pygame.Vector2(0, 0)

                elif distance_player_mob > self.ALERT_ZONE:
                    self.wandering(self.target_coordinates)

                else:
                    direction = self.target_coordinates - self.coordinates
                    if direction.length_squared() > 0:
                        self.velocity = direction.normalize() * self.max_speed
                    else:
                        self.velocity = pygame.Vector2(0, 0)
            else:
                self.wandering(self.target_coordinates)
        self.move(dt)





    def wandering(self, target: pygame.Vector2):
        """Add the wandering logic: the mob moves towards a random point within a circle of radius WANDERING_ZONE,
          centered on the given target position. The chosen destination is stored in wandering_point.
          Every 100 ticks, the destination point has a 50% chance of changing; otherwise, it stays in place.
          Args:
            target (pygame.Vector2): The position to wander around.
        """
        if self.animation_timer > 100 / self.BASE_FPS:
            self.animation_timer = 0
            self.is_paused = randint(0, 1) == 0
            if not self.is_paused:
                self.wandering_point = self.target_random_point(0, self.WANDERING_ZONE, target)

        if self.is_paused:
            self.velocity = pygame.Vector2(0, 0)
            return

        direction = self.wandering_point - self.coordinates
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * (self.max_speed * 0.5)
        else:
            self.velocity = pygame.Vector2(0, 0)



    def modifie_zone(self, ALERT_ZONE = 200, CONFORT_ZONE = 20, WANDERING_ZONE = 200):
        """Update mob distance thresholds for follow and wandering zones.
        Args:
            ALERT_ZONE (int, optional): Distance at which mob starts following the target. Defaults to 200.
            CONFORT_ZONE (int, optional): Distance within which mob feels comfortable. Defaults to 20.
            WANDERING_ZONE (int, optional): Distance within which mob will wander around the target. Defaults to 200.
        """
        self.ALERT_ZONE = ALERT_ZONE
        self.CONFORT_ZONE = CONFORT_ZONE
        self.WANDERING_ZONE = WANDERING_ZONE


    def target_random_point(self, min_rayon_limite, max_rayon_limite, target: pygame.Vector2 = None) -> pygame.Vector2:
        """Return a random point around target within radius limits.
        Args:
            min_rayon_limite (float): Minimum distance from target for the random point.
            max_rayon_limite (float): Maximum distance from target for the random point.
            target (pygame.Vector2, optional): The position to generate a random point around. Defaults to None, which uses the mob's current position.
        """
        if target == None:
            target = self.coordinates
        
        rayon = uniform(min_rayon_limite, max_rayon_limite)
        angle = uniform(0, pi*2)
        return pygame.Vector2(cos(angle)*rayon, sin(angle)*rayon)+target
