import pygame

from States.State import State

from States.Button import Button
from States.ScrollButton import ScrollButton

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager."""


        self.BUTTON1_POS = (266, 200)
        self.BUTTON2_POS = (100, 400)

        self.BUTTON1_SCALE = 1
        self.BUTTON2_SCALE = 1


    def load(self):
        # Load resources specific to the buttons.
        self.button_game = pygame.image.load("Design/button_background.png").convert_alpha()
        self.button_game_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()   
        self.button_scroll_background = pygame.image.load("Design/scroll_button_background.png").convert_alpha()
        self.button_scroll = pygame.image.load("Design/scroll_button.png").convert_alpha()
        self.scroll_trail = pygame.image.load("Design/scroll_trail.png").convert_alpha()

        # Initialize buttons with their positions, sprites, and scale.
        self.but_g = Button(self.BUTTON1_POS,
                            self.button_game, 
                            self.button_game_hovered, 
                            self.BUTTON1_SCALE,
                            self.manager,
                            "next_state")
        
        self.but_2 = ScrollButton(self.BUTTON2_POS,
                                  self.button_scroll_background,
                                  self.button_scroll,
                                  self.scroll_trail, 
                                  self.BUTTON2_SCALE,
                                  self.manager)

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle events specific to the FirstMenu state."""
        
        # Handle events for the buttons.

        self.but_g.handle_events(events)
        self.but_2.handle_events(events)

    def update(self, dt):
        """Handle the transition to the Menu state."""

        mouse_pos = pygame.mouse.get_pos()

        # Update the buttons based on mouse position.
        self.but_g.update(dt)
        self.but_2.update(dt)

    def render(self, screen: pygame.Surface):
        # Render the buttons on the screen.
        self.but_g.draw(screen)
        self.but_2.draw(screen)

    def unload(self):
        # Unload resources specific to the buttons.
        self.button_game = None
        self.button_game_hovered = None
        self.button_scroll_background = None
        self.button_scroll = None
        self.scroll_trail = None

