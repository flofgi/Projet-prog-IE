import pygame

from States.State import State

class NextState(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        self.image = pygame.image.load("Design/Hunter_Walk_G_2.png").convert_alpha()

    def load(self):
        print("Entering NextState state")

    def update(self, dt: float):
        """Handle the transition to the Menu state."""
        pass

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.image, (100, 100))


    def unload(self):
        print("Exiting NextState state")