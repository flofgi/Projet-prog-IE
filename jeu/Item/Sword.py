from Item.Item import Item
from WorldElement.Player import Player
from WorldElement.WorldElement import WorldElement
from WorldElement.Mob import Mob
from Map import Map
import pygame
import math


class sword(Item):

    def __init__(self, sprites, coordinates, shot_angle: float, shot_distance: float, domage: float = 3, durability = 50, be_stackable = False):
        super().__init__(sprites, coordinates, durability, be_stackable)
        self.shot_angle = shot_angle
        self.shot_distance = shot_distance
        self.domage = domage


    def use(self, player: Player, map: Map):
        mobs: list[Mob] = map.get_worldelements(player, self.shot_distance, Mob)
        for mob in mobs:
            if self.in_cone(player, mob):
                mob.is_attack(self.domage)

    def in_cone(self, player: Player, target: pygame.Vector2 | WorldElement):
        """Check if a target is within the sword's attack cone."""
        mouse = pygame.Vector2(pygame.mouse.get_pos())
        if isinstance(target, WorldElement):
            target = target.get_coordinates
        position = player.get_coordinates

        normalised_target = target + pygame.Vector2(player.camera.x, player.camera.y) - position
        mouse_target_angle = normalised_target.angle_to(mouse - position)
        return abs(mouse_target_angle) < self.shot_angle/2 and target.distance_to(position) < self.shot_distance



