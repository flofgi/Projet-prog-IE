import pygame


RECUP_EVENT = pygame.event.custom_type()
ALLY_EVENT = pygame.event.custom_type()
OPEN_INVENTORY_EVENT = pygame.event.custom_type()
CLOSE_INVENTORY_EVENT = pygame.event.custom_type()

KEYS = {
    "interact": pygame.K_e,
    "move_up": pygame.K_z,
    "move_down": pygame.K_s,
    "move_right": pygame.K_d,
    "move_left": pygame.K_q

}