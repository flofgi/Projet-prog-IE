from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    
    from jeu import Map
    from WorldElement.Mob import Mob
    from WorldElement.Mob import Player

import pygame
from Item.Item import Item
from Item.utilitary import register_item
from utilitary import GRENADE_EXPLOSION_EVENT, vec_to_list, list_to_vec


DEFAULT_GRENADE_RADIUS = 100
DEFAULT_GRENADE_DAMAGE = 50
DEFAULT_MAX_EXPLOSION_RADIUS = 200
DEFAULT_ANIMATION_TIME = 0

@register_item("grenade")
class grenade(Item):
    def __init__(self, sprites: list[str], coordinates: pygame.Vector2, radius: int = DEFAULT_GRENADE_RADIUS, damage: int = DEFAULT_GRENADE_DAMAGE):
        super().__init__(sprites, coordinates, durability=None, be_stackable=True)
        self.be_stackable = True
        self.radius = radius
        self.damage = damage
        self.max_radius = DEFAULT_MAX_EXPLOSION_RADIUS

    def use(self, player: Player, map: Map):
        """Use the grenade, affecting nearby mobs and posting a RECUP_EVENT.
        
        Args:
            player (Player): The player using the grenade.
            map (Map): The map on which the grenade is used.
        """
        mouse_pos = pygame.mouse.get_pos() + player.camera.get_coordinates

        affected_mobs: list[Mob] = self.get_mobs(player, map, distance=self.radius+self.max_radius)
        
        for mob in affected_mobs:
            if mob.get_coordinates.distance_to(mouse_pos) <= self.radius:
                mob.is_attack(self.damage)

        pygame.event.post(
            pygame.event.Event(
                GRENADE_EXPLOSION_EVENT,
                {
                    "position": pygame.Vector2(mouse_pos),
                    "radius": self.radius,
                    "damage": self.damage
                },
            )
        )

    def save(self, map_name: str, data: dict = {}) -> dict:
        data = super().save(map_name, data)
        data.update(
            {
                "radius": self.radius,
                "damage": self.damage,
                "max_radius": self.max_radius,
            }
        )
        return data
    
    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> grenade:
        """Create a Grenade instance from saved data.
        
        Args:
            data (dict): A dictionary containing the grenade's saved state, including radius, damage, and position.
            map_name (str, optional): The name of the map to retrieve coordinates from. Defaults to None.
        """
        coordinates_data = data.get(map_name, {}).get("coordinates", data.get("coordinates", [0, 0]))

        grenade = self(
            sprites=data.get("sprites", []),
            coordinates=list_to_vec(coordinates_data),
            radius=data.get("radius", DEFAULT_GRENADE_RADIUS),
            damage=data.get("damage", DEFAULT_GRENADE_DAMAGE)
        )
        grenade.max_radius = data.get("max_radius", DEFAULT_MAX_EXPLOSION_RADIUS)
        grenade.animation_time = data.get("animation_time", DEFAULT_ANIMATION_TIME)

        return grenade
        