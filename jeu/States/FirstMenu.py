import pygame

from States.State import State
from EVENTS import STATE_PUSH, STATE_POP, STATE_REPLACE

from States.Button import Button
from States.ScrollButton import ScrollButton

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """

        screen_size: tuple[int, int] = pygame.display.get_window_size()

        self.BUTTON1_POS = (screen_size[0] // 2, screen_size[1] // 4)
        self.BUTTON2_POS = (screen_size[0] // 2, screen_size[1] // 3)
        self.BUTTON3_POS = (screen_size[0] // 2, screen_size[1] // 2)

        self.BUTTON1_SCALE = 1
        self.BUTTON2_SCALE = 1
        self.BUTTON3_SCALE = 1


    def load(self):
        """Load resources specific to the FirstMenu state."""

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
                            "next_state",
                            STATE_PUSH)
        
        self.but_2 = ScrollButton(self.BUTTON2_POS,
                                  self.button_scroll_background,
                                  self.button_scroll,
                                  self.scroll_trail, 
                                  self.BUTTON2_SCALE)

        self.but_g2 = Button(self.BUTTON3_POS,
                             self.button_game,
                             self.button_game_hovered,
                             self.BUTTON3_SCALE,
                             "title",
                             STATE_REPLACE)

    def handle_event(self, event: pygame.event.Event):
        """Handle events specific to the FirstMenu state.
        
        Args!
            event (pygame.event.Event): An event to handle.
        """
        
        # Handle events for the buttons.

        self.but_g.handle_event(event)
        self.but_2.handle_event(event)
        self.but_g2.handle_event(event)

    def update(self, dt):
        """Handle the transition to the Menu state."""

        # Update the buttons based on mouse position.
        self.but_g.update(dt)
        self.but_2.update(dt)
        self.but_g2.update(dt)

    def render(self, screen: pygame.Surface):

        """Render the FirstMenu state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render the state on.
        """

        # Render the buttons on the screen.
        self.but_g.draw(screen)
        self.but_2.draw(screen)
        self.but_g2.draw(screen)

    def unload(self):
        """Unload resources specific to the FirstMenu state."""

        # Unload resources specific to the buttons.
        self.button_game = None
        self.button_game_hovered = None
        self.button_scroll_background = None
        self.button_scroll = None
        self.scroll_trail = None

