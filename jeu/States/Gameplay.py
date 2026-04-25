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
RANDOM_SPAWN_MAX = pygame.Vector2(150, 150)
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
        self.player: Player
        self.map: Map
        self.camera: Camera

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
        screen_size = pygame.display.get_surface().get_size()
        
        if not os.path.exists(f"assets/saves/{self.game_name}"):
            self.load_new_map(self.first_map)


            os.makedirs(f"assets/saves/{self.game_name}")
        else:
            self.load_map(self.first_map)
        

    def update(self, dt: float):
        self.player.update(dt, self.map)
        self.map.update(dt, self.player)
        self.camera.update(self.player)

    def render(self, screen: pygame.Surface):
        screen.fill(BACKGROUND_COLOR)

        self.map.draw()
        screen.blit(
            self.map.image,
            self.map.rect,
            (
                self.camera.x,
                self.camera.y,
                screen.get_width(),
                screen.get_height(),
            ),
        )

        render_list = self.map.get_worldelement + [self.player] + self.player.get_allies
        render_list.sort(key=lambda e: e.get_rect.bottom)

        for element in render_list:
            if not element.sprite:
                continue
            element.draw(screen, self.camera, self.player)

    def handle_collision(self):
        """Placeholder collision-handling hook."""
        self.map.handle_collisions(self.player)


    def load_new_map(self, map_name: str):
        if map_name not in self.maps:
            return
        if self.map.name == map_name:
            return
        if self.map:
            self.map.save(self.camera, self.game_name)

        map_data = read_json(f"assets/maps/{map_name}.json")

        self.map = Map.load_map(map_data, self.game_name, map_name)
        self.camera = Camera(self.map.mapsize, pygame.display.get_surface().get_size(), TILESIZE)
        
        self.map.load()

        player_data = read_json(f"assets/saves/{self.game_name}/player.json")
        coordinates = list_to_vec(player_data.get(map_name, {}).get("coordinates", vec_to_list(self.map.spawn_point)))

        self.player.load_new_map(self.map, self.camera, coordinates)
    

    def load_save(self, map_name: str):
        """Placeholder save-loading hook."""
        player_data = read_json(f"assets/saves/{self.game_name}/player.json")
        world_data = read_json(f"assets/saves/{self.game_name}/{map_name}.json")

        self.Map = Map.load_from_data(world_data, self.game_name, map_name)
        self.Player = Player.load_from_data(player_data, map_name)
        

    def save(self) -> None:
        """Save current map/player state without losing data from other maps."""
        save_dir = f"assets/saves/{self.game_name}"
        os.makedirs(save_dir, exist_ok=True)
        player_data = read_json(f"assets/saves/{self.game_name}/player.json") or {}

        self.map.save(self.camera, self.game_name)
        player_data = self.player.save(self.map.name, player_data)

        with open(f"assets/saves/{self.game_name}/player.json", "w", encoding="utf-8") as f:
            json.dump(player_data, f, indent=4)
