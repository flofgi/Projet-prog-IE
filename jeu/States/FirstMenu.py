import pygame

from States.State import State

from States.Button import Button
from States.ScrollButton import ScrollButton

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)

        button_game = pygame.image.load("Design/button_background.png").convert_alpha()
        button_game_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()   
        button_scroll_background = pygame.image.load("Design/scroll_button_background.png").convert_alpha()
        button_scroll = pygame.image.load("Design/scroll_button.png").convert_alpha()
        scroll_trail = pygame.image.load("Design/scroll_trail.png").convert_alpha()

        font1 = pygame.font.SysFont(None, 36)

        self.but_g = Button((266, 200), "Play", font1, button_game, button_game_hovered, 1)
        self.but_2 = ScrollButton((100, 400), button_scroll_background, button_scroll, scroll_trail, 1)

        self.statemanager = state_manager

    

    def load(self):
        print("Entering FirstMenu state")
        self.but_2.load()


    def update(self, dt: float, events: list[pygame.event.Event], mouse_pos: tuple[int, int]):
        """Handle the transition to the Menu state."""

        self.but_g.update(mouse_pos, events, self.statemanager)
        self.but_2.update(mouse_pos, events)

    def render(self, screen: pygame.Surface):
        self.but_g.draw(screen)
        self.but_2.draw(screen)

    def unload(self):
        print("Exiting FirstMenu state")
