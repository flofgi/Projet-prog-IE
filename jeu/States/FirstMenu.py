import pygame

from States.State import State
from utilitary import STATE_PUSH, STATE_POP, STATE_REPLACE
from States.keys_dictionary import load_key

from States.Buttons.ScrollButton import ScrollButton
from States.Buttons.TextButton import TextButton

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """
        self.screen_is_resized = False

        # x = center of the screen, y = write at the 3*COLUMNS of the screen, splite in 3 layers for the 3 buttons.

        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()
        self.GAME_TITLE_POS = (self.screen_size[0] // 2, self.screen_size[1] // 4)

        load_key()

    def load(self):
        """Load resources specific to the FirstMenu state."""

        # Load resources specific to the buttons.

        self.game_title = pygame.image.load("Design/game_title.png").convert_alpha()
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.center = self.GAME_TITLE_POS

        self.button_text_font = pygame.font.Font("Fonts/TLOZ.ttf", 18)
        self.button_text_color = (255, 255, 255)

        # Initialize buttons with their positions, sprites, and scale.
        
        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()
        
        self._calculte_position(self.screen_size)

        self.Start_button = TextButton(self.START_POS,
                                       "next_state",
                                       STATE_REPLACE,
                                       self.button_text_font,
                                       name="button_game")
        
        self.Param_button = TextButton(self.PARAM_POS,
                                       "param_state",
                                       STATE_REPLACE,
                                       self.button_text_font,
                                       name="button_param")
        
        self.Leave_button = TextButton(self.LEAVE_POS,
                                       "quit",
                                       pygame.QUIT,
                                       self.button_text_font,
                                       name="button_quit")
        
        self._update_position()

                                       

    def handle_event(self, event: pygame.event.Event):
        """Handle events specific to the FirstMenu state.
        
        Args:
            event (pygame.event.Event): An event to handle.
        """
        
        # Handle events for the buttons.
        self.Param_button.handle_event(event)
        self.Start_button.handle_event(event)
        self.Leave_button.handle_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.screen_size: tuple[int, int] = event.size
            self.screen_is_resized = True
            

    def update(self, dt):
        """Handle the transition to the Menu state."""

        # Update the buttons based on mouse position.

        if self.screen_is_resized:
            self._calculte_position(self.screen_size)
            self._update_position()

            self.screen_is_resized = False

        self.Param_button.update(dt)
        self.Start_button.update(dt)
        self.Leave_button.update(dt)

    def render(self, screen: pygame.Surface):

        """Render the FirstMenu state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render the state on.
        """

        # Render the buttons on the screen.

        self.Param_button.draw(screen)
        self.Start_button.draw(screen)
        self.Leave_button.draw(screen)
        screen.blit(self.game_title, self.game_title_rect)

    def unload(self):
        """Unload resources specific to the FirstMenu state."""

        # Unload resources specific to the buttons.

        self.button_text_font = None
        self.button_text_color = None
        self.button_start_text = None
        self.button_param_text = None
        self.button_leave_text = None



    def _calculte_position(self, screen_size):
        self.START_POS = (screen_size[0] //2, screen_size[1] * ((1/16)+(1/2)))
        self.PARAM_POS = (screen_size[0] //2, screen_size[1] * ((1/8)+(1/2)))
        self.LEAVE_POS = (screen_size[0] //2, screen_size[1] * ((3/16)+(1/2)))

        self.GAME_TITLE_POS = (screen_size[0] // 2, screen_size[1] // 4)


    def _update_position(self):
        self.Start_button.update_position(self.START_POS)
        self.Param_button.update_position(self.PARAM_POS)
        self.Leave_button.update_position(self.LEAVE_POS)

        self.game_title_rect.center = self.GAME_TITLE_POS   