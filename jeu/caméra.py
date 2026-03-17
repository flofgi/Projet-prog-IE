import pygame

class Camera :
  def __init__(self, mapsize, screensize, tilesize, speed : int):
    self.mapsize=mapsize
    self.screensize = screensize   
    self.tilesize = tilesize
    self.speed = speed

    self.x = 0
    self.y = 0
    self.max_x = mapsize[1] * tilesize[0] - screensize[0]
    self.max_y = mapsize[0] * tilesize[1] - screensize[1]

  def update(self, player_pos):
    self.x = player_pos[0] - self.screensize[0]//2
    self.y = player_pos[1] - self.screensize[1]//2
    self.x = max(0, min(self.x, self.max_x))
    self.y = max(0, min(self.y, self.max_y))
  