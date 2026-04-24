import pygame
import json
import os

FPS = 60

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

KEYS= {
    "interact": pygame.K_e,
    "move_up": pygame.K_z,
    "move_down": pygame.K_s,
    "move_right": pygame.K_d,
    "move_left": pygame.K_q,
    "inventory": pygame.K_i,
    "escape": pygame.K_ESCAPE,
    "inventoryUP": pygame.K_UP,
    "inventoryDOWN": pygame.K_DOWN ,
    "inventoryLEFT": pygame.K_LEFT ,
    "inventoryRIGHT": pygame.K_RIGHT,
    "inventorySELECT": pygame.K_e
}

MOUSE = {
    "inventorymouseSELECT": 1,
    "use_item": 1
}



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