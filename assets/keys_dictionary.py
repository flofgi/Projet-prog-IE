import pygame
from utilitary import read_json

# To change key while the program is still loaded
KEYS = {
    "UP": pygame.K_z,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_q,
    "RIGHT": pygame.K_d,
    "INVENTORY": pygame.K_e,
    "INTERACT": pygame.K_a,
    "ESCAPE": pygame.K_ESCAPE,
    "ZOOM": pygame.K_o,
    "UNZOOM": pygame.K_p
}

MOUSE = {
    "inventorymouseSELECT": 1,
    "use_item": 1
}


def load_key(file_path: str = None):
    if file_path:
        f_path = file_path
    else:
        f_path = "jeu/options.json"
        f_path = "assets/options.json"

    data = read_json(f_path)
    section = "Saved_keys"

    saved_keys = data[section]

    for action, key in saved_keys.items():
        KEYS[action] = int(key)


