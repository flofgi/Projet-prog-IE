import pygame

from States.FirstMenu import FirstMenu
from States.StateManager import StateManager
from States.NextState import NextState
from States.Title import Title
from States.ParamState import ParamState
from States.KeyMenuState import KeyState 
from States.SwitchKeyState import SwitchKeyState
pygame.font.init()

FPS = 60 # lire dans la sauvegarde, les fps indiqués, sachant que la sauvegarde de cette ligne sera modifié dans la scène paramètre 

SCREEN_WIDTH = 640 # de même
SCREEN_HEIGHT = 360 # de même

#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)

pygame.display.set_caption("demo button")

state_manager = StateManager()
first_menu = FirstMenu(state_manager)
next_state = NextState(state_manager)
title = Title(state_manager)
paramState = ParamState(state_manager)
key_state = KeyState(state_manager)
switch_key_state = SwitchKeyState(state_manager)


state_manager.push_state(first_menu)

state_manager.register_route("title", title)
state_manager.register_route("first_menu", first_menu)
state_manager.register_route("next_state", next_state)
state_manager.register_route("param_state", paramState)
state_manager.register_route("key_state", key_state)
state_manager.register_route("Switch_key_state", switch_key_state)

clock = pygame.time.Clock()

run = True
while run:

    dt = clock.tick(FPS) / 1000

    screen.fill((6, 6, 7))

    state_manager.update(dt)
    state_manager.render(screen)

    pygame.display.flip()

pygame.quit()
    
