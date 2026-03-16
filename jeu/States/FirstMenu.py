import pygame

from States.State import State

from States.Button import Button

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)

        button_game = pygame.image.load("Design/button_background.png").convert_alpha()
        button_game_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()   
        font1 = pygame.font.SysFont(None, 36)

        self.but_g = Button(300, 250, "Play", font1, button_game, button_game_hovered, 1)
        self.but_2 = Button(250, 200, "Options", font1, button_game, button_game_hovered, 1)

        self.statemanager = state_manager

        

    def load(self):
        print("Entering FirstMenu state")


    def update(self, dt: float, events: list[pygame.event.Event], mouse_pos: tuple[int, int]):
        """Handle the transition to the Menu state."""
        
        self.but_g.update(mouse_pos, events, self.statemanager)
        self.but_2.update(mouse_pos, events, self.statemanager)

    def render(self, screen: pygame.Surface):
        self.but_g.draw(screen)
        self.but_2.draw(screen)

    def unload(self):
        print("Exiting FirstMenu state")
