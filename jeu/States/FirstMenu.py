import pygame

from States.State import State
from EVENTS import STATE_PUSH, STATE_POP, STATE_REPLACE

from States.Buttons.ScrollButton import ScrollButton
from States.Buttons.TextButton import TextButton

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """
        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()

        self.screen_is_resized = False

        """ self.BUTTON1_POS = (screen_size[0] // 2, screen_size[1] // 4)
        self.BUTTON2_POS = (screen_size[0] // 2, screen_size[1] // 3)
        self.BUTTON3_POS = (screen_size[0] // 2, screen_size[1] // 2) """

        # x = center of the screen, y = write at the 3/4 of the screen, splite in 3 layers for the 3 buttons.
        self.START_POS = (self.screen_size[0] //2, self.screen_size[1] * ((1/16)+(1/2)))
        self.PARAM_POS = (self.screen_size[0] //2, self.screen_size[1] * ((1/8)+(1/2)))
        self.LEAVE_POS = (self.screen_size[0] //2, self.screen_size[1] * ((3/16)+(1/2)))

        self.GAME_TITLE_POS = (self.screen_size[0] // 2, self.screen_size[1] // 4)

        """ self.BUTTON1_SCALE = 1
        self.BUTTON2_SCALE = 1
        self.BUTTON3_SCALE = 1 """

    


    def load(self):
        """Load resources specific to the FirstMenu state."""

        # Load resources specific to the buttons.
        """ self.button_game = pygame.image.load("Design/button_background.png").convert_alpha()
        self.button_game_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()   
        self.button_scroll_background = pygame.image.load("Design/scroll_button_background.png").convert_alpha()
        self.button_scroll = pygame.image.load("Design/scroll_button.png").convert_alpha()
        self.scroll_trail = pygame.image.load("Design/scroll_trail.png").convert_alpha() """

        self.game_title = pygame.image.load("Design/game_title.png").convert_alpha()
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.center = self.GAME_TITLE_POS

        self.button_text_font = pygame.font.Font("Fonts/TLOZ.ttf", 18)
        self.button_text_color = (255, 255, 255)
        self.button_start_text = "start game"
        self.button_param_text = "parameters"
        self.button_leave_text = "leave"

        # Initialize buttons with their positions, sprites, and scale.
        """ self.but_g = Button1(self.BUTTON1_POS,
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

        self.but_g2 = Button1(self.BUTTON3_POS,
                             self.button_game,
                             self.button_game_hovered,
                             self.BUTTON3_SCALE,
                             "title",
                             STATE_REPLACE)"""
        
        self.Start_button = TextButton(self.START_POS,
                                       self.button_text_font,
                                       self.button_start_text,
                                       self.button_text_color,
                                       "next_state",
                                       STATE_PUSH)
        
        self.Param_button = TextButton(self.PARAM_POS,
                                       self.button_text_font,
                                       self.button_param_text,
                                       self.button_text_color,
                                       "param_state",
                                       STATE_PUSH)
        
        self.Leave_button = TextButton(self.LEAVE_POS,
                                       self.button_text_font,
                                       self.button_leave_text,
                                       self.button_text_color,
                                       "quit",
                                       pygame.QUIT)

                                       

    def handle_event(self, event: pygame.event.Event):
        """Handle events specific to the FirstMenu state.
        
        Args!
            event (pygame.event.Event): An event to handle.
        """
        
        # Handle events for the buttons.

        """ self.but_g.handle_event(event)
        self.but_2.handle_event(event)
        self.but_g2.handle_event(event) """
        self.Param_button.handle_event(event)
        self.Start_button.handle_event(event)
        self.Leave_button.handle_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.screen_size: tuple[int, int] = event.size
            self.screen_is_resized = True
            

    def update(self, dt):
        """Handle the transition to the Menu state."""

        # Update the buttons based on mouse position.
        """ self.but_g.update(dt)
        self.but_2.update(dt)
        self.but_g2.update(dt) """
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

        # Render the buttons on the screen.
        """ self.but_g.draw(screen)
        self.but_2.draw(screen)
        self.but_g2.draw(screen) """
        self.Param_button.draw(screen)
        self.Start_button.draw(screen)
        self.Leave_button.draw(screen)
        screen.blit(self.game_title, self.game_title_rect)

    def unload(self):
        """Unload resources specific to the FirstMenu state."""

        # Unload resources specific to the buttons.
        """ self.button_game = None
        self.button_game_hovered = None
        self.button_scroll_background = None
        self.button_scroll = None
        self.scroll_trail = None """
        self.button_text_font = None
        self.button_text_color = None
        self.button_start_text = None
        self.button_param_text = None
        self.button_leave_text = None
        