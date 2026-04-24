import pygame

from States.FirstMenu import FirstMenu
from States.StateManager import StateManager
from States.NextState import NextState
from States.Title import Title
from States.ParamState import ParamState
from States.KeyMenuState import KeyState 
from States.SwitchKeyState import SwitchKeyState
from States.LanguageState import LanguageState
from utilitary import CHANGE_FPS, read_json


pygame.font.init()



data = read_json("assets/options.json")

FPS = data.get("Options", {}).get("fps", {}).get("Percentage", 1)*240

SCREEN_WIDTH = 1280 # de même
SCREEN_HEIGHT = 720 # de même

STATE_BACK_COLOR = (5, 5, 10)

#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE| pygame.DOUBLEBUF)

pygame.display.set_caption("demo button")

state_manager = StateManager()
first_menu = FirstMenu(state_manager)
next_state = NextState(state_manager)
title = Title(state_manager)
paramState = ParamState(state_manager)
key_state = KeyState(state_manager)
switch_key_state = SwitchKeyState(state_manager)
language_state = LanguageState(state_manager)


state_manager.push_state(first_menu)

state_manager.register_route("title", title)
state_manager.register_route("first_menu", first_menu)
state_manager.register_route("next_state", next_state)
state_manager.register_route("param_state", paramState)
state_manager.register_route("key_state", key_state)
state_manager.register_route("Switch_key_state", switch_key_state)
state_manager.register_route("language_state", language_state)

clock = pygame.time.Clock()

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state_manager.current_state.unload()
            raise SystemExit 
        elif event.type == CHANGE_FPS:
            FPS = event.fps
        else:
            state_manager.handle_event(event)

    dt = clock.tick(FPS) / 1000

    screen.fill((STATE_BACK_COLOR))

    state_manager.update(dt)
    state_manager.render(screen)

    pygame.display.flip()

pygame.quit()
    
