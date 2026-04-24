from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map


from WorldElement.Entity import Entity
import pygame
from random import uniform, randint
from math import pi, cos, sin
from utilitary import ALLY_EVENT, list_to_vec, vec_to_list


DEFAULT_NAME = " "
DEFAULT_WANDERING_POINT = pygame.Vector2(0, 0)
DEFAULT_ALERT_ZONE = 400
DEFAULT_CONFORT_ZONE = 20
DEFAULT_WANDERING_ZONE = 200
INTERACTION_DISTANCE = 20
FOLLOW_TELEPORT_MARGIN = 5
WANDER_CHECK_SECONDS = 100
HALF_SPEED_FACTOR = 0.5
RANDOM_BOOL_MIN = 0
RANDOM_BOOL_MAX = 1
TAU = pi * 2


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
        Entity.__init__(self, hp, sprites, coordinates, DEFAULT_NAME)
        self.wandering_point = DEFAULT_WANDERING_POINT.copy()
        self.target_coordinates = coordinates
        self.ALERT_ZONE = DEFAULT_ALERT_ZONE
        self.CONFORT_ZONE = DEFAULT_CONFORT_ZONE
        self.WANDERING_ZONE = DEFAULT_WANDERING_ZONE

    def interaction(self):
        pass

    def combat(self):
        pass

    def interact(self, player: Player) -> bool:
        """Check if player is close enough to interact and post an ALLY_EVENT if so.
        
        Args:
            player (Player): The player entity to check interaction with.
        
        Returns:
            bool: True if interaction occurred, False otherwise.
        """
        if player.get_coordinates.distance_to(self.coordinates) < INTERACTION_DISTANCE:
            pygame.event.post(pygame.event.Event(ALLY_EVENT, {
                "target": self
            }))
            return True
        return False


    def update(self, dt: float, map: Map, target: Player = None):
        """Update ally behavior to follow or wander around a target.
        Args:
            dt (float): Time delta since last update, used for timing animations and movements.
            target (Player, optional): The player entity to follow or wander around. Defaults to None.
        """
        self.animation_timer += dt
        
        if target is not None and target.is_ally(self):
            self.target_coordinates = target.get_coordinates

            distance_player_ally = self.target_coordinates.distance_to(self.coordinates) 
            
            if distance_player_ally < self.CONFORT_ZONE:
                self.velocity = pygame.Vector2(0, 0)
            
            elif distance_player_ally > self.ALERT_ZONE:
                self.coordinates = self.target_random_point(self.CONFORT_ZONE, self.CONFORT_ZONE + FOLLOW_TELEPORT_MARGIN, self.target_coordinates)
                self.velocity = DEFAULT_WANDERING_POINT.copy()
                

            else:
                self.wandering(target.get_coordinates)
        else:
            self.wandering(self.target_coordinates)
        self.move(dt)

    def wandering(self, target: pygame.Vector2):
        """Move ally toward a random wandering point near the target.
        Args:
            target (pygame.Vector2): The position to wander around."""
        if self.animation_timer > WANDER_CHECK_SECONDS / self.BASE_FPS:
            self.animation_timer = 0
            if randint(RANDOM_BOOL_MIN, RANDOM_BOOL_MAX) == RANDOM_BOOL_MAX:
                self.wandering_point = self.target_random_point(self.CONFORT_ZONE, self.WANDERING_ZONE, target)

        direction = self.wandering_point - self.coordinates
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * (self.max_speed * HALF_SPEED_FACTOR)

    def set_zones(self, ALERT_ZONE = DEFAULT_ALERT_ZONE, CONFORT_ZONE = DEFAULT_CONFORT_ZONE, WANDERING_ZONE = DEFAULT_WANDERING_ZONE):
        """Update ally distance thresholds for follow and wandering zones.
        Args:
            ALERT_ZONE (int, optional): Distance at which ally starts following the target. Defaults to 400.
            CONFORT_ZONE (int, optional): Distance within which ally feels comfortable. Defaults to 20.
            WANDERING_ZONE (int, optional): Distance within which ally will wander around the target. Defaults to 200.
        """
        self.ALERT_ZONE = ALERT_ZONE
        self.CONFORT_ZONE = CONFORT_ZONE
        self.WANDERING_ZONE = WANDERING_ZONE


    def target_random_point(self, min_rayon_limite, max_rayon_limite, target: pygame.Vector2 = None) -> pygame.Vector2:
        """Return a random point around target within radius limits.
        Args:
            min_rayon_limite (float): Minimum distance from target for the random point.
            max_rayon_limite (float): Maximum distance from target for the random point.
            target (pygame.Vector2, optional): The position to generate a random point around. Defaults to None, which uses the ally's current position.
            
        Returns:
            pygame.Vector2: A random point around the target within the specified radius limits."""
        if target is None:
            target = self.coordinates
        
        rayon = uniform(min_rayon_limite, max_rayon_limite)
        angle = uniform(RANDOM_BOOL_MIN, TAU)
        return pygame.Vector2(cos(angle)*rayon, sin(angle)*rayon)+target



    def save(self, map_name: str | None, data: dict[str, dict] | None = None) -> dict:
        if data is None:
            data = {}
        if map_name not in data:
            data[map_name] = {}


        super().save(data)
        wandering_point = vec_to_list(self.wandering_point)
        target_coordinates = vec_to_list(self.target_coordinates)


        data[map_name].update(
            {
                "wandering_point": wandering_point,
                "target_coordinates": target_coordinates,
                "ALERT_ZONE": self.ALERT_ZONE,
                "CONFORT_ZONE": self.CONFORT_ZONE,
                "WANDERING_ZONE": self.WANDERING_ZONE
            }
        )

        return data

    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> Ally:
        """Create an Ally instance from saved data.
        
        Args:
            data (dict): A dictionary containing the ally's saved state, including wandering point, target coordinates, and zone thresholds.
        """
 
        ally: Ally = super().load_from_data(data, map_name)

        ally.wandering_point = list_to_vec(data.get(map_name, {}).get("wandering_point", [0, 0]))
        ally.target_coordinates = list_to_vec(data.get(map_name, {}).get("target_coordinates", [0, 0]))
        ally.ALERT_ZONE = data.get(map_name, {}).get("ALERT_ZONE", DEFAULT_ALERT_ZONE)
        ally.CONFORT_ZONE = data.get(map_name, {}).get("CONFORT_ZONE", DEFAULT_CONFORT_ZONE)
        ally.WANDERING_ZONE = data.get(map_name, {}).get("WANDERING_ZONE", DEFAULT_WANDERING_ZONE)

        return ally