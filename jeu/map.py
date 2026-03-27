#from sectors import sector
import pygame
import numpy as np

class Map :
    def __init__(self,mapsize : tuple, tileset, mapset : np.array, rect=None): #, sectors: tuple
      
      """initialize the map
      Args:
        mapsize(tuple) : the size of the map in tiles
        tileset(Tileset) : an image containing the set of tiles used for the map, with methods to load them into a list of tiles and unload this list
        mapset(np.array) : a table of numbers defining the position of the tiles on the map
        rect(pygame.Rect) : relative position of the window on the screen 
      """
      self.mapsize = mapsize
      self.mapset = mapset
      self.tileset = tileset
      #self.sectors = sectors
      h, w = self.mapsize
      self.image = pygame.Surface((32*w,32*h))
      if rect :
        self.rect = pygame.Rect(rect)
      else :
        self.rect = self.image.get_rect()
      

    def draw(self):
      """draw the map with the tileset and the associated list of tiles"""
      m, n = self.mapset.shape
      for i in range (m):
        for j in range (n):
            tile = self.tileset.tiles[self.mapset[i,j]]
            self.image.blit(tile, (j*32,i*32))
    

    #def get_sectors():
    #def get_visible_tiles(): 
    #def transfer_entity():
    
class Tileset:
    def __init__(self, file, tilesize=(32, 32), margin=1, spacing=1):
      self.file = file
      self.tilesize = tilesize
      self.margin = margin
      self.spacing = spacing
      self.image = pygame.image.load(file)
      self.rect = self.image.get_rect()
      self.tiles = []
      self.load()

    def load(self):
      """cut the image containing the tiles into individual tiles in a list"""
      self.tiles = []
      x0 = y0 = self.margin
      w, h = self.rect.size
      dx = self.tilesize[0] + self.spacing
      dy = self.tilesize[1] + self.spacing
      
      for x in range(x0, w, dx):
          for y in range(y0, h, dy):
              tile = pygame.Surface(self.tilesize)
              tile.blit(self.image, (0, 0), (x, y, *self.tilesize))
              self.tiles.append(tile)

    def unload(self):
      """Nullify the tile list"""
      for i in range (len(self.tiles)):
        self.tiles[i]=None