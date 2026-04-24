from __future__ import annotations
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WorldElement.Ally import Ally
    from Item.base_Item import Item
    from WorldElement.Entity import Entity
    from WorldElement.WorldElement import WorldElement
    from WorldElement.Player import Player
    from Camera import Camera
    from WorldElement.Mob import Mob


#from sectors import sector
import pygame
import numpy as np
from pathlib import Path
from WorldElement.WorldElement import WorldElement
from utilitary import RECUP_EVENT, ALLY_EVENT, DEAD, GRENADE_EXPLOSION_EVENT, vec_to_list
from WorldElement import WorldElement
from Tileset import Tileset
from Item.utilitary import ITEM_REGISTRY


DEFAULTS_PAWN_POINT = pygame.Vector2(250, 250)


class Map :
    def __init__(self,mapsize : tuple, tileset, mapset : np.array, name: str, rect=None): #, sectors: tuple, camera: caméra
        """initialize the map
        Args:
        mapsize(tuple) : the size of the map in tiles
        tileset(Tileset) : an image containing the set of tiles used for the map, with methods to load them into a list of tiles and unload this list
        mapset(np.array) : a table of numbers defining the position of the tiles on the map
        rect(pygame.Rect) : relative position of the window on the screen 
        """
    
        self.mapsize = mapsize
        self.mapset: np.array = mapset
        self.tileset: Tileset = tileset
        self.spawn_point = DEFAULTS_PAWN_POINT
        self.name = name
        self.allies: list[Ally] = []
        self.items: list[Item] = []
        self.mobs: list[Mob] = []
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
        return self.allies + self.items + self.mobs


    def get_worldelements(self, player: Player = None, d: float = None, type = None):
        """Return world elements filtered by class and optionally by distance to player.

        Args:
            player (Player | None): reference player for distance filtering/sorting.
            d (float | None): max distance from player. If None, no distance filter.
            type (type | tuple[type, ...] | None): class filter used with isinstance.
        """
        elements = self.get_worldelement

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
        for worldelement in self.get_worldelement:
            worldelement.handle_events(event)

        if event.type == ALLY_EVENT:
            self.allies.remove(event.target)
        
        if event.type == RECUP_EVENT:
            if event.target in self.items:
                self.items.remove(event.target)
        
        if event.type == DEAD:
            if event.target in self.mobs:
                self.mobs.remove(event.target)
            elif event.target in self.allies:
                self.allies.remove(event.target)


        if event.type == GRENADE_EXPLOSION_EVENT:
            for mob in self.mobs:
                if mob.get_coordinates.distance_to(event.position) <= event.radius:
                    mob.is_attack(event.damage)
    


    def update(self, dt: float, target: Player = None) -> None:
        """Update the worldelements list and update all worldelement from the list"""
            
        for worldelement in self.get_worldelement:
            worldelement.update(dt, self, target)


    def load(self) -> None:
        """load all worldelemets"""
        for element in self.get_worldelement:
            element.load()

    def save(self, camera: Camera, game_name: str) -> dict:
        """Return a dictionary representing the map's current state for saving."""
        folder = Path(f"assets/saves/{game_name}")
        folder.mkdir(parents=True, exist_ok=True)

        np.savetxt(f"assets/saves/{game_name}/{self.name}_mapset.txt", self.mapset, fmt="%d")
        
        world_data = {
            "map_name": self.name,
            "spawn_point": vec_to_list(self.spawn_point),
            "Tileset": self.tileset.save(),
            "worldelements": {
                "ally": [ally.save(self.name) for ally in self.allies],
                "item": [item.save() for item in self.items],
                "mob": [mob.save() for mob in self.mobs]
                },
            "camera": camera.save()
        
        }

        with open(f"assets/saves/{game_name}/{self.name}.json", "w", encoding="utf-8") as f:
            json.dump(world_data, f, indent=4)
        

    
    @classmethod
    def load_from_data(self, data: dict, game_name: str, map_name: str) -> Map:
        """Create a Map instance from saved data.
        
        Args:
            data (dict): A dictionary containing the map's saved state, including spawn point and world elements.
        """
        spawn_point = pygame.Vector2(data.get("spawn_point", [0, 0]))

        mapsize = data.get("Mapsize", (0, 0))
        mapset = np.loadtxt(f"assets/tilesets/{map_name}_mapset.txt", dtype=int) 
        
        tileset = Tileset.load_from_data(data.get("Tileset", {}))
        name = data.get("Map_name")
        map = Map(mapsize, tileset, mapset, name)
        map.spawn_point = spawn_point

        worldelements_data: dict[str, list[dict]] = data.get("worldelements", [])
        for element_data in worldelements_data.get("ally", []):
            element = Ally.load_from_data(element_data)
            map.allies.append(element)

        for element_data in worldelements_data.get("item", []):
            element = Item.load_from_data(element_data)
            item_class = ITEM_REGISTRY.get(element_data.get("type"))

            element = item_class.load_from_data(element_data.get("item", {}))
            map.items.append(element)
        
        for element_data in worldelements_data.get("mob", []):
            element = Mob.load_from_data(element_data)
            map.mobs.append(element)

        return map



