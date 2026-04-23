import os
import random
import shutil
import tempfile
from pathlib import Path

import pygame

from States.StateManager import StateManager
from States.State import State
from States.InventoryState import InventoryState
from States.Gameplay import Gameplay

from WorldElement import WorldElement, Player, Mob
from Item.Item import Item
from Item.Grenade import Grenade
from Item.Gun import gun
from Item.Sword import sword

from Map import Map, Tileset
from Camera import Camera


import numpy as np

from events import STATE_POP, STATE_PUSH, STATE_REPLACE, KEYS, RECUP_EVENT, ALLY_EVENT, FULLSCREEN

from abc import ABC, abstractmethod


pygame.font.init()

FPS = 60 # lire dans la sauvegarde, les fps indiqués, sachant que la sauvegarde de cette ligne sera modifié dans la scène paramètre 

SCREEN_WIDTH = 1280 # de même
SCREEN_HEIGHT = 740 # de même

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)

pygame.display.set_caption("demo button")

state_manager = StateManager()

gameplay = Gameplay(state_manager)
inventory_state = InventoryState(state_manager)

state_manager.push_state(gameplay)

state_manager.register_route("gameplay", gameplay)
state_manager.register_route("inventory", inventory_state)

clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(FPS) / 1000

    screen.fill((6, 6, 7))

    state_manager.update(dt)
    state_manager.render(screen)
    pygame.display.flip()
pygame.quit()