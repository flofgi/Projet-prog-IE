import pygame

from States.FirstMenu import FirstMenu
from States.StateManager import StateManager
from States.NextState import NextState

pygame.font.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("demo button")

state_manager = StateManager()
first_menu = FirstMenu(state_manager)
state_manager.push_state(first_menu)

run = True
while run:
    events = pygame.event.get()

    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((231, 211, 255))

    state_manager.update(0, events, mouse_pos)
    state_manager.render(screen)

    pygame.display.flip()

pygame.quit()



