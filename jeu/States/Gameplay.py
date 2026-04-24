from __future__ import annotations

import numpy as np
import pygame

from Camera import Camera
from Map import Map, Tileset
from States.State import State
from States.StateManager import StateManager
from WorldElement.Player import Player
from Item.Gun import gun
from Item.Sword import sword
from events import KEYS, STATE_PUSH, STATE_POP, STATE_REPLACE
from WorldElement.Ally import Ally
from WorldElement.Mob import Mob
from Item import Item
from random import randint


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
BACKGROUND_COLOR = (25, 30, 40)

TILESIZE =  (32, 32)
MAPSIZE = pygame.Vector2(30, 40)
WINDOWSIZE = pygame.Vector2(800, 800)
SPEED = 3
TILESET = "Design/Tileset/MAP1_tileset.png"


def random_spawn_position() -> pygame.Vector2:
    return pygame.Vector2(
        randint(int(RANDOM_SPAWN_MIN.x), int(RANDOM_SPAWN_MAX.x)),
        randint(int(RANDOM_SPAWN_MIN.y), int(RANDOM_SPAWN_MAX.y)),
    )


class Gameplay(State):
    """Playable state with two simple test maps."""

    def __init__(self, state_manager: StateManager):
        super().__init__(state_manager)

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["inventory"]:
                self.player.open_inventory()
            
            elif event.key == KEYS["escape"]:
                pygame.event.post(pygame.event.Event(pygame.QUIT, state = "quit"))
            
            elif event.key == KEYS["interact"]:
                for element in self.map.get_worldelements(self.player, INTERACT_RANGE):
                    if element.interact(self.player):
                        continue


        self.map.handle_events(event)
        self.player.handle_events(event)

    def load(self):
        screen_size = pygame.display.get_surface().get_size()

        self.camera = Camera((int(MAPSIZE.x), int(MAPSIZE.y)), screen_size, TILESIZE)

        self.player = Player(
            PLAYER_HP,
            ["Design/Hunter_Stand_DB_1.png"],
            PLAYER_SPAWN,
            self.camera,
        )

        allies = [Ally(10, ["Design\\Hunter_Stand_DB_2.png"], random_spawn_position()) for _ in range(ALLY_COUNT)]
        mobs = [Mob(10, ["Design\\Hunter_Walk_GB_3.png"], random_spawn_position()) for _ in range(MOB_COUNT)]

        items : Item = [
            sword(["Design\\sword.png"], random_spawn_position(), SWORD_ANGLE, SWORD_RANGE)
            for _ in range(ITEM_SPAWN_COUNT)
        ] + [
            gun(["Design\\gun.png"], random_spawn_position())
            for _ in range(ITEM_SPAWN_COUNT)
        ]

        self.map: Map = Map(
            mapsize=(int(MAPSIZE.x), int(MAPSIZE.y)),
            tileset=tileset,
            mapset=mapset,
            worldelements=allies + mobs + items,
        )
        self.map.load()
        self.player.load(self.map)

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

    def load_new_map(self, map_name: str):
        """Load a new map and update player/camera links."""
        if map_name not in self.maps:
            return

        self.map = self.maps[map_name]
        self.map.load()
        self.camera = self.cameras[map_name]
        self.player.camera = self.camera
        self.player.map = self.map
        self.player.get_coordinates = self.map.spawn_point

    def load_save(self, save_data: str):
        """Placeholder save-loading hook."""
        pass






tileset = Tileset(TILESET, tilesize=TILESIZE)
mapset = np.array([
    [1, 6, 2, 4, 1, 6, 2, 4, 1, 5, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 3, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6],
    [4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 3, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 1, 4, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1],
    [2, 4, 1, 6, 2, 4, 1, 6, 5, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 5, 1, 6, 2, 4, 1, 6],
    [6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 3, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2],
    [1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 3, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4],
    [4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 5, 2, 1, 6, 4, 2, 1, 6],
    [6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 3, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1],
    [2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 5, 4, 2, 1, 6, 4, 2, 1, 6, 4],
    [1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 3, 2, 1, 4, 6, 2],
    [6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 5, 2, 4, 1],
    [4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 3, 6, 1, 2, 4, 6, 1, 2],
    [2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 5, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6],
    [1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 18, 22, 6, 1, 4, 2, 6, 1, 3, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6],
    [6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 19, 23, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 5, 4, 6, 2, 1, 4],
    [4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 4, 6, 2, 1, 3, 6, 2, 1],
    [2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 5, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1],
    [1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 3, 4, 6],
    [6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 5, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4],
    [4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 3, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2],
    [2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 4, 6, 1, 2, 5, 6, 1, 2, 4, 6, 1],
    [1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 3, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2, 1, 6, 4, 2],
    [6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 5, 2, 4, 1],
    [4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 3, 2, 4, 1, 6, 2, 4, 1, 6, 2],
    [2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 5, 4],
    [1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 3, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6],
    [6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 5, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1, 6, 2, 4, 1],
    [4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 3, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6],
    [2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 5, 6, 4, 1, 2, 6, 4, 1],
    [1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 3, 4, 1, 2, 6, 4, 1, 2, 6, 4],
    [6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 4, 1, 2, 6, 5, 1, 2],
    [4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 3, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1, 4, 2, 6, 1],
])

