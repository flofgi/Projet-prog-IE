import pygame

from abc import ABC, abstractmethod

class ButtonMenu(ABC):

    def __init__(self, x: int, y: int, scale: int, sprite: pygame.image):
        """Initialize the button with its position and size."""
        self.TOP_LEFT = (x, y)
        
        self.BaseScale = (int(sprite.get_width()*scale), int(sprite.get_height()*scale))

        self.image = pygame.transform.scale(sprite, self.BaseScale)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.TOP_LEFT

    def is_clicked(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]) -> bool:
        """Check if the button is clicked based on the mouse position."""
        if self.is_hovered(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        """Check if the mouse is hovering over the button."""
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    @abstractmethod
    def update(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]):
        """Update the button state based on mouse position and events."""
        pass