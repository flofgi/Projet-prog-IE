from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player
    from main import RECUP_EVENT



import pygame
from abc import ABC, abstractmethod


class Object(ABC):

    def __init__(self, sprites : list[str], coordinates: pygame.Vector2, durability: int = None):
        self.sprite: pygame.image = [pygame.image.load(s) for s in sprites]
        
        #Is None if the object have infinity durability
        self.durability = durability
        #Is None if the object is not drop
        self.coordinates = coordinates


    @abstractmethod
    def use(self):
        pass

    def interact(self, player: Player):
        if self.coordinates is not None and player.get_coordinates().distance_to(self.coordinates) < 20:
            pygame.event.post(pygame.event.Event(RECUP_EVENT, {
                "target": self
            }))
            self.coordinates = None


    def draw(self):
        pass

    def update(self, dt: float, events: list[pygame.event.Event], target: Player = None):
        pass