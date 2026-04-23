import pygame
import Map
from Player import Player


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

    self.x = 0
    self.y = 0
    self.max_x = mapsize[1] * tilesize[0] - windowsize[0]
    self.max_y = mapsize[0] * tilesize[1] - windowsize[1]

  def update(self, player: Player):
    """update the position of the camera following the player's coordinates and the border of the map"""
    self.x = player.get_coordinates[0] - self.scaled_window.get_width()// 2
    self.y = player.get_coordinates[1] - self.scaled_window.get_height()// 2
    self.x = max(0, min(self.x, self.max_x))
    self.y = max(0, min(self.y, self.max_y))
  
  def scaling(self, newscale):
    """update the zoom of the window depending on the scale gived, and redraw the map"""   
    self.coefscale = max(self.min_scale, min(self.max_scale, newscale))
    zoom = (int(self.windowsize[0] * self.coefscale), int(self.windowsize[1] * self.coefscale))
    self.scaled_window = pygame.Surface(zoom)
    #return self.scaled_window.get_size()

  def render(self, map_obj: Map, window):
    self.scaled_window.fill((0,0,50))
    map_obj.draw(self)

    scaled = pygame.transform.scale(self.scaled_window, self.windowsize)
    window.blit(scaled,(0,0))
  
  @property
  def get_position(self):
    return pygame.Vector2(self.x, self.y)