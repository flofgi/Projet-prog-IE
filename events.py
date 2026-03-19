import pygame

# It's in a separate file to avoid circular imports with StateManager and the states that use it. Those below are custom types to post in the event queue.

STATE_REPLACE = pygame.event.custom_type()
STATE_POP = pygame.event.custom_type()
STATE_PUSH = pygame.event.custom_type()
