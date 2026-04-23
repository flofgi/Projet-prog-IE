from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    
    from jeu import Map
    from jeu.WorldElement.Mob import Mob
    from jeu.WorldElement.Mob import Player

import pygame
from Item.Item import Item
from events import GRENADE_EXPLOSION_EVENT


class Grenade(Item):
    def __init__(self, sprites: list[str], coordinates: pygame.Vector2, radius: int = 100, damage: int = 50):
        super().__init__(sprites, coordinates, durability=None, be_stackable=True)
        self.be_stackable = True
        self.radius = radius
        self.damage = damage
        self.max_radius = 200

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
        