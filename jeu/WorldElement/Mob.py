from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map

from WorldElement.Entity import Entity
import pygame
from random import uniform, randint
from math import pi, cos, sin
from utilitary import BOSSFIGHT, DEAD, vec_to_list, list_to_vec


DEFAULT_NAME = " "
DEFAULT_ALERT_ZONE = 200
DEFAULT_CONFORT_ZONE = 20
DEFAULT_WANDERING_ZONE = 200
DEFAULT_MAX_SPEED = 0.7
DEFAULT_TIMER = 0
DECISION_INTERVAL_TICKS = 15
PAUSE_CHECK_SECONDS = 100
HALF_SPEED_FACTOR = 0.5
RANDOM_BOOL_MIN = 0
RANDOM_BOOL_MAX = 1
TAU = pi * 2
ZERO_VECTOR = pygame.Vector2(0, 0)
MIN_HP = 0


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

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, name: str = DEFAULT_NAME, is_boss: bool = False) -> None:
        """Initialize a mob with tracking and wandering parameters.
        Args:
            hp (int): Initial health points for the mob. Must be a positive integer.
            sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2): Position of the entity on the map.
        """
        Entity.__init__(self, hp, sprites, coordinates, name)
        self.wandering_point = pygame.Vector2(coordinates)
        self.is_paused = False
        self.target_coordinates = coordinates
        self.ALERT_ZONE = DEFAULT_ALERT_ZONE
        self.CONFORT_ZONE = DEFAULT_CONFORT_ZONE
        self.WANDERING_ZONE = DEFAULT_WANDERING_ZONE
        self.max_speed = DEFAULT_MAX_SPEED
        self.timer = DEFAULT_TIMER
        self.is_boss = is_boss
        self.is_enemy = True

    def interact(self, player: Player) -> bool:
        """Check if player is close enough to interact and post a MOB_EVENT if so.
        
        Args:
            player (Player): The player entity to check interaction with.
        
        Returns:
            bool: True if interaction occurred, False otherwise.
        """
        return False

    def combat(self):
        pass


    def update(self, dt: float, map: Map, target: Player = None):
        """Update mob behavior depending on distance to target.
        Args:
            dt (float): Time delta since last update, used for timing animations and movements.
            events (list[pygame.event.Event]): List of events to process for interactions.
            target (Player, optional): The player entity to follow or wander around. Defaults to None.
        """
        self.animation_timer += dt
        self.timer += 1
        if self.timer % DECISION_INTERVAL_TICKS == 0:
            if target is not None:
                self.target_coordinates = target.get_coordinates

                distance_player_mob = self.target_coordinates.distance_to(self.coordinates) 
                
                if distance_player_mob < self.CONFORT_ZONE:
                    self.velocity = ZERO_VECTOR.copy()

                elif distance_player_mob > self.ALERT_ZONE:
                    self.wandering(self.target_coordinates)

                else:
                    direction = self.target_coordinates - self.coordinates
                    if direction.length_squared() > 0:
                        self.velocity = direction.normalize() * self.max_speed
                    else:
                        self.velocity = ZERO_VECTOR.copy()
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
        if self.animation_timer > PAUSE_CHECK_SECONDS / self.BASE_FPS:
            self.animation_timer = 0
            self.is_paused = randint(RANDOM_BOOL_MIN, RANDOM_BOOL_MAX) == RANDOM_BOOL_MIN
            if not self.is_paused:
                self.wandering_point = self.target_random_point(RANDOM_BOOL_MIN, self.WANDERING_ZONE, target)

        if self.is_paused:
            self.velocity = ZERO_VECTOR.copy()
            return

        direction = self.wandering_point - self.coordinates
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * (self.max_speed * HALF_SPEED_FACTOR)
        else:
            self.velocity = ZERO_VECTOR.copy()



    def modifie_zone(self, ALERT_ZONE = DEFAULT_ALERT_ZONE, CONFORT_ZONE = DEFAULT_CONFORT_ZONE, WANDERING_ZONE = DEFAULT_WANDERING_ZONE):
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
        angle = uniform(RANDOM_BOOL_MIN, TAU)
        return pygame.Vector2(cos(angle)*rayon, sin(angle)*rayon)+target
    
    def is_attack(self, dommage: float):
        self.hp -= dommage
        if self.hp <= MIN_HP:
            pygame.event.post(pygame.event.Event(DEAD, target = self))
        elif self.is_boss:
            pygame.event.post(pygame.event.Event(BOSSFIGHT, target = self))

    def save(self, map_name) -> dict:
        data = super().save(map_name)
        wandering_point = [self.wandering_point.x, self.wandering_point.y] if self.wandering_point is not None else None
        target_coordinates = [self.target_coordinates.x, self.target_coordinates.y] if self.target_coordinates is not None else None
        data.update(
            {
                "wandering_point": wandering_point,
                "target_coordinates": target_coordinates,
                "ALERT_ZONE": self.ALERT_ZONE,
                "CONFORT_ZONE": self.CONFORT_ZONE,
                "WANDERING_ZONE": self.WANDERING_ZONE,
                "is_paused": self.is_paused,
                "timer": self.timer,
                "is_boss": self.is_boss,
                "coordinates": vec_to_list(self.coordinates)
            }
        )
        return data


    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> Mob:
        """Create a Mob instance from saved data.

        Args:
            data (dict): A dictionary containing the ally's saved state, including wandering point, target coordinates, and zone thresholds.
        """
        hp = data.get("hp", 100)
        sprites = data.get("sprites", [])

        map_data = data.get(map_name, {}) if map_name is not None else data
        coordinates = list_to_vec(map_data.get("coordinates", data.get("coordinates", [0, 0])))

        mob = Mob(hp, sprites, coordinates)
        
        
        mob.name = data.get("name", DEFAULT_NAME)
        mob.scale = data.get("scale", 1.0)
        
        mob.velocity = pygame.Vector2(0, 0)
        mob.current_frame = data.get("current_frame", 0)
        mob.animation_timer = data.get("animation_timer", 0)
        mob.max_speed = data.get("max_speed", 0)

        mob.wandering_point = list_to_vec(map_data.get("wandering_point", [0, 0]))
        mob.target_coordinates = list_to_vec(map_data.get("target_coordinates", [0, 0]))
        mob.ALERT_ZONE = map_data.get("ALERT_ZONE", DEFAULT_ALERT_ZONE)
        mob.CONFORT_ZONE = map_data.get("CONFORT_ZONE", DEFAULT_CONFORT_ZONE)
        mob.WANDERING_ZONE = map_data.get("WANDERING_ZONE", DEFAULT_WANDERING_ZONE)
        mob.is_paused = map_data.get("is_paused", False)
        mob.timer = map_data.get("timer", 0)
        mob.is_boss = map_data.get("is_boss", False)

        return mob
