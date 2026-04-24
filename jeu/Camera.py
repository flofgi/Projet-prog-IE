from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Player import Player

import pygame


class Camera :
  def __init__(self, mapsize, windowsize, tilesize = (32,32), coefscale=1.0):
    """initialize the camera who follows the player
    Args:
      window(py.display): the window of the game
      mapsize(tuple): the size of the map in tiles
      windowsize(tuple): the size of the window in pixel
      tilesize(tuple): the size of a unique tile in pixel, 32 by 32 by default
      scale(int): zoom coefficient
    """
    self.mapsize = mapsize
    self.windowsize = windowsize   
    self.tilesize = tilesize

    self.scaled_window = pygame.Surface(self.windowsize)
    self.max_scale = 2
    self.min_scale = 0.04
    self.coefscale = coefscale

    self.zoomsize = self.windowsize
    self.x = 0
    self.y = 0

  def update(self, player: Player):
    """update the position of the camera following the player's coordinates and the border of the map"""
    self.max_x = max(0,self.mapsize[1] * self.tilesize[0] - self.zoomsize[0])
    self.max_y = max(0,self.mapsize[0] * self.tilesize[1] - self.zoomsize[1])
    self.x = max(0, min(player.get_coordinates[0] - self.zoomsize[0]// 2, self.max_x))
    self.y = max(0, min(player.get_coordinates[1] - self.zoomsize[1]// 2, self.max_y))


  @property
  def get_coordinates(self) -> pygame.Vector2:
    """return the position of the camera as a pygame.Vector2"""
    return pygame.Vector2(self.x, self.y)
  

  def scaling(self, newscale):
    """update the zoom of the window depending on the scale gived, and redraw the map"""   
    self.coefscale = max(self.min_scale, min(self.max_scale, newscale))
    self.zoomsize = (int(self.windowsize[0] * self.coefscale), int(self.windowsize[1] * self.coefscale))
    self.scaled_window = pygame.Surface(self.zoomsize)
    self.scaled_window.fill((0,0,50))


  def render(self, window):
    scaled = pygame.transform.scale(self.scaled_window, self.windowsize)
    window.blit(scaled,(0,0))
  
  @property
  def get_coordinates(self):
    return pygame.Vector2(self.x, self.y)
  
  @property
  def rect(self):
    return pygame.Rect(self.x, self.y, self.zoomsize[0], self.zoomsize[1])
  def save(self) -> dict:
    """save the camera's position and relevant attributes for serialization."""
    return {
        "x": self.x,
        "y": self.y,
    }
