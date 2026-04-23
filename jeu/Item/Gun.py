from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player
    from Map import Map
    from Camera import Camera

from Item.Item import Item
from WorldElement.Mob import Mob
import pygame

class gun(Item):

    def __init__(self, sprites, coordinates, durability = None, be_stackable = False, shot_distance: int = 50, tolerance: int = 5, damage: float = 5):
        super().__init__(sprites, coordinates, durability, be_stackable)
        self.shot_distance = shot_distance
        self.tolerance = tolerance
        self.damage = damage
        self.list_shots: list[tuple[int, pygame.Vector2, pygame.Vector2]] = []

    def use(self, player: Player, map: Map):
        if self.list_shots and self.animation_time - self.list_shots[-1][0] < 0.3:
            return
        mobs: list[Mob] = map.get_worldelements(player, 60, Mob)
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
            if self.animation_time - dt > 0.5:
                self.list_shots.remove(shot_parameter)
            else:
                end_point = player_position + shot
                pygame.draw.line(screen, (255, 0, 0), player_position - camera.get_coordinates, end_point - camera.get_coordinates, 2)    

    def update(self, dt, map, target = None):
        self.animation_time += dt