import pygame

from States.State import State

class NextState(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        self.image = pygame.image.load("Design/Hunter_Walk_G_2.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] *10 ,self.image.get_size()[1] *10 )   )

        self.image2 = pygame.image.load("Design/Hunter_Walk_G_2.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (self.image2.get_size()[0] *10 ,self.image2.get_size()[1] *10 )   )

    def load(self):
        print("Entering NextState state")

    def update(self, dt: float):
        """Handle the transition to the Menu state."""
        pass

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.image, (100, 100))
        screen.blit(self.image2, (500, 100))


    def unload(self):
        print("Exiting NextState state")