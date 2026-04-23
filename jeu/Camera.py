from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player

import pygame

class Camera :
  def __init__(self, mapsize, screensize, tilesize = (32,32)):
    """initialize the camera who follows the player
    Args:
      mapsize(tuple): the size of the map in tiles
      screensize(tuple): the size of the screen in pixel
      tilesize(tuple): the size of a unique tile in pixel, 32 by 32 by default
    """
    self.mapsize = mapsize
    self.screensize = screensize   
    self.tilesize = tilesize

    self.x = 0
    self.y = 0
    self.max_x = mapsize[1] * tilesize[0] - screensize[0]
    self.max_y = mapsize[0] * tilesize[1] - screensize[1]

  def update(self, player: Player):
    """update the position of the camera following the player's coordinates and the border of the map"""
    self.x = player.get_coordinates.x - self.screensize[0]//2
    self.y = player.get_coordinates.y - self.screensize[1]//2
    self.x = max(0, min(self.x, self.max_x))
    self.y = max(0, min(self.y, self.max_y))
  
  @property
  def get_coordinates(self) -> pygame.Vector2:
    """return the position of the camera as a pygame.Vector2"""
    return pygame.Vector2(self.x, self.y)
  