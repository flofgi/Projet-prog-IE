from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Map import Map
    from WorldElement.Player import Player, WorldElement, Mob


from .base_Item import Item
from .utilitary import register_item
import pygame
from Camera import Camera
from events import vec_to_list, list_to_vec


DEFAULT_SWORD_DAMAGE = 3
DEFAULT_SWORD_DURABILITY = 50
DEFAULT_MOUSE_POSITION = pygame.Vector2(0, 0)
DEFAULT_SWING_DURATION = 0.4
HAND_SWORD_SPRITES = ["hand"]
HAND_SWORD_ANGLE = 45
HAND_SWORD_DISTANCE = 64
SWING_COLOR = (200, 200, 200)
SWING_LINE_WIDTH = 2


@register_item("sword")
class sword(Item):

    def __init__(self, sprites, coordinates, shot_angle: float, shot_distance: float, damage: float = DEFAULT_SWORD_DAMAGE, durability = DEFAULT_SWORD_DURABILITY, be_stackable = False):
        super().__init__(sprites, coordinates, durability, be_stackable)
        self.shot_angle = shot_angle
        self.shot_distance = shot_distance
        self.damage = damage
        self.animation_time = 0
        self.is_used = False
        self.mouse_position = DEFAULT_MOUSE_POSITION.copy()
        self.animation = DEFAULT_SWING_DURATION

    @staticmethod
    def hand():
        """Return a default hand item for the player when no item is equipped."""
        return sword(HAND_SWORD_SPRITES, None, HAND_SWORD_ANGLE, HAND_SWORD_DISTANCE, durability=None, be_stackable=False)


    def use(self, player: Player, map: Map):
        if self.is_used:
            return

        self.is_used = True
        self.animation_time = 0
        if self.durability is not None:
            self.durability -= 1
            if self.durability <= 0:
                player.inventory.remove_item(self)

        mobs: list[Mob] = map.mobs
        for mob in mobs:
            if self.in_cone(player, mob):
                mob.is_attack(self.damage)

    def in_cone(self, player: Player, target: pygame.Vector2 | WorldElement):
        """Check if a target is within the sword's attack cone."""
        self.mouse_position = pygame.Vector2(pygame.mouse.get_pos()) + player.camera.get_coordinates
        if not(isinstance(target, pygame.Vector2)):
            target = target.get_coordinates
        position = player.get_coordinates

        normalised_target = target - position
        mouse_target_angle = normalised_target.angle_to(self.mouse_position - position)
        return abs(mouse_target_angle) < self.shot_angle/2 and target.distance_to(position) < self.shot_distance

    def draw_equip(self, surface: pygame.Surface, camera: Camera, player: Player) -> None:
        if not self.is_used:
            return

        position = player.get_coordinates
        normalised_mouse = self.mouse_position - position
        if normalised_mouse.length() == 0:
            return

        normalised_mouse.normalize_ip()
        normalised_mouse.scale_to_length(self.shot_distance)
        start_mouse_pos = normalised_mouse.rotate(-self.shot_angle/2)
        end_point = position + start_mouse_pos.rotate(self.shot_angle/self.animation*self.animation_time)

        screen_start = position - camera.get_coordinates
        screen_end = end_point - camera.get_coordinates
        pygame.draw.line(surface, SWING_COLOR, screen_start, screen_end, SWING_LINE_WIDTH)

    def update(self, dt, map, target = None):
        self.animation_time += dt
        if self.animation_time > self.animation:
            self.is_used = False

    def save(self) -> dict:
        data = super().save()
        data.update(
            {
                "shot_angle": self.shot_angle,
                "shot_distance": self.shot_distance,
                "damage": self.damage,
                "is_used": self.is_used,
                "animation": self.animation,
            }
        )
        return data
    
    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> sword:
        """Create a sword instance from saved data.
        
        Args:
            data (dict): A dictionary containing the sword's saved state, including shot angle, shot distance, damage, usage state, and animation duration.
            map_name (str, optional): The name of the map to load coordinates from. Defaults to None.
        """
        sword_instance = self(
            sprites=data.get("sprites", []),
            coordinates=list_to_vec(data.get(map_name, {}).get("coordinates", None)),
            shot_angle=data.get("shot_angle", HAND_SWORD_ANGLE),
            shot_distance=data.get("shot_distance", HAND_SWORD_DISTANCE),
            damage=data.get("damage", DEFAULT_SWORD_DAMAGE),
            durability=data.get("durability", DEFAULT_SWORD_DURABILITY),
            be_stackable=data.get("be_stackable", False)
        )
        sword_instance.is_used = data.get("is_used", False)
        sword_instance.animation = data.get("animation", DEFAULT_SWING_DURATION)

        return sword_instance