from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from StateManager import StateManager


import pygame

from States.State import State
from events import STATE_PUSH, STATE_POP, STATE_REPLACE, KEYS
from Player import Player, Inventory


class InventoryState(State):

    def __init__(self, state_manager: StateManager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """
        self.cols = 5
        self.slot_size = 32
        self.gap = 14
        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()
        self.screen_is_resized = False
    


    def load(self):
        self.player: Player = self.manager.routes["gameplay"].player
        self.inventory: Inventory = self.player.inventory
        self.image = pygame.image.load("Design\Inventory.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_size[0]//2, self.screen_size[1]//2)

                                       

    def handle_events(self, event: pygame.event.Event):
        """Handle events specific to the Inventory state.
        
        Args:
            event (pygame.event.Event): An event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["inventory"]:
                self.inventory.close_inventory()
        

    def update(self, dt):
        """Handle the transition to the Menu state."""
        pass

    def render(self, screen: pygame.Surface):

        """Render the FirstMenu state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render the state on.
        """
        self.manager.states[-2].render(screen)
        screen.blit(self.image, self.rect)



    def unload(self):
        """Unload resources specific to the FirstMenu state."""

        