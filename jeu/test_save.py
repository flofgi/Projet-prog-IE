from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pygame

from Camera import Camera
from Item.Gun import gun
from Item.Sword import sword
from Map import Map, Tileset
from States.Gameplay import (
    ALLY_COUNT,
    BACKGROUND_COLOR,
    DEFAULT_MAPSET_PATH,
    DEFAULT_PLAYER_SPRITE,
    ITEM_SPAWN_COUNT,
    MAPSIZE,
    MOB_COUNT,
    PLAYER_HP,
    PLAYER_SPAWN,
    RANDOM_SPAWN_MAX,
    RANDOM_SPAWN_MIN,
    SWORD_ANGLE,
    SWORD_RANGE,
    TILESET,
    TILESIZE,
    Gameplay,
    random_spawn_position,
)
from States.StateManager import StateManager
from WorldElement.Ally import Ally
from WorldElement.Mob import Mob
from WorldElement.Player import Player


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 740
FPS = 60
GAME_NAME = "test_save"
FIRST_MAP_NAME = "map1"



class SaveTestGameplay(Gameplay):
    def load(self):
        screen_size = pygame.display.get_surface().get_size()

        self.player = Player(
            PLAYER_HP,
            [DEFAULT_PLAYER_SPRITE],
            PLAYER_SPAWN,
        )

        allies = [
            Ally(10, ["Design\Hunter_Walk_D_3.png"], random_spawn_position())
            for _ in range(ALLY_COUNT)
        ]
        mobs = [
            Mob(10, ["Design\Hunter_Walk_GB_3.png"], random_spawn_position())
            for _ in range(MOB_COUNT)
        ]
        items = [
            sword(["Design\sword.png"], random_spawn_position(), SWORD_ANGLE, SWORD_RANGE)
            for _ in range(ITEM_SPAWN_COUNT)
        ] + [
            gun(["Design\gun.png"], random_spawn_position())
            for _ in range(ITEM_SPAWN_COUNT)
        ]

        tileset = Tileset(TILESET)
        mapset = np.loadtxt(DEFAULT_MAPSET_PATH, dtype=int)

        self.map = Map(
            mapsize=(int(MAPSIZE.x), int(MAPSIZE.y)),
            tileset=tileset,
            mapset=mapset,
            name=FIRST_MAP_NAME,
        )
        self.map.allies = allies
        self.map.mobs = mobs
        self.map.items = items

        self.camera = Camera((int(MAPSIZE.x), int(MAPSIZE.y)), screen_size, TILESIZE)
        self.map.load()
        self.player.load(self.map, self.camera)


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)
    pygame.display.set_caption("save test")

    state_manager = StateManager()
    gameplay = SaveTestGameplay(state_manager, GAME_NAME, FIRST_MAP_NAME)
    state_manager.push_state(gameplay)

    screen.fill(BACKGROUND_COLOR)
    state_manager.update(1 / FPS)
    state_manager.render(screen)
    pygame.display.flip()

    gameplay.save()
    print(f"Saved current game to assets\saves\{GAME_NAME}")

    pygame.quit()


if __name__ == "__main__":
    main()
