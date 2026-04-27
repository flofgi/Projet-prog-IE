from __future__ import annotations

import json
import os
from random import randint

import numpy as np
import pygame

from Camera import Camera
from Map import Map
from States.State import State
from States.StateManager import StateManager
from WorldElement.Player import Player
from utilitary import KEYS, read_json, vec_to_list, list_to_vec



INTERACT_RANGE = 50
PLAYER_HP = 100
PLAYER_SPAWN = pygame.Vector2(250, 250)
ALLY_COUNT = 10
MOB_COUNT = 10
ITEM_SPAWN_COUNT = 20
RANDOM_SPAWN_MIN = pygame.Vector2(100, 100)
RANDOM_SPAWN_MAX = pygame.Vector2(400, 400)
SWORD_ANGLE = 90
SWORD_RANGE = 50
BACKGROUND_COLOR = (0, 0, 50)

TILESIZE =  (32, 32)
MAPSIZE = pygame.Vector2(30, 40)
TILESET = "Design/Tileset/MAP1_tileset.png"
DEFAULT_MAPSET_PATH = "assets/mapset_test.txt"
DEFAULT_PLAYER_SPRITE = "Design/Hunter_Stand_DB_1.png"


def random_spawn_position() -> pygame.Vector2:
    return pygame.Vector2(
        randint(int(RANDOM_SPAWN_MIN.x), int(RANDOM_SPAWN_MAX.x)),
        randint(int(RANDOM_SPAWN_MIN.y), int(RANDOM_SPAWN_MAX.y)),
    )


class Gameplay(State):
    """Playable state with save/load support."""

    def __init__(self, state_manager: StateManager, game_name: str, first_map_name: str):
        super().__init__(state_manager)
        self.game_name = game_name
        self.first_map = first_map_name
        self.initmaps = []
        self.map: Map | None = None
        self.camera: Camera | None = None
        self.player: Player | None = None

        if os.path.exists("assets/saves/init/map"):
            for files in os.listdir("assets/saves/init/map"):
                if files.endswith(".json"):
                    self.initmaps.append(files[:-5])

        self.maps = []

        os.makedirs(f"assets/saves/{self.game_name}/map", exist_ok=True)
        for files in os.listdir(f"assets/saves/{self.game_name}/map"):
            if files.endswith(".json"):
                self.maps.append(files[:-5])


    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["inventory"]:
                self.player.open_inventory()
            elif event.key == KEYS["escape"]:
                self.save()
                pygame.event.post(pygame.event.Event(pygame.QUIT, state="quit"))
            elif event.key == KEYS["interact"]:
                for element in self.map.get_worldelements(self.player, INTERACT_RANGE):
                    if element.interact(self.player):
                        continue

        self.map.handle_events(event)
        self.player.handle_events(event)

    def load(self):
        """Load gameplay from saved map if available, otherwise from init map."""
        if self.player is None:
            player_data = read_json(f"assets/saves/{self.game_name}/player.json") or {}
            if player_data:
                self.player = Player.load_from_data(player_data, self.first_map)
            else:
                init_data = read_json("assets/saves/init/player.json") or {}
                self.player = Player.load_from_data(init_data, self.first_map)

        if self.first_map not in self.maps:
            self.load_new_map(self.first_map)
        else:
            self.load_map(self.first_map)

    def update(self, dt: float):
        self.player.update(dt, self.map)
        self.map.update(dt, self.player)
        self.camera.update(self.player)

    def render(self, screen: pygame.Surface):
        self.camera.scaled_window.fill(BACKGROUND_COLOR)
        self.map.draw(self.camera)

        render_list = self.map.get_worldelement + [self.player] + self.player.get_allies
        render_list.sort(key=lambda e: e.get_rect.bottom)

        for element in render_list:
            if not element.sprite:
                continue
            element.draw(self.camera.scaled_window, self.camera, self.player)

        self.camera.render(screen)

    def handle_collision(self):
        """Placeholder collision-handling hook."""
        self.map.handle_collisions(self.player)

    def unload(self):
        self.save()

    def save(self) -> None:
        """Save current map/player state without losing data from other maps."""
        if self.map is None or self.player is None or self.camera is None:
            return

        save_dir = f"assets/saves/{self.game_name}"
        os.makedirs(f"{save_dir}/map", exist_ok=True)

        player_data = read_json(f"{save_dir}/player.json") or {}

        self.map.save(self.camera, self.game_name)
        player_data = self.player.save(self.map.name, player_data)

        with open(f"{save_dir}/player.json", "w", encoding="utf-8") as f:
            json.dump(player_data, f, indent=4)


    def load_new_map(self, map_name: str):

        if map_name not in self.initmaps:
            raise ValueError(f"Map '{map_name}' not found in initial maps. Available maps: {self.initmaps}")

        if self.map is not None:
            self.map.save(self.camera, self.game_name)

        map_data = read_json(f"assets/saves/init/map/{map_name}.json")
        self.map, self.camera = Map.load_from_data(map_data, map_name, "assets/saves/init/map/")
        
        self.map.load()

        player_data = read_json(f"assets/saves/{self.game_name}/player.json") or {}
        allies = getattr(self.player, "allies", None)
        inventory = getattr(getattr(self.player, "inventory", None), "items", None)
        self.player.load(self.map, self.camera, allies, inventory)
        self.player.load_map(self.map, self.camera, player_data)
    
    def load_map(self, map_name: str):
        """Load a previously saved map state."""
        if map_name not in self.maps:
            self.load_new_map(map_name)
            return
        else:
            map_path = f"assets/saves/{self.game_name}/map/"
        
        if self.map is not None:
            self.map.save(self.camera, self.game_name)

        map_data = read_json(f"{map_path}{map_name}.json")

        self.map, self.camera = Map.load_from_data(map_data, map_name, map_path)
        
        self.map.load()

        player_data = read_json(f"assets/saves/{self.game_name}/player.json") or {}
        allies = getattr(self.player, "allies", None)
        inventory = getattr(getattr(self.player, "inventory", None), "items", None)
        self.player.load(self.map, self.camera, allies, inventory)
        self.player.load_map(self.map, self.camera, player_data)

    def load_save(self, map_name: str):
        """Compatibility wrapper for old callsites."""
        self.load_map(map_name)