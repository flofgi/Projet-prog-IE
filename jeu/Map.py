from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ally import Ally
    from jeu.Item import Item
    from Entity import Entity
    from WorldElement import WorldElement


#from sectors import sector
import pygame
import numpy as np
from Player import Player
from WorldElement import WorldElement
from events import RECUP_EVENT, ALLY_EVENT



class Map :
    def __init__(self,mapsize : tuple, tileset : Tileset, mapset : np.array, worldelements: list[WorldElement] = None): #, sectors: tuple, camera: caméra
        """initialize the map
        Args:
        mapsize(tuple) : the size of the map in tiles
        tileset(Tileset) : an image containing the set of tiles used for the map, with methods to load them into a list of tiles and unload this list
        mapset(np.array) : a table of numbers defining the position of the tiles on the map
        rect(pygame.Rect) : relative position of the window on the screen 
        """
    
        self.mapsize = mapsize
        self.mapset: np.array = mapset
        self.tileset = tileset
        self.worldelements: list[WorldElement] = list(worldelements) if worldelements is not None else []
        #self.sectors = sectors

        h, w = self.mapsize
        self.image = pygame.Surface((self.tileset.getTileSize()[0]*w,self.tileset.getTileSize()[1]*h))
    

      

    def draw(self):
        """draw the map with the tileset and the associated list of tiles"""
        m, n = self.mapset.shape
        for i in range (m):
            for j in range (n):
                tile = self.tileset.tiles[self.mapset[i,j]]
                self.image.blit(tile, (j*self.tileset.getTileSize()[0], i*self.tileset.getTileSize()[1]))
        
    @property
    def get_worldelement(self) -> list[WorldElement]:
        return self.worldelements 

    #def get_sectors():
    #def get_visible_tiles(): 
    #def transfer_entity():

    def update(self, dt: float, events: list[pygame.event.Event], target: Player = None) -> None:
        """Update the worldelements list and update all worldelement from the list"""
        for event in events:
            if event.type == ALLY_EVENT or event.type == RECUP_EVENT:
                if event.dict["target"] in self.worldelements:
                    self.worldelements.remove(event.dict["target"])
        for worldelement in self.worldelements:
            worldelement.update(dt, events, target)
    
    def load(self) -> None:
        """load all worldelemets"""
        for element in self.worldelements:
            element.load()

class Tileset:
    def __init__(self, file, tilesize : tuple, margin=1, spacing=1):
      self.file = file
      self.tilesize = tilesize
      self.margin = margin
      self.spacing = spacing
      self.image = pygame.image.load(file)
      self.tiles = []
      self.load()

    def getTileSize(self):
        return self.tilesize

    def load(self):
      """cut the image containing the tiles into individual tiles in a list"""
      self.tiles = []
      x0 = y0 = self.margin
      w = self.image.width
      h = self.image.height
      dx = self.tilesize[0] + self.spacing
      dy = self.tilesize[1] + self.spacing
      
      for x in range(x0, w, dx):
          for y in range(y0, h, dy):
              tile = pygame.Surface(self.tilesize)
              tile.blit(self.image, (0, 0), (x, y, self.tilesize))
              self.tiles.append(tile)

    def unload(self):
      """Nullify the tile list"""
      for i in range (len(self.tiles)):
        self.tiles[i]=None