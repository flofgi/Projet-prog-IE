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

  def update(self, player):
    """update the position of the camera following the player's coordinates and the border of the map"""
    self.x = player.getPosition()[0] - self.screensize[0]//2
    self.y = player.getPosition()[1] - self.screensize[1]//2
    self.x = max(0, min(self.x, self.max_x))
    self.y = max(0, min(self.y, self.max_y))
  