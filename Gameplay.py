from __future__ import annotations

import numpy as np
import pygame

from Camera import Camera
from Map import Map, Tileset
from States.State import State
from States.StateManager import StateManager
from WorldElement.Player import Player
from Item import gun, sword
from events import KEYS, NEW_MAP, STATE_PUSH, STATE_POP, STATE_REPLACE



class Gameplay(State):
    """Playable state with two simple test maps."""

    def __init__(self, state_manager: StateManager, initial_map: str = "Map1"):
        super().__init__(state_manager)
        self.initial_map = initial_map

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["inventory"]:
                pygame.event.post(pygame.event.Event(STATE_PUSH, state="inventory"))
            
            elif event.key == KEYS["escape"]:
                pygame.event.post(pygame.event.Event(STATE_POP))

        if event.type == NEW_MAP:
            self.load_new_map(event.map_name)

        self.current_map.handle_events(event)
        self.player.handle_events(event)

    def load(self):
        screen_size = pygame.display.get_surface().get_size()

        self.maps: dict[str, Map] = {
            "Map1": Map(
                (20, 30),
                MAP_TILESET,
                MAP1_SET,
                spawn_point=pygame.Vector2(240, 215),
            ),
        }

        if self.initial_map not in self.maps:
            self.initial_map = "Map1"

        self.current_map = self.maps[self.initial_map]
        self.cameras: dict[str, Camera] = {
            map_name: Camera(map_data.mapsize, screen_size)
            for map_name, map_data in self.maps.items()
        }
        self.current_camera = self.cameras[self.initial_map]

        self.player = Player(
            100,
            ["Design/Hunter_Stand_DB_1.png"],
            pygame.Vector2(self.current_map.spawn_point),
            self.current_camera,
        )

        self.current_map.load()
        self.player.load(self.current_map)

    def update(self, dt: float):
        self.player.update(dt, self.current_map)
        self.current_map.update(dt, self.player)
        self.current_camera.update(self.player)

    def render(self, screen: pygame.Surface):
        screen.fill((25, 30, 40))

        self.current_map.draw()
        screen.blit(
            self.current_map.image,
            self.current_map.rect,
            (
                self.current_camera.x,
                self.current_camera.y,
                screen.get_width(),
                screen.get_height(),
            ),
        )

        render_list = self.current_map.get_worldelement + [self.player] + self.player.get_allies
        render_list.sort(key=lambda e: e.get_rect.bottom)

        for element in render_list:
            if not element.sprite:
                continue
            rect = element.get_rect.move(-self.current_camera.x, -self.current_camera.y)
            screen.blit(element.sprite[0], rect)

    def load_new_map(self, map_name: str):
        """Load a new map and update player/camera links."""
        if map_name not in self.maps:
            return

        self.current_map = self.maps[map_name]
        self.current_map.load()
        self.current_camera = self.cameras[map_name]
        self.player.camera = self.current_camera
        self.player.map = self.current_map
        self.player.get_coordinates = self.current_map.spawn_point

    def load_save(self, save_data: str):
        """Placeholder save-loading hook."""
        pass


MAP_TILESET = Tileset(
    "Design\Tileset\Gemini_Generated_Image_b20ktbb20ktbb20k.png",
    tilesize=(122, 126),
    margin=8,
    spacing=5,
)

MAP1_SET = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
        [0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3, 3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3, 3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    dtype=int,
)

MAP2_SET = np.array(
    [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3],
        [3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 0, 2, 2, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 0, 2, 2, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 1, 0, 2, 0, 1, 0, 3, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    dtype=int,
)