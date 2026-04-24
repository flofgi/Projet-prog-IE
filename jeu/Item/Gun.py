from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map
    from Camera import Camera

from Item.utilitary import register_item
from Item.base_Item import Item
from WorldElement.Mob import Mob
import pygame
from events import vec_to_list, list_to_vec


DEFAULT_SHOT_DISTANCE = 50
DEFAULT_TOLERANCE = 5
DEFAULT_DAMAGE = 5
FIRE_COOLDOWN_SECONDS = 0.3
TARGET_SCAN_DISTANCE = 60
SHOT_TRACE_DURATION = 0.5
SHOT_COLOR = (255, 0, 0)
SHOT_LINE_WIDTH = 2


@register_item("gun")
class gun(Item):

    def __init__(self, sprites, coordinates, durability = None, be_stackable = False, shot_distance: int = DEFAULT_SHOT_DISTANCE, tolerance: int = DEFAULT_TOLERANCE, damage: float = DEFAULT_DAMAGE):
        super().__init__(sprites, coordinates, durability, be_stackable)
        self.shot_distance = shot_distance
        self.tolerance = tolerance
        self.damage = damage
        self.list_shots: list[tuple[int, pygame.Vector2, pygame.Vector2]] = []

    def use(self, player: Player, map: Map):
        if self.list_shots and self.animation_time - self.list_shots[-1][0] < FIRE_COOLDOWN_SECONDS:
            return
        mobs: list[Mob] = map.get_worldelements(player, TARGET_SCAN_DISTANCE, Mob)
        mouse = pygame.Vector2(pygame.mouse.get_pos()) + player.camera.get_coordinates
        shot =  mouse - player.get_coordinates
        shot.normalize_ip()
        shot.scale_to_length(self.shot_distance)
        self.list_shots.append((self.animation_time, player.get_coordinates, shot))
        for mob in mobs:
            if self.point_in_segment(mob.get_coordinates, mouse, player.get_coordinates):
                mob.is_attack(self.damage)
        if self.durability is not None:
            self.durability -= 1
    
    def point_in_segment(self, point: pygame.Vector2, mouse_point: pygame.Vector2, player_position: pygame.Vector2) -> bool:
        """Check if a point is within a certain distance from the line segment defined by the player's position and the mouse position.
        This is used to determine if a mob is hit by the gunshot.
        Args:
            point (pygame.Vector2): The position of the mob to check.
            mouse_point (pygame.Vector2): The position of the mouse cursor.
            player_position (pygame.Vector2): The position of the player.
        
        Returns:
            bool: True if the point is within the tolerance distance from the line segment, False otherwise.
        """
        normalised_mouse_point = (mouse_point - player_position).normalize() * self.shot_distance + player_position
        return bool(self.rect.clipline(player_position, normalised_mouse_point))
        

    def draw_equip(self, screen: pygame.Surface, camera: Camera, player: Player = None):
        for shot_parameter in self.list_shots:
            dt, player_position, shot = shot_parameter
            if self.animation_time - dt > SHOT_TRACE_DURATION:
                self.list_shots.remove(shot_parameter)
            else:
                end_point = player_position + shot
                pygame.draw.line(screen, SHOT_COLOR, player_position - camera.get_coordinates, end_point - camera.get_coordinates, SHOT_LINE_WIDTH)

    def update(self, dt, map, target = None):
        self.animation_time += dt

    def save(self) -> dict:
        data = super().save()
        data.update(
            {
                "shot_distance": self.shot_distance,
                "tolerance": self.tolerance,
                "damage": self.damage,
                "list_shots": [
                    {
                        "time": shot[0],
                        "player_position": [shot[1].x, shot[1].y],
                        "shot": [shot[2].x, shot[2].y],
                    }
                    for shot in self.list_shots
                ],
            }
        )
        return data
    
    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> gun:
        """Create a gun instance from saved data.
        
        Args:
            data (dict): A dictionary containing the gun's saved state, including shot distance, tolerance, damage, and list of shots.
            map_name (str, optional): The name of the map to load coordinates from. Defaults to None.
        """
        gun_instance = self(
            sprites=data.get("sprites", []),
            coordinates=list_to_vec(data.get(map_name, {}).get("coordinates", None)),
            durability=data.get("durability", None),
            be_stackable=data.get("be_stackable", False),
            shot_distance=data.get("shot_distance", DEFAULT_SHOT_DISTANCE),
            tolerance=data.get("tolerance", DEFAULT_TOLERANCE),
            damage=data.get("damage", DEFAULT_DAMAGE)
        )
        gun_instance.animation_time = data.get("animation_time", 0)
        gun_instance.list_shots = [
            (
                shot_data["time"],
                list_to_vec(shot_data["player_position"]),
                list_to_vec(shot_data["shot"])
            )
            for shot_data in data.get("list_shots", [])
        ]
        return gun_instance