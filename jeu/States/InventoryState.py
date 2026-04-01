import pygame

from States.State import State
from events import STATE_PUSH, STATE_POP, STATE_REPLACE
from Player import Player, Inventory


class InventoryState(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """

    


    def load(self):
        self.player: Player = self.manager.routes["Gameplay"].player
        self.inventory: Inventory = self.player.inventory

                                       

    def handle_event(self, event: pygame.event.Event):
        """Handle events specific to the Inventory state.
        
        Args!
            event (pygame.event.Event): An event to handle.
        """
        

    def update(self, dt):
        """Handle the transition to the Menu state."""

        if self.screen_is_resized:
            self.START_POS = (self.screen_size[0] //2, self.screen_size[1] * ((1/16)+(1/2)))
            self.PARAM_POS = (self.screen_size[0] //2, self.screen_size[1] * ((1/8)+(1/2)))
            self.LEAVE_POS = (self.screen_size[0] //2, self.screen_size[1] * ((3/16)+(1/2)))

            self.GAME_TITLE_POS = (self.screen_size[0] // 2, self.screen_size[1] // 4)

            self.game_title_rect.center = self.GAME_TITLE_POS

            self.Param_button.update_position(self.PARAM_POS)
            self.Start_button.update_position(self.START_POS)
            self.Leave_button.update_position(self.LEAVE_POS)

            self.screen_is_resized = False

        self.Param_button.update(dt)
        self.Start_button.update(dt)
        self.Leave_button.update(dt)

    def render(self, screen: pygame.Surface):

        """Render the FirstMenu state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render the state on.
        """


    def unload(self):
        """Unload resources specific to the FirstMenu state."""

        