import pygame
import json
import os
# It's in a separate file to avoid circular imports with StateManager and the states that use it. Those under are customs type to post in the event queue.

STATE_REPLACE = pygame.event.custom_type()
STATE_POP = pygame.event.custom_type()
STATE_PUSH = pygame.event.custom_type()
FULLSCREEN = pygame.event.custom_type()
KEY_CHANGE = pygame.event.custom_type()
    

def update_json(section, new_data, file_path: str = None):
    if file_path:
        f_path = file_path
    else:
        f_path = "jeu/options.json"

    data = read_json(f_path)

    data[section] = new_data

    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_json(f_path) -> dict:
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            return json.load(f)