import pygame

from States.State import State

class FirstMenu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)

    def enter(self):
        print("Entering FirstMenu state")

    def update(self, dt, events):
        """Handle the transition to the Menu state."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.manager.change_state("Menu")


    def render(self, screen):
        """Render a text on the middle of the screen to indicate what to do."""

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    def exit(self):
        print("Exiting FirstMenu state")
