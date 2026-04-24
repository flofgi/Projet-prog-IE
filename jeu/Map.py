from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jeu.WorldElement.Ally import Ally
    from Item.Item import Item
    from WorldElement.Entity import Entity
    from WorldElement.WorldElement import WorldElement
    from WorldElement.Player import Player
    from Camera import Camera
    from WorldElement.Mob import Mob


#from sectors import sector
import pygame
import numpy as np
from WorldElement.WorldElement import WorldElement
from jeu.utilitary import RECUP_EVENT, ALLY_EVENT, DEAD, GRENADE_EXPLOSION_EVENT


class Map :
    def __init__(self,mapsize : tuple, tileset, mapset : np.array, rect=None, worldelements: list[WorldElement] = None): #, sectors: tuple, camera: caméra
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
        
    @property
    def get_worldelement(self) -> list[WorldElement]:
        return self.worldelements 


    def get_worldelements(self, player: Player = None, d: float = None, type = None):
        """Return world elements filtered by class and optionally by distance to player.

        Args:
            player (Player | None): reference player for distance filtering/sorting.
            d (float | None): max distance from player. If None, no distance filter.
            type (type | tuple[type, ...] | None): class filter used with isinstance.
        """
        elements = self.worldelements

        if type is not None:
            elements = [e for e in elements if isinstance(e, type)]

        if d is None or player is None:
            return elements

        return sorted([e for e in elements if e.distance_to(player) < d],key=lambda e: e.distance_to(player))


    #def get_sectors():
    #def get_visible_tiles(): 
    #def transfer_entity():

    def handle_events(self, event: pygame.event.Event):
        """Check for player-specific events such as item pickup or ally interaction.
        Args:
            events (pygame.event.Event):events to process for interactions.
        """
        for worldelement in self.worldelements:
            worldelement.handle_events(event)

        if event.type == ALLY_EVENT or event.type == RECUP_EVENT or event.type == DEAD:
            if event.target in self.worldelements:
                self.worldelements.remove(event.dict["target"])

        if event.type == GRENADE_EXPLOSION_EVENT:
            for worldelement in self.worldelements:
                if worldelement.is_enemy and worldelement.get_coordinates.distance_to(event.position) < event.radius:
                    worldelement.is_attack(event.damage)
    


    def update(self, dt: float, target: Player = None) -> None:
        """Update the worldelements list and update all worldelement from the list"""
            
        for worldelement in self.worldelements:
            worldelement.update(dt, self, target)


    def load(self) -> None:
        """load all worldelemets"""
        for element in self.worldelements:
            element.load()

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