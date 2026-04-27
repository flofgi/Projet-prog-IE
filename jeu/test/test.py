from pathlib import Path
import pygame
import numpy as np


from jeu.utilitary import STATE_POP, STATE_PUSH, STATE_REPLACE, KEYS, RECUP_EVENT, ALLY_EVENT, FULLSCREEN
from jeu.States.StateManager import StateManager
from jeu.States.InventoryState import InventoryState
from jeu.States.Gameplay import Gameplay


pygame.font.init()

FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 740

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)

pygame.display.set_caption("demo button")

state_manager = StateManager()

gameplay = Gameplay(state_manager, "wiwi", "gameplay_test_map")
inventory_state = InventoryState(state_manager)

state_manager.push_state(gameplay)

state_manager.register_route("gameplay", gameplay)
state_manager.register_route("INVENTORY", inventory_state)

clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(FPS) / 1000

    screen.fill((6, 6, 7))

    state_manager.update(dt)
    state_manager.render(screen)
    pygame.display.flip()
pygame.quit()