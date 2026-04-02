import pygame

STATE_POP = pygame.event.custom_type()
STATE_PUSH = pygame.event.custom_type()
STATE_REPLACE = pygame.event.custom_type()
RECUP_EVENT = pygame.event.custom_type()
ALLY_EVENT = pygame.event.custom_type()
FULLSCREEN = pygame.event.custom_type()

KEYS = {
    "interact": pygame.K_e,
    "move_up": pygame.K_z,
    "move_down": pygame.K_s,
    "move_right": pygame.K_d,
    "move_left": pygame.K_q,
    "inventory": pygame.K_i,
    "escape": pygame.K_ESCAPE,

}