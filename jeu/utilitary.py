import pygame
import json
import os
# It's in a separate file to avoid circular imports with StateManager and the states that use it. Those under are customs type to post in the event queue.

STATE_POP = pygame.event.custom_type()
STATE_PUSH = pygame.event.custom_type()
STATE_REPLACE = pygame.event.custom_type()
RECUP_EVENT = pygame.event.custom_type()
ALLY_EVENT = pygame.event.custom_type()
FULLSCREEN = pygame.event.custom_type()
ATTACK = pygame.event.custom_type()
DEAD = pygame.event.custom_type()
BOSSFIGHT = pygame.event.custom_type()
GRENADE_EXPLOSION_EVENT = pygame.event.custom_type()

# BASIC COLOR

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKEN_COLOR = (0, 0, 0, 127)


def update_json(section, new_data, file_path: str = None):
    if file_path:
        f_path = file_path
    else:
        f_path = "assets/options.json"

    data = read_json(f_path)

    data[section] = new_data

    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_json(f_path) -> dict:
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            return json.load(f)
      

def vec_to_list(vec: pygame.Vector2 | None) -> list[float] | None:
    """Convert a pygame.Vector2 to a list of two floats, or return None if the input is None."""
    if vec is None:
        return None
    return [vec.x, vec.y]

def list_to_vec(lst: list[float] | None) -> pygame.Vector2 | None:
    if lst is None:
        return None
    return pygame.Vector2(lst[0], lst[1])
