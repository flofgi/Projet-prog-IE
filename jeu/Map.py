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
from Tileset import Tileset


class Map :
    def __init__(self,mapsize : tuple, tileset : Tileset, mapset : np.array, worldelements: list[WorldElement] = None, rect=None): #, sectors: tuple, camera: caméra
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
        self.worldelements = list(worldelements) if worldelements is not None else []
        #self.sectors = sectors

        h, w = self.mapsize
        tile_w, tile_h = self.tileset.getTileSize
        self.background = pygame.Surface((tile_w*w,tile_h*h))
        self.rect = rect if rect else self.background.get_rect()

      

    def draw(self, camera):
        """draw the affiched map with the tileset and the associated list of tiles"""
        surface = camera.scaled_window
        tile_w, tile_h = self.tileset.getTileSize
    
        start_x = max(0, camera.x//tile_w)
        end_x = min(self.mapsize[1], (surface.get_width()+ camera.x)//tile_w+1)
        start_y = max(0, camera.y//tile_h)
        end_y = min(self.mapsize[0], (surface.get_height()+ camera.y)//tile_h+1)
        
        for i in range (int(start_y), int(end_y)):
            for j in range (int(start_x), int(end_x)):
                if 0<=i<self.mapset.shape[0] and 0<=j<self.mapset.shape[1]:
                    tile = self.tileset.tiles[self.mapset[i,j]]
                    x = j * tile_w - camera.x
                    y = i * tile_h - camera.y
                    surface.blit(tile, (x, y))
  
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

