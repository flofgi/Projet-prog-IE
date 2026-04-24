from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Ally import Ally
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
from utilitary import RECUP_EVENT, ALLY_EVENT, DEAD, GRENADE_EXPLOSION_EVENT
from WorldElement import WorldElement
from Tileset import Tileset

DEFAULTS_PAWN_POINT = pygame.Vector2(250, 250)


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
        self.spawn_point = DEFAULTS_PAWN_POINT
        self.worldelements: list[WorldElement] = list(worldelements) if worldelements is not None else []
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

